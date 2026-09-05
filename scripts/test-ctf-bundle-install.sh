#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

assert_file() {
  [[ -f "$1" ]] || fail "missing file: $1"
}

assert_absent() {
  [[ ! -e "$1" ]] || fail "unexpected path: $1"
}

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

skill_names=(
  ctf-ai-ml ctf-crypto ctf-forensics ctf-malware ctf-misc ctf-osint
  ctf-pwn ctf-reverse ctf-web ctf-writeup solve-challenge
)

ctf_fixture="$tmp_dir/ctf-fixture/ctf-skills-d6662d2"
for name in "${skill_names[@]}"; do
  mkdir -p "$ctf_fixture/$name"
  printf '%s\n' '---' "name: $name" "description: Fixture for $name." '---' >"$ctf_fixture/$name/SKILL.md"
done
mkdir -p "$ctf_fixture/ctf-web/references"
printf '%s\n' 'nested fixture' >"$ctf_fixture/ctf-web/references/example.md"
printf '%s\n' '#!/usr/bin/env bash' 'touch "$CTF_TOOL_MARKER"' >"$ctf_fixture/install-tools.sh"
tar -czf "$tmp_dir/ctf.tar.gz" -C "$tmp_dir/ctf-fixture" ctf-skills-d6662d2

bad_fixture="$tmp_dir/bad-ctf/ctf-skills-d6662d2"
mkdir -p "$tmp_dir/bad-ctf"
cp -R "$ctf_fixture" "$bad_fixture"
rm "$bad_fixture/ctf-ai-ml/SKILL.md"
tar -czf "$tmp_dir/bad-ctf.tar.gz" -C "$tmp_dir/bad-ctf" ctf-skills-d6662d2

forge_fixture="$tmp_dir/forge-fixture/Agent-Skill-Forge-master"
mkdir -p "$forge_fixture/scripts" "$forge_fixture/bundles" "$forge_fixture/skills/engineering/core-fixture/agents"
cp scripts/install.sh "$forge_fixture/scripts/install.sh"
cp bundles/ctf-skills.lock.json "$forge_fixture/bundles/ctf-skills.lock.json"
printf '%s\n' '---' 'name: core-fixture' 'description: Core fixture.' '---' >"$forge_fixture/skills/engineering/core-fixture/SKILL.md"
printf '%s\n' 'interface:' '  display_name: "Core Fixture"' '  short_description: "Install a core fixture skill"' >"$forge_fixture/skills/engineering/core-fixture/agents/openai.yaml"
tar -czf "$tmp_dir/forge.tar.gz" -C "$tmp_dir/forge-fixture" Agent-Skill-Forge-master

mkdir -p "$tmp_dir/fake-bin"
cat >"$tmp_dir/fake-bin/curl" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

output=""
url=""
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    -o) output="$2"; shift 2 ;;
    -*) shift ;;
    *) url="$1"; shift ;;
  esac
done

[[ -n "$output" && -n "$url" ]]
case "$url" in
  *Agent-Skill-Forge*) cp "$FAKE_FORGE_ARCHIVE" "$output" ;;
  *ctf-skills*) cp "$FAKE_CTF_ARCHIVE" "$output" ;;
  *) exit 1 ;;
esac
EOF
chmod +x "$tmp_dir/fake-bin/curl"

common_path="$tmp_dir/fake-bin:$PATH"
home="$tmp_dir/home"
mkdir -p "$home/.agents/skills/unrelated"
printf '%s\n' 'keep' >"$home/.agents/skills/unrelated/marker"
for retired in grill-me grill-with-docs evidence-first ponytail; do
  mkdir -p "$home/.agents/skills/$retired"
  printf '%s\n' 'old skill' >"$home/.agents/skills/$retired/SKILL.md"
done

PATH="$common_path" FAKE_CTF_ARCHIVE="$tmp_dir/ctf.tar.gz" FAKE_FORGE_ARCHIVE="$tmp_dir/forge.tar.gz" \
  CTF_TOOL_MARKER="$tmp_dir/tool-ran" HOME="$home" bash scripts/install-with-ctf.sh >"$tmp_dir/install.out"

assert_file "$home/.agents/skills/teach/SKILL.md"
assert_file "$home/.agents/skills/unrelated/marker"
assert_file "$home/.agents/skills/ctf-web/references/example.md"
assert_file "$home/.agents/skill-sources/agent-skill-forge/ctf-skills.json"
assert_absent "$tmp_dir/tool-ran"
for retired in grill-me grill-with-docs evidence-first ponytail; do
  assert_absent "$home/.agents/skills/$retired"
done
if compgen -G "$home/.agents/skills/.ctf-skills-stage.*" >/dev/null; then
  fail "installer left a staging directory"
fi
if compgen -G "$home/.agents/skill-sources/agent-skill-forge/.ctf-skills.*" >/dev/null; then
  fail "installer left a receipt temporary file"
fi
for name in "${skill_names[@]}"; do
  assert_file "$home/.agents/skills/$name/SKILL.md"
done

printf '%s\n' 'stale' >"$home/.agents/skills/ctf-web/stale"
PATH="$common_path" FAKE_CTF_ARCHIVE="$tmp_dir/ctf.tar.gz" FAKE_FORGE_ARCHIVE="$tmp_dir/forge.tar.gz" \
  HOME="$home" bash scripts/install-with-ctf.sh >"$tmp_dir/reinstall.out"
assert_absent "$home/.agents/skills/ctf-web/stale"

rollback_home="$tmp_dir/rollback-home"
cp -R "$home" "$rollback_home"
printf '%s\n' 'old ai content' >"$rollback_home/.agents/skills/ctf-ai-ml/rollback-marker"
printf '%s\n' 'old crypto content' >"$rollback_home/.agents/skills/ctf-crypto/rollback-marker"
cp "$rollback_home/.agents/skill-sources/agent-skill-forge/ctf-skills.json" "$tmp_dir/rollback-receipt-before.json"
mkdir -p "$tmp_dir/fail-bin"
real_mv="$(command -v mv)"
cat >"$tmp_dir/fail-bin/mv" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

if [[ "$1" == */.ctf-skills-stage.*/ctf-crypto ]]; then
  exit 70
fi
exec "$REAL_MV" "$@"
EOF
chmod +x "$tmp_dir/fail-bin/mv"
if PATH="$tmp_dir/fail-bin:$common_path" REAL_MV="$real_mv" FAKE_CTF_ARCHIVE="$tmp_dir/ctf.tar.gz" \
  FAKE_FORGE_ARCHIVE="$tmp_dir/forge.tar.gz" HOME="$rollback_home" \
  bash scripts/install-with-ctf.sh >"$tmp_dir/rollback.out" 2>&1; then
  fail "installer ignored an external install failure"
fi
assert_file "$rollback_home/.agents/skills/ctf-ai-ml/rollback-marker"
assert_file "$rollback_home/.agents/skills/ctf-crypto/rollback-marker"
cmp -s "$tmp_dir/rollback-receipt-before.json" \
  "$rollback_home/.agents/skill-sources/agent-skill-forge/ctf-skills.json" || fail "rollback changed the receipt"
if compgen -G "$rollback_home/.agents/skills/.ctf-skills-stage.*" >/dev/null; then
  fail "rollback left a staging directory"
fi

collision_home="$tmp_dir/collision-home"
mkdir -p "$collision_home/.agents/skills/ctf-web"
printf '%s\n' 'owned elsewhere' >"$collision_home/.agents/skills/ctf-web/marker"
if PATH="$common_path" FAKE_CTF_ARCHIVE="$tmp_dir/ctf.tar.gz" FAKE_FORGE_ARCHIVE="$tmp_dir/forge.tar.gz" \
  HOME="$collision_home" bash scripts/install-with-ctf.sh >"$tmp_dir/collision.out" 2>&1; then
  fail "installer replaced an unowned skill directory"
fi
assert_file "$collision_home/.agents/skills/ctf-web/marker"
assert_absent "$collision_home/.agents/skills/teach"

bad_home="$tmp_dir/bad-home"
if PATH="$common_path" FAKE_CTF_ARCHIVE="$tmp_dir/bad-ctf.tar.gz" FAKE_FORGE_ARCHIVE="$tmp_dir/forge.tar.gz" \
  HOME="$bad_home" bash scripts/install-with-ctf.sh >"$tmp_dir/bad.out" 2>&1; then
  fail "installer accepted a bundle with a missing SKILL.md"
fi
assert_absent "$bad_home/.agents/skills/teach"

mkdir -p "$tmp_dir/standalone"
cp scripts/install-with-ctf.sh "$tmp_dir/standalone/install-with-ctf.sh"
standalone_home="$tmp_dir/standalone-home"
PATH="$common_path" FAKE_CTF_ARCHIVE="$tmp_dir/ctf.tar.gz" FAKE_FORGE_ARCHIVE="$tmp_dir/forge.tar.gz" \
  HOME="$standalone_home" bash "$tmp_dir/standalone/install-with-ctf.sh" >"$tmp_dir/standalone.out"
assert_file "$standalone_home/.agents/skills/core-fixture/SKILL.md"
assert_file "$standalone_home/.agents/skills/solve-challenge/SKILL.md"

echo "CTF bundle install tests passed"
