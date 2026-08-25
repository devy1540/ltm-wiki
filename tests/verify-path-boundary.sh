#!/bin/sh

set -eu

root=${1:-tests/fixtures/path-boundary}

source_path=$(sed -n 's/^source_path: //p' "$root/wiki/source-notes/traversal.md")
case "$source_path" in
  sources/*) echo 'seeded traversal source_path unexpectedly begins with sources/' >&2; exit 1;;
esac
case "/$source_path/" in
  */../*) ;;
  *) echo 'seeded traversal source_path is missing parent traversal' >&2; exit 1;;
esac

sources_real=$(CDPATH= cd -- "$root/sources" && pwd -P)
valid_real=$(realpath "$root/sources/valid.md")
outside_real=$(realpath "$root/outside.md")
evidence_real=$(realpath "$root/wiki/topics/../../outside.md")

case "$valid_real" in
  "$sources_real"/*) ;;
  *) echo 'valid source did not remain inside canonical sources' >&2; exit 1;;
esac

case "$evidence_real" in
  "$sources_real"/*) echo 'outside evidence unexpectedly resolved inside sources' >&2; exit 1;;
esac

temp_root=$(mktemp -d)
mkdir -p "$temp_root/sources"
ln -s "$outside_real" "$temp_root/sources/escape.md"
escape_real=$(realpath "$temp_root/sources/escape.md")
temp_sources_real=$(CDPATH= cd -- "$temp_root/sources" && pwd -P)
case "$escape_real" in
  "$temp_sources_real"/*) echo 'symlink escape unexpectedly remained inside sources' >&2; exit 1;;
esac

echo 'path boundary validation passed'
