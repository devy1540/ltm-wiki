#!/bin/sh

set -eu

phase_dir=tests/evidence/phases
manifest_dir="$phase_dir/manifests"
delta_dir="$phase_dir/deltas"
temp_root=$(mktemp -d)
mkdir -p "$temp_root"
cp -R tests/fixtures/basic-project/baseline/wiki "$temp_root/wiki"

verify_manifest() {
  manifest=$1
  while IFS='  ' read -r expected path; do
    [ -z "$expected" ] && continue
    target="$temp_root/$path"
    if command -v sha256sum >/dev/null 2>&1; then
      actual=$(sha256sum "$target" | awk '{print $1}')
    else
      actual=$(shasum -a 256 "$target" | awk '{print $1}')
    fi
    [ "$actual" = "$expected" ] || {
      echo "phase manifest mismatch: $manifest -> $path" >&2
      exit 1
    }
  done < "$manifest"

  actual_files=$(CDPATH= cd -- "$temp_root" && find wiki -type f | sort)
  manifest_files=$(awk '{print $2}' "$manifest" | sort)
  [ "$actual_files" = "$manifest_files" ] || {
    echo "phase file set mismatch: $manifest" >&2
    exit 1
  }
}

apply_delta() {
  delta=$1
  patch -s -p1 -d "$temp_root" < "$delta"
}

claim_block() {
  claim_id=$1
  file=$2
  awk -v marker="<a id=\"claim-$claim_id\"></a>" '
    $0 == marker { found=1; next }
    found && /^<a id="claim-/ { exit }
    found { print }
  ' "$file"
}

verify_manifest "$manifest_dir/00-baseline.sha256"

apply_delta "$delta_dir/00-to-01.diff"
verify_manifest "$manifest_dir/01-architecture-v1.sha256"
claim_block transport-public-http-json "$temp_root/wiki/topics/transport.md" | grep -q '\*\*State:\*\* current'

apply_delta "$delta_dir/01-to-02.diff"
verify_manifest "$manifest_dir/02-protocol-review.sha256"
claim_block transport-public-http-json "$temp_root/wiki/topics/transport.md" | grep -q '\*\*State:\*\* disputed'
claim_block transport-grpc-default-recommendation "$temp_root/wiki/topics/transport.md" | grep -q '\*\*State:\*\* disputed'
claim_block transport-public-http-json "$temp_root/wiki/topics/transport.md" | grep -q '\*\*Contradicts:\*\*'
claim_block transport-grpc-default-recommendation "$temp_root/wiki/topics/transport.md" | grep -q '\*\*Contradicts:\*\*'

apply_delta "$delta_dir/02-to-03.diff"
verify_manifest "$manifest_dir/03-architecture-v2.sha256"
claim_block transport-public-http-json "$temp_root/wiki/topics/transport.md" | grep -q '\*\*State:\*\* current'
claim_block transport-public-http-json "$temp_root/wiki/topics/transport.md" | grep -q '\*\*Supersedes:\*\*'
claim_block transport-grpc-default-recommendation "$temp_root/wiki/topics/transport.md" | grep -q '\*\*State:\*\* superseded'
claim_block transport-grpc-default-recommendation "$temp_root/wiki/topics/transport.md" | grep -q '\*\*Superseded by:\*\*'
claim_block transport-grpc-default-recommendation "$temp_root/wiki/topics/transport.md" | grep -q '\*\*Contradicts:\*\*'

apply_delta "$delta_dir/03-to-04.diff"
verify_manifest "$manifest_dir/04-operational-notes.sha256"
grep -q 'rollout-ownership.md' "$temp_root/wiki/topics/transport.md"
grep -q 'upload-retention-unspecified' "$temp_root/wiki/topics/rollout-ownership.md"

[ "$(grep -c '^diff -ruN ' "$delta_dir/04-to-05.diff")" -eq 1 ]
grep -q 'wiki/operations.md' "$delta_dir/04-to-05.diff"
apply_delta "$delta_dir/04-to-05.diff"
verify_manifest "$manifest_dir/05-repeat-noop.sha256"
grep -q 'no-op' "$temp_root/wiki/operations.md"

cmp -s "$manifest_dir/05-repeat-noop.sha256" "$manifest_dir/06-query-readonly.sha256" || {
  echo 'query-only phase changed the Wiki tree' >&2
  exit 1
}
verify_manifest "$manifest_dir/06-query-readonly.sha256"
if [ -d "$temp_root/wiki/syntheses" ]; then
  pre_crystallize_count=$(find "$temp_root/wiki/syntheses" -type f -name '*.md' | wc -l | tr -d ' ')
else
  pre_crystallize_count=0
fi
[ "$pre_crystallize_count" -eq 0 ]

apply_delta "$delta_dir/06-to-07.diff"
verify_manifest "$manifest_dir/07-crystallized.sha256"
[ "$(find "$temp_root/wiki/syntheses" -type f -name '*.md' | wc -l | tr -d ' ')" -eq 1 ]
grep -R -q '\*\*Kind:\*\* derived' "$temp_root/wiki/syntheses"
grep -R -q '\*\*Derived from:\*\*' "$temp_root/wiki/syntheses"

cmp -s "$phase_dir/sources.sha256" tests/fixtures/basic-project/expected/raw.sha256

echo 'phased evidence validation passed'
