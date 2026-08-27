#!/bin/sh

set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root"

required_files='
README.md
docs/product-definition.md
docs/mvp-scenarios.md
.codex-plugin/plugin.json
skills/llm-wiki/SKILL.md
skills/llm-wiki/agents/openai.yaml
skills/llm-wiki/references/project-resolution.md
skills/llm-wiki/references/external-source-import.md
skills/llm-wiki/references/storage-model.md
skills/llm-wiki/references/setup.md
skills/llm-wiki/references/ingest.md
skills/llm-wiki/references/query.md
skills/llm-wiki/references/crystallize.md
skills/llm-wiki/references/lint.md
skills/llm-wiki/assets/wiki-template/schema.md
skills/llm-wiki/assets/wiki-template/index.md
skills/llm-wiki/assets/wiki-template/operations.md
skills/llm-wiki/scripts/llm_wiki_common.py
skills/llm-wiki/scripts/project_resolver.py
skills/llm-wiki/scripts/import_source.py
tests/acceptance.md
tests/test_plugin_package.py
tests/test_project_resolver.py
tests/test_import_source.py
tests/test_cli_flow.py
tests/evidence/2026-08-24-forward-tests.md
tests/evidence/basic-flow-transcript.md
tests/evidence/phased-basic-flow.md
tests/evidence/lint-report.md
tests/evidence/source-replacement-report.md
tests/evidence/path-boundary-report.md
tests/evidence/basic-flow.diff
tests/evidence/lint-repair.diff
tests/evidence/source-replacement.diff
tests/evidence/manifests/basic-golden.sha256
tests/evidence/manifests/lint-pre.sha256
tests/evidence/manifests/lint-post-readonly.sha256
tests/evidence/manifests/lint-repaired.sha256
tests/evidence/manifests/source-replacement-golden.sha256
tests/fixtures/basic-project/expected/raw.sha256
tests/fixtures/basic-project/golden/wiki/topics/transport.md
tests/fixtures/source-replacement/expected.md
tests/fixtures/source-replacement/version-hashes.sha256
tests/fixtures/source-replacement/golden/wiki/topics/client-policy.md
tests/fixtures/path-boundary/expected.md
tests/verify-generated-wiki.sh
tests/verify-source-replacement.sh
tests/verify-path-boundary.sh
tests/verify-lint-fixture.sh
tests/verify-phased-evidence.sh
'

printf '%s\n' "$required_files" | while IFS= read -r path; do
  [ -z "$path" ] && continue
  if [ ! -f "$path" ]; then
    echo "missing required file: $path" >&2
    exit 1
  fi
done

[ -L .agents/skills/llm-wiki ] || {
  echo '.agents/skills/llm-wiki must be a compatibility symlink' >&2
  exit 1
}

[ "$(readlink .agents/skills/llm-wiki)" = '../../skills/llm-wiki' ] || {
  echo 'unexpected .agents skill link target' >&2
  exit 1
}

skill_file=skills/llm-wiki/SKILL.md
[ "$(sed -n '1p' "$skill_file")" = '---' ]
sed -n '2,8p' "$skill_file" | grep -q '^name: llm-wiki$'
sed -n '2,8p' "$skill_file" | grep -q '^description: '

for ref in project-resolution setup external-source-import ingest query crystallize lint storage-model; do
  grep -q "references/$ref.md" "$skill_file" || {
    echo "skill does not route to references/$ref.md" >&2
    exit 1
  }
done

fixture=tests/fixtures/basic-project
while IFS='  ' read -r expected path; do
  [ -z "$expected" ] && continue
  target="$fixture/$path"
  if command -v sha256sum >/dev/null 2>&1; then
    actual=$(sha256sum "$target" | awk '{print $1}')
  elif command -v shasum >/dev/null 2>&1; then
    actual=$(shasum -a 256 "$target" | awk '{print $1}')
  else
    echo 'no SHA-256 command available' >&2
    exit 1
  fi
  if [ "$actual" != "$expected" ]; then
    echo "fixture hash mismatch: $path" >&2
    exit 1
  fi
done < "$fixture/expected/raw.sha256"

replacement=tests/fixtures/source-replacement
while IFS='  ' read -r expected path; do
  [ -z "$expected" ] && continue
  target="$replacement/$path"
  if command -v sha256sum >/dev/null 2>&1; then
    actual=$(sha256sum "$target" | awk '{print $1}')
  else
    actual=$(shasum -a 256 "$target" | awk '{print $1}')
  fi
  [ "$actual" = "$expected" ] || {
    echo "replacement fixture hash mismatch: $path" >&2
    exit 1
  }
done < "$replacement/version-hashes.sha256"

verify_manifest() {
  root=$1
  manifest=$2
  while IFS='  ' read -r expected path; do
    [ -z "$expected" ] && continue
    target="$root/$path"
    if command -v sha256sum >/dev/null 2>&1; then
      actual=$(sha256sum "$target" | awk '{print $1}')
    else
      actual=$(shasum -a 256 "$target" | awk '{print $1}')
    fi
    [ "$actual" = "$expected" ] || {
      echo "evidence manifest mismatch: $manifest -> $path" >&2
      exit 1
    }
  done < "$manifest"
}

verify_manifest "$fixture/golden" tests/evidence/manifests/basic-golden.sha256
verify_manifest "$replacement/golden" tests/evidence/manifests/source-replacement-golden.sha256

verify_diff() {
  left=$1
  right=$2
  retained=$3
  generated=$(mktemp)
  normalized_generated=$(mktemp)
  normalized_retained=$(mktemp)
  if diff -ru "$left" "$right" > "$generated"; then
    echo "expected fixture differences but found none: $left -> $right" >&2
    exit 1
  else
    code=$?
    [ "$code" -eq 1 ] || exit "$code"
  fi
  sed -E 's/^((---|\+\+\+) [^[:space:]]+)[[:space:]]+[0-9]{4}-[0-9]{2}-[0-9]{2}.*$/\1/' \
    "$generated" > "$normalized_generated"
  sed -E 's/^((---|\+\+\+) [^[:space:]]+)[[:space:]]+[0-9]{4}-[0-9]{2}-[0-9]{2}.*$/\1/' \
    "$retained" > "$normalized_retained"
  cmp -s "$normalized_generated" "$normalized_retained" || {
    echo "retained diff is stale: $retained" >&2
    exit 1
  }
  rm -f "$generated" "$normalized_generated" "$normalized_retained"
}

verify_diff "$fixture/baseline/wiki" "$fixture/golden/wiki" tests/evidence/basic-flow.diff
verify_diff "$fixture/lint-seed/wiki" "$fixture/lint-repaired/wiki" tests/evidence/lint-repair.diff
verify_diff "$replacement/baseline/wiki" "$replacement/golden/wiki" tests/evidence/source-replacement.diff

cmp -s "$replacement/baseline/sources/policy.md" "$replacement/versions/policy-v1.md" || {
  echo 'replacement baseline must start from policy-v1.md' >&2
  exit 1
}

grep -q '^source_path: ../outside.md$' tests/fixtures/path-boundary/wiki/source-notes/traversal.md
grep -q '../../outside.md' tests/fixtures/path-boundary/wiki/topics/boundary.md

claim_count=$(grep -c '^## `transport-' "$fixture/expected/claim-register.md")
[ "$claim_count" -eq 4 ] || {
  echo "expected 4 oracle claims, found $claim_count" >&2
  exit 1
}

grep -q 'not a general-purpose agent-memory system' README.md || {
  echo 'README must retain the Agent Memory boundary' >&2
  exit 1
}

grep -q 'does not require third-party Python packages' README.md || {
  echo 'README must state the third-party dependency boundary' >&2
  exit 1
}

grep -q 'allow_implicit_invocation: true' skills/llm-wiki/agents/openai.yaml || {
  echo 'skill metadata must allow implicit invocation' >&2
  exit 1
}

grep -q 'Mutual contradiction' "$fixture/expected/required-relations.md" || {
  echo 'oracle must require mutual contradiction links' >&2
  exit 1
}

grep -q 'Both supersession directions' "$fixture/expected/required-relations.md" || {
  echo 'oracle must require bidirectional supersession links' >&2
  exit 1
}

sh tests/verify-generated-wiki.sh "$fixture/golden"
sh tests/verify-source-replacement.sh "$replacement/golden"
sh tests/verify-path-boundary.sh tests/fixtures/path-boundary
sh tests/verify-lint-fixture.sh
sh tests/verify-phased-evidence.sh
python3 -m unittest \
  tests/test_plugin_package.py \
  tests/test_project_resolver.py \
  tests/test_import_source.py \
  tests/test_cli_flow.py

find . -path './.git' -prune -o -type f -print | while IFS= read -r file; do
  case "$file" in
    *.diff|*.pyc|*/__pycache__/*) continue;;
  esac
  if grep -n '[[:blank:]]$' "$file" >/dev/null 2>&1; then
    echo "trailing whitespace: $file" >&2
    exit 1
  fi
  last_byte=$(tail -c 1 "$file" | od -An -t u1 | tr -d ' ')
  [ "$last_byte" = '10' ] || {
    echo "missing final newline: $file" >&2
    exit 1
  }
done

echo 'repository validation passed'
