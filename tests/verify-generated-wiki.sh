#!/bin/sh

set -eu

root=${1:-tests/fixtures/basic-project/golden}
wiki="$root/wiki"
sources="$root/sources"

for path in \
  "$wiki/index.md" \
  "$wiki/operations.md" \
  "$wiki/topics/transport.md" \
  "$wiki/syntheses/transport-comparison.md"; do
  [ -f "$path" ] || {
    echo "missing generated artifact: $path" >&2
    exit 1
  }
done

source_note_count=$(find "$wiki/source-notes" -type f -name '*.md' | wc -l | tr -d ' ')
[ "$source_note_count" -eq 4 ] || {
  echo "expected 4 source notes, found $source_note_count" >&2
  exit 1
}

if grep -R '<a id="claim-' "$wiki/source-notes" >/dev/null 2>&1; then
  echo 'source notes must not own reconciled claim blocks' >&2
  exit 1
fi

for note in "$wiki"/source-notes/*.md; do
  source_path=$(sed -n 's/^source_path: //p' "$note")
  recorded_digest=$(sed -n 's/^source_digest: sha256://p' "$note")
  case "$source_path" in
    sources/*) ;;
    *) echo "invalid source_path in $note: $source_path" >&2; exit 1;;
  esac
  case "/$source_path/" in
    */../*) echo "parent traversal in source_path: $source_path" >&2; exit 1;;
  esac
  source_file="$root/$source_path"
  if command -v sha256sum >/dev/null 2>&1; then
    actual_digest=$(sha256sum "$source_file" | awk '{print $1}')
  else
    actual_digest=$(shasum -a 256 "$source_file" | awk '{print $1}')
  fi
  [ "$recorded_digest" = "$actual_digest" ] || {
    echo "source-note digest mismatch in $note" >&2
    exit 1
  }
done

transport="$wiki/topics/transport.md"
for id in \
  transport-public-http \
  transport-all-new-grpc \
  transport-internal-grpc \
  transport-rollout-owner; do
  count=$(grep -c "<a id=\"claim-$id\"></a>" "$transport")
  [ "$count" -eq 1 ] || {
    echo "expected one topic claim $id, found $count" >&2
    exit 1
  }
done

all_anchors=$(grep -Rho '<a id="claim-[^"]*"></a>' "$wiki" | sort)
duplicate_anchors=$(printf '%s\n' "$all_anchors" | uniq -d)
[ -z "$duplicate_anchors" ] || {
  echo "duplicate claim anchors: $duplicate_anchors" >&2
  exit 1
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

claim_block transport-public-http "$transport" | grep -q '\*\*State:\*\* current'
claim_block transport-public-http "$transport" | grep -q '\*\*Supersedes:\*\*'
claim_block transport-all-new-grpc "$transport" | grep -q '\*\*State:\*\* superseded'
claim_block transport-all-new-grpc "$transport" | grep -q '\*\*Contradicts:\*\*'
claim_block transport-all-new-grpc "$transport" | grep -q '\*\*Superseded by:\*\*'
claim_block transport-internal-grpc "$transport" | grep -q '\*\*State:\*\* current'
claim_block transport-internal-grpc "$transport" | grep -q '\*\*Supersedes:\*\*'
claim_block transport-rollout-owner "$transport" | grep -q '\*\*State:\*\* current'

synthesis="$wiki/syntheses/transport-comparison.md"
claim_block transport-approved-client-internal-policy "$synthesis" | grep -q '\*\*Kind:\*\* derived'
claim_block transport-approved-client-internal-policy "$synthesis" | grep -q '\*\*Derived from:\*\*'

grep -q 'no-op' "$wiki/operations.md"
grep -q '| crystallize |' "$wiki/operations.md"

for source in tests/fixtures/basic-project/sources/*.md; do
  name=$(basename "$source")
  cmp -s "$source" "$sources/$name" || {
    echo "golden source differs from fixture source: $name" >&2
    exit 1
  }
done

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
      echo "broken generated link in $page: $target" >&2
      exit 1
    }
  done
done

echo 'generated wiki validation passed'
