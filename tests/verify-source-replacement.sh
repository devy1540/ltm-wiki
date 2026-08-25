#!/bin/sh

set -eu

root=${1:-tests/fixtures/source-replacement/golden}
wiki="$root/wiki"

cmp -s "$root/sources/policy.md" tests/fixtures/source-replacement/versions/policy-v2.md || {
  echo 'golden replacement source must match policy-v2.md' >&2
  exit 1
}

note="$wiki/source-notes/policy.md"
topic="$wiki/topics/client-policy.md"
synthesis="$wiki/syntheses/client-request-behavior.md"
operations="$wiki/operations.md"

grep -q '^source_digest: sha256:9b721fb2d9dfe360bdc38283e54ac3677962c040f6f9b4bbae63e1052cc0cf61$' "$note"

recorded_digest=$(sed -n 's/^source_digest: sha256://p' "$note")
if command -v sha256sum >/dev/null 2>&1; then
  actual_digest=$(sha256sum "$root/sources/policy.md" | awk '{print $1}')
else
  actual_digest=$(shasum -a 256 "$root/sources/policy.md" | awk '{print $1}')
fi
[ "$recorded_digest" = "$actual_digest" ]

if sed -n '/^## Important assertions/,$p' "$note" | grep -q '30-second'; then
  echo 'replacement source note still asserts the removed timeout' >&2
  exit 1
fi

claim_block() {
  claim_id=$1
  file=$2
  awk -v marker="<a id=\"claim-$claim_id\"></a>" '
    $0 == marker { found=1; next }
    found && /^<a id="claim-/ { exit }
    found { print }
  ' "$file"
}

claim_block client-timeout-30-seconds "$topic" | grep -q '\*\*State:\*\* stale'
claim_block client-timeout-30-seconds "$topic" | grep -q '\*\*Former evidence:\*\*'
claim_block client-timeout-30-seconds "$topic" | grep -q 'sha256:1e5a4a8b80c727eec7905a96f8a122914d14fffb4f3b3dd1e11845eb700b5d9e'
claim_block client-timeout-30-seconds "$topic" | grep -q 'heading "Timeout", lines 3-5'
claim_block client-reliability-guidance-ownership "$topic" | grep -q '\*\*State:\*\* current'
claim_block client-request-behavior "$synthesis" | grep -q '\*\*State:\*\* stale'

grep -q '1e5a4a8b80c727eec7905a96f8a122914d14fffb4f3b3dd1e11845eb700b5d9e -> sha256:9b721fb2d9dfe360bdc38283e54ac3677962c040f6f9b4bbae63e1052cc0cf61' "$operations"
grep -q 'current -> stale' "$operations"
grep -q 'no-op' "$operations"

baseline_operations=tests/fixtures/source-replacement/baseline/wiki/operations.md
[ "$(sed -n '1,6p' "$operations")" = "$(sed -n '1,6p' "$baseline_operations")" ] || {
  echo 'pre-existing operations history was not preserved verbatim' >&2
  exit 1
}

anchors=$(grep -Rho '<a id="claim-[^"]*"></a>' "$wiki" | sort)
duplicates=$(printf '%s\n' "$anchors" | uniq -d)
[ -z "$duplicates" ] || {
  echo "duplicate replacement claim anchors: $duplicates" >&2
  exit 1
}

find "$wiki" -type f -name '*.md' | while IFS= read -r page; do
  grep -oE '\]\([^)]+\)' "$page" 2>/dev/null | while IFS= read -r raw; do
    target=${raw#']('}
    target=${target%')'}
    case "$target" in
      http://*|https://*|mailto:*|'#'*) continue;;
    esac
    target=${target%%#*}
    [ -z "$target" ] && continue
    resolved=$(CDPATH= cd -- "$(dirname -- "$page")" && cd -- "$(dirname -- "$target")" && pwd)/$(basename -- "$target")
    [ -f "$resolved" ] || {
      echo "broken replacement link in $page: $target" >&2
      exit 1
    }
  done
done

echo 'source replacement validation passed'
