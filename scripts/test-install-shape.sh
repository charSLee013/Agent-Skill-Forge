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
assert_contains '~/.agents/agent-skill-forge/' README.md
assert_contains 'runtime_dest="$agents_root/agent-skill-forge"' scripts/install.sh

runtime_files=(
  "hooks/hooks.json"
  "hooks/checkpoint.py"
  "hooks/issue_gate.py"
  "scripts/finalize-issue.py"
  "scripts/delegation.py"
)

for relative_path in "${runtime_files[@]}"; do
  assert_file "$relative_path"
done

home="$tmp_dir/home"
mkdir -p "$home/.agents/skills/ask-skills" "$home/.agents/skills/user-custom"
printf 'keep me\n' >"$home/.agents/skills/ask-skills/marker.txt"
printf 'keep me\n' >"$home/.agents/skills/user-custom/marker.txt"
mkdir -p "$home/.agents/skills/teach"
printf 'stale\n' >"$home/.agents/skills/teach/stale.txt"
mkdir -p "$home/.agents/agent-skill-forge/obsolete"
printf 'stale\n' >"$home/.agents/agent-skill-forge/obsolete/debug.txt"

HOME="$home" bash scripts/install.sh >"$tmp_dir/install.out"

assert_contains 'Installing ' "$tmp_dir/install.out"
assert_contains 'Installing execution-reliability support:' "$tmp_dir/install.out"
assert_contains 'Done.' "$tmp_dir/install.out"
assert_file "$home/.agents/skills/teach/SKILL.md"
assert_file "$home/.agents/skills/handoff/SKILL.md"
if [[ -e "$home/.agents/skills/teach/stale.txt" ]]; then
  fail "current skill directory was not replaced"
fi
assert_file "$home/.agents/skills/ask-skills/marker.txt"
assert_file "$home/.agents/skills/user-custom/marker.txt"
if [[ -e "$home/.agents/agent-skill-forge/obsolete" ]]; then
  fail "runtime support bundle retained stale files"
fi

for relative_path in "${runtime_files[@]}"; do
  assert_file "$home/.agents/agent-skill-forge/$relative_path"
  cmp "$relative_path" "$home/.agents/agent-skill-forge/$relative_path" >/dev/null || \
    fail "installed runtime support differs: $relative_path"
done

printf '%s\n' "${runtime_files[@]}" | sort >"$tmp_dir/runtime-expected"
find "$home/.agents/agent-skill-forge" -type f -print | \
  sed "s#^$home/.agents/agent-skill-forge/##" | sort >"$tmp_dir/runtime-actual"
cmp "$tmp_dir/runtime-expected" "$tmp_dir/runtime-actual" >/dev/null || \
  fail "runtime support bundle contains an unexpected file"
if find "$home/.agents" -maxdepth 1 -name '.agent-skill-forge-stage.*' -print | rg -q .; then
  fail "runtime support install left a staging directory"
fi

for executable_path in \
  hooks/checkpoint.py \
  hooks/issue_gate.py \
  scripts/finalize-issue.py \
  scripts/delegation.py; do
  [[ -x "$home/.agents/agent-skill-forge/$executable_path" ]] || \
    fail "installed runtime entrypoint is not executable: $executable_path"
done

while IFS= read -r skill_md; do
  skill_name="$(basename "$(dirname "$skill_md")")"
  assert_file "$home/.agents/skills/$skill_name/SKILL.md"
done < <(find skills -name SKILL.md -not -path '*/node_modules/*' -print | sort)

if HOME="$tmp_dir/with-args" bash scripts/install.sh teach >"$tmp_dir/args.out" 2>"$tmp_dir/args.err"; then
  fail "install accepted a skill-selection argument"
fi
assert_contains 'install.sh takes no arguments' "$tmp_dir/args.err"

fixture_root="$tmp_dir/fixture/Agent-Skill-Forge-master"
mkdir -p \
  "$fixture_root/skills/engineering/remote-fixture" \
  "$fixture_root/hooks" \
  "$fixture_root/scripts"
printf '%s\n' '---' 'name: remote-fixture' 'description: Remote installer fixture.' '---' >"$fixture_root/skills/engineering/remote-fixture/SKILL.md"
printf '{}\n' >"$fixture_root/hooks/hooks.json"
printf '#!/usr/bin/env python3\n' >"$fixture_root/hooks/checkpoint.py"
printf '#!/usr/bin/env python3\n' >"$fixture_root/hooks/issue_gate.py"
printf '#!/usr/bin/env python3\n' >"$fixture_root/scripts/finalize-issue.py"
printf '#!/usr/bin/env python3\n' >"$fixture_root/scripts/delegation.py"
chmod +x \
  "$fixture_root/hooks/checkpoint.py" \
  "$fixture_root/hooks/issue_gate.py" \
  "$fixture_root/scripts/finalize-issue.py" \
  "$fixture_root/scripts/delegation.py"
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
for relative_path in "${runtime_files[@]}"; do
  assert_file "$tmp_dir/remote-home/.agents/agent-skill-forge/$relative_path"
done

consumer="$tmp_dir/consumer"
mkdir -p "$consumer/.codex/agents/runtime"
cp -R "$home/.agents/agent-skill-forge" "$consumer/.codex/agents/runtime/support"
python3 "$consumer/.codex/agents/runtime/support/scripts/finalize-issue.py" --help >"$tmp_dir/finalize-help.out"
python3 "$consumer/.codex/agents/runtime/support/scripts/delegation.py" --help >"$tmp_dir/delegation-help.out"
assert_contains 'Baseline-aware finalization for local implementation issues.' "$tmp_dir/finalize-help.out"
assert_contains 'Manage the temporary REQUEST.md and RESULT.md delegation protocol.' "$tmp_dir/delegation-help.out"

session_id="00000000-0000-4000-8000-000000000004"
printf '{"hook_event_name":"SessionStart","source":"startup","session_id":"%s","cwd":"%s"}\n' \
  "$session_id" "$consumer" | \
  python3 "$consumer/.codex/agents/runtime/support/hooks/checkpoint.py" >"$tmp_dir/checkpoint.out"
assert_contains "$consumer/.codex/agents/runtime/checkpoints/$session_id.md" "$tmp_dir/checkpoint.out"

HOME="$tmp_dir/idempotent" bash scripts/install.sh >"$tmp_dir/idempotent-1.out"
find "$tmp_dir/idempotent/.agents" -type f -print | sed "s#^$tmp_dir/idempotent/.agents/##" | sort >"$tmp_dir/files-1"
HOME="$tmp_dir/idempotent" bash scripts/install.sh >"$tmp_dir/idempotent-2.out"
find "$tmp_dir/idempotent/.agents" -type f -print | sed "s#^$tmp_dir/idempotent/.agents/##" | sort >"$tmp_dir/files-2"
cmp "$tmp_dir/files-1" "$tmp_dir/files-2" >/dev/null || fail "install is not idempotent"
for relative_path in "${runtime_files[@]}"; do
  cmp "$relative_path" "$tmp_dir/idempotent/.agents/agent-skill-forge/$relative_path" >/dev/null || \
    fail "idempotent install changed runtime support: $relative_path"
done

echo "install shape tests passed"
