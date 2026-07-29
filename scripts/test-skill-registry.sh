#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

compare_sets() {
  local expected="$1"
  local actual="$2"
  local label="$3"

  if ! diff -u "$expected" "$actual"; then
    fail "$label does not match shipped skill directories"
  fi
}

command -v jq >/dev/null || fail "jq is required"

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

find skills -mindepth 3 -maxdepth 3 -name SKILL.md -type f -print \
  | sed 's#/SKILL.md$##' \
  | sort -u >"$tmp_dir/skills"

jq -e '
  .name == "agent-skill-forge" and
  (.version | test("^[0-9]+\\.[0-9]+\\.[0-9]+$")) and
  (.description | type == "string" and length > 0) and
  (.author.name | type == "string" and length > 0) and
  (.skills | type == "array" and length > 0) and
  all(.skills[]; test("^\\./skills/(engineering|productivity|research)/[^/]+$"))
' .claude-plugin/plugin.json >/dev/null || fail "invalid plugin manifest metadata or skill path"

jq -r '.skills[] | sub("^\\./"; "")' .claude-plugin/plugin.json \
  | sort -u >"$tmp_dir/manifest"

find skills -path '*/agents/openai.yaml' -type f -print \
  | sed 's#/agents/openai.yaml$##' \
  | sort -u >"$tmp_dir/sidecars"

rg -o '\(\./skills/(engineering|productivity|research)/[^/)]+/SKILL\.md\)' README.md \
  | sed -E 's#^\(\./##; s#/SKILL\.md\)$##' \
  | sort -u >"$tmp_dir/top-readme"

: >"$tmp_dir/bucket-readmes"
for bucket in engineering productivity research; do
  rg -o '\(\./[^/)]+/SKILL\.md\)' "skills/$bucket/README.md" \
    | sed -E 's#^\(\./##; s#/SKILL\.md\)$##' \
    | sed "s#^#skills/$bucket/#" >>"$tmp_dir/bucket-readmes"
done
sort -u "$tmp_dir/bucket-readmes" -o "$tmp_dir/bucket-readmes"

compare_sets "$tmp_dir/skills" "$tmp_dir/manifest" "plugin manifest"
compare_sets "$tmp_dir/skills" "$tmp_dir/sidecars" "Codex sidecars"
compare_sets "$tmp_dir/skills" "$tmp_dir/top-readme" "top-level README"
compare_sets "$tmp_dir/skills" "$tmp_dir/bucket-readmes" "bucket READMEs"

while IFS= read -r skill_dir; do
  skill_md="$skill_dir/SKILL.md"
  sidecar="$skill_dir/agents/openai.yaml"

  rg -q '^interface:$' "$sidecar" || fail "missing interface block: $sidecar"
  rg -q '^  display_name: ".+"$' "$sidecar" || fail "missing display_name: $sidecar"
  rg -q '^  short_description: ".+"$' "$sidecar" || fail "missing short_description: $sidecar"

  if rg -q '^disable-model-invocation: true$' "$skill_md"; then
    rg -q '^policy:$' "$sidecar" || fail "missing user-only policy block: $sidecar"
    rg -q '^  allow_implicit_invocation: false$' "$sidecar" || fail "implicit invocation must be false: $sidecar"
  else
    if rg -q '^(policy:|  allow_implicit_invocation:)' "$sidecar"; then
      fail "model-invoked skill must omit the Codex policy block: $sidecar"
    fi
  fi
done <"$tmp_dir/skills"

echo "skill registry checks passed"
