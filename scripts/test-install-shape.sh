#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

assert_file() {
  [[ -f "$1" ]] || fail "expected file: $1"
}

assert_contains() {
  local pattern="$1"
  local file="$2"
  rg -Fq "$pattern" "$file" || fail "expected '$pattern' in $file"
}

assert_not_contains() {
  local pattern="$1"
  local file="$2"
  if rg -Fq "$pattern" "$file"; then
    fail "did not expect '$pattern' in $file"
  fi
}

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

assert_contains 'https://codeload.github.com/${owner}/${repo}/tar.gz/refs/heads/${ref}' scripts/install.sh
assert_contains 'raw.githubusercontent.com/charSLee013/Agent-Skill-Forge/master/scripts/install.sh' README.md
assert_not_contains 'retired_skill_names' scripts/install.sh
assert_not_contains 'AGENT=codex' README.md
assert_not_contains 'bash scripts/install.sh teach' README.md

home="$tmp_dir/home"
mkdir -p "$home/.agents/skills/ask-skills" "$home/.agents/skills/user-custom"
printf 'keep me\n' >"$home/.agents/skills/ask-skills/marker.txt"
printf 'keep me\n' >"$home/.agents/skills/user-custom/marker.txt"
mkdir -p "$home/.agents/skills/teach"
printf 'stale\n' >"$home/.agents/skills/teach/stale.txt"

AGENT=codex HOME="$home" bash scripts/install.sh >"$tmp_dir/install.out"

assert_contains 'Installing ' "$tmp_dir/install.out"
assert_contains 'Done.' "$tmp_dir/install.out"
assert_file "$home/.agents/skills/teach/SKILL.md"
assert_file "$home/.agents/skills/handoff/SKILL.md"
if [[ -e "$home/.agents/skills/teach/stale.txt" ]]; then
  fail "current skill directory was not replaced"
fi
assert_file "$home/.agents/skills/ask-skills/marker.txt"
assert_file "$home/.agents/skills/user-custom/marker.txt"

while IFS= read -r skill_md; do
  skill_name="$(basename "$(dirname "$skill_md")")"
  assert_file "$home/.agents/skills/$skill_name/SKILL.md"
done < <(find skills -name SKILL.md -not -path '*/node_modules/*' -print | sort)

if HOME="$tmp_dir/with-args" bash scripts/install.sh teach >"$tmp_dir/args.out" 2>"$tmp_dir/args.err"; then
  fail "install accepted a skill-selection argument"
fi
assert_contains 'install.sh takes no arguments' "$tmp_dir/args.err"

fixture_root="$tmp_dir/fixture/Agent-Skill-Forge-master"
mkdir -p "$fixture_root/skills/engineering/remote-fixture"
printf '%s\n' '---' 'name: remote-fixture' 'description: Remote installer fixture.' '---' >"$fixture_root/skills/engineering/remote-fixture/SKILL.md"
tar -czf "$tmp_dir/fixture.tar.gz" -C "$tmp_dir/fixture" Agent-Skill-Forge-master

mkdir -p "$tmp_dir/fake-bin" "$tmp_dir/standalone"
cp scripts/install.sh "$tmp_dir/standalone/install.sh"
cat >"$tmp_dir/fake-bin/curl" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

output=""
while [[ "$#" -gt 0 ]]; do
  if [[ "$1" == "-o" ]]; then
    output="$2"
    shift 2
  else
    shift
  fi
done

[[ -n "$output" ]]
cp "$FAKE_ARCHIVE" "$output"
EOF
chmod +x "$tmp_dir/fake-bin/curl"

PATH="$tmp_dir/fake-bin:$PATH" FAKE_ARCHIVE="$tmp_dir/fixture.tar.gz" HOME="$tmp_dir/remote-home" \
  bash "$tmp_dir/standalone/install.sh" >"$tmp_dir/remote.out" 2>&1
assert_file "$tmp_dir/remote-home/.agents/skills/remote-fixture/SKILL.md"
assert_contains 'Local skills directory not found.' "$tmp_dir/remote.out"

HOME="$tmp_dir/idempotent" bash scripts/install.sh >"$tmp_dir/idempotent-1.out"
find "$tmp_dir/idempotent/.agents/skills" -type f -print | sed "s#^$tmp_dir/idempotent/.agents/skills/##" | sort >"$tmp_dir/files-1"
HOME="$tmp_dir/idempotent" bash scripts/install.sh >"$tmp_dir/idempotent-2.out"
find "$tmp_dir/idempotent/.agents/skills" -type f -print | sed "s#^$tmp_dir/idempotent/.agents/skills/##" | sort >"$tmp_dir/files-2"
cmp "$tmp_dir/files-1" "$tmp_dir/files-2" >/dev/null || fail "install is not idempotent"

echo "install shape tests passed"
