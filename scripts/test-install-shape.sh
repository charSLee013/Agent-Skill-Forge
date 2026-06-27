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
  rg -q "$pattern" "$file" || fail "expected '$pattern' in $file"
}

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

bash scripts/install.sh --help >"$tmp_dir/help.out"
assert_contains 'Usage:' "$tmp_dir/help.out"
assert_contains 'Default:' "$tmp_dir/help.out"
assert_contains 'Supported AGENT values:' "$tmp_dir/help.out"
assert_contains 'Available skills:' "$tmp_dir/help.out"
assert_contains 'raw.githubusercontent.com/charSLee013/Agent-Skill-Forge/master/scripts/install.sh' "$tmp_dir/help.out"
assert_contains 'teach' "$tmp_dir/help.out"

HOME="$tmp_dir/home-default" bash scripts/install.sh >"$tmp_dir/default.out"
assert_file "$tmp_dir/home-default/.agents/skills/teach/SKILL.md"
assert_file "$tmp_dir/home-default/.agents/skills/handoff/SKILL.md"
assert_contains 'Installing ' "$tmp_dir/default.out"
assert_contains 'Done\.' "$tmp_dir/default.out"

HOME="$tmp_dir/home-selective" bash scripts/install.sh teach handoff >"$tmp_dir/selective.out"
assert_file "$tmp_dir/home-selective/.agents/skills/teach/SKILL.md"
assert_file "$tmp_dir/home-selective/.agents/skills/handoff/SKILL.md"
if [[ -e "$tmp_dir/home-selective/.agents/skills/grill-me" ]]; then
  fail "selective install unexpectedly installed grill-me"
fi

for agent in codex claude opencode agents; do
  home="$tmp_dir/home-$agent"
  AGENT="$agent" HOME="$home" CODEX_HOME="$home/.codex" bash scripts/install.sh teach >"$tmp_dir/$agent.out"

  case "$agent" in
    codex)
      dest="$home/.codex/skills/teach"
      ;;
    claude)
      dest="$home/.claude/skills/teach"
      ;;
    opencode)
      dest="$home/.config/opencode/skills/teach"
      ;;
    agents)
      dest="$home/.agents/skills/teach"
      ;;
  esac

  assert_file "$dest/SKILL.md"
done

HOME="$tmp_dir/home-idempotent" bash scripts/install.sh teach >"$tmp_dir/idempotent-1.out"
dest="$tmp_dir/home-idempotent/.agents/skills/teach"
find "$dest" -type f -print | sed "s#^$dest/##" | sort >"$tmp_dir/files-1"
HOME="$tmp_dir/home-idempotent" bash scripts/install.sh teach >"$tmp_dir/idempotent-2.out"
find "$dest" -type f -print | sed "s#^$dest/##" | sort >"$tmp_dir/files-2"
cmp "$tmp_dir/files-1" "$tmp_dir/files-2" >/dev/null || fail "install is not idempotent"

if HOME="$tmp_dir/home-unknown" bash scripts/install.sh not-a-skill >"$tmp_dir/unknown.out" 2>"$tmp_dir/unknown.err"; then
  fail "unknown skill unexpectedly succeeded"
fi
assert_contains "unknown skill 'not-a-skill'" "$tmp_dir/unknown.err"
assert_contains "Available skills:" "$tmp_dir/unknown.err"
assert_contains "Usage:" "$tmp_dir/unknown.err"

if AGENT=unknown HOME="$tmp_dir/home-agent" bash scripts/install.sh teach >"$tmp_dir/bad-agent.out" 2>"$tmp_dir/bad-agent.err"; then
  fail "unknown AGENT unexpectedly succeeded"
fi
assert_contains "unsupported AGENT 'unknown'" "$tmp_dir/bad-agent.err"
assert_contains "Supported AGENT values:" "$tmp_dir/bad-agent.err"
assert_contains "Usage:" "$tmp_dir/bad-agent.err"

assert_contains 'github.com/charSLee013/Agent-Skill-Forge' README.md
assert_contains 'raw.githubusercontent.com/charSLee013/Agent-Skill-Forge/master/scripts/install.sh' README.md

echo "install shape tests passed"
