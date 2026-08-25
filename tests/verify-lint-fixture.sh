#!/bin/sh

set -eu

seed=tests/fixtures/basic-project/lint-seed
repaired=tests/fixtures/basic-project/lint-repaired
evidence=tests/evidence

for source in tests/fixtures/basic-project/sources/*.md; do
  name=$(basename "$source")
  cmp -s "$source" "$seed/sources/$name" || {
    echo "lint seed source mismatch: $name" >&2
    exit 1
  }
  cmp -s "$source" "$repaired/sources/$name" || {
    echo "lint repaired source mismatch: $name" >&2
    exit 1
  }
done

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
      echo "manifest mismatch: $manifest -> $path" >&2
      exit 1
    }
  done < "$manifest"
}

verify_manifest "$seed" "$evidence/manifests/lint-pre.sha256"
verify_manifest "$seed" "$evidence/manifests/lint-post-readonly.sha256"
cmp -s "$evidence/manifests/lint-pre.sha256" "$evidence/manifests/lint-post-readonly.sha256"
verify_manifest "$repaired" "$evidence/manifests/lint-repaired.sha256"

grep -q 'topics/does-not-exist.md' "$seed/wiki/index.md"
if grep -q 'topics/does-not-exist.md' "$repaired/wiki/index.md"; then
  echo 'approved broken link remains in repaired fixture' >&2
  exit 1
fi

seed_files=$(CDPATH= cd -- "$seed/wiki" && find . -type f | sort)
repaired_files=$(CDPATH= cd -- "$repaired/wiki" && find . -type f | sort)
[ "$seed_files" = "$repaired_files" ] || {
  echo 'lint repair changed the Wiki file set' >&2
  exit 1
}

printf '%s\n' "$seed_files" | while IFS= read -r path; do
  case "$path" in
    ./index.md|./operations.md) continue;;
  esac
  cmp -s "$seed/wiki/$path" "$repaired/wiki/$path" || {
    echo "unapproved lint repair changed: $path" >&2
    exit 1
  }
done

cmp -s "$seed/wiki/operations.md" tests/fixtures/basic-project/golden/wiki/operations.md || {
  echo 'lint seed did not preserve the generated operation history' >&2
  exit 1
}

seed_operation_bytes=$(wc -c < "$seed/wiki/operations.md" | tr -d ' ')
head -c "$seed_operation_bytes" "$repaired/wiki/operations.md" | cmp -s - "$seed/wiki/operations.md" || {
  echo 'lint repair did not preserve the operation log as an exact prefix' >&2
  exit 1
}

[ "$(grep -c '| repair |' "$repaired/wiki/operations.md")" -eq 1 ]
[ "$(grep -c '^diff -ru .*wiki/' "$evidence/lint-repair.diff")" -eq 2 ]

for finding in LWM-MS-001 LWM-ML-002 LWM-MC-003 LWM-SS-004; do
  grep -q "$finding" "$evidence/lint-report.md" || {
    echo "missing retained lint finding: $finding" >&2
    exit 1
  }
done

echo 'lint fixture validation passed'
