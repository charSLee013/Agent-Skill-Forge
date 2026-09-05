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

assert_absent() {
  [[ ! -e "$1" && ! -L "$1" ]] || fail "unexpected path: $1"
}

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

home="$tmp_dir/home"
mkdir -p "$home/.agents/skills/external-skill" "$home/.agents/skills/user-custom"
printf 'keep me\n' >"$home/.agents/skills/external-skill/marker.txt"
printf 'keep me\n' >"$home/.agents/skills/user-custom/marker.txt"
mkdir -p "$home/.agents/skills/teach"
printf 'stale\n' >"$home/.agents/skills/teach/stale.txt"

for name in grill-me grill-with-docs evidence-first; do
  mkdir -p "$home/.agents/skills/$name"
  printf 'user-modified old skill\n' >"$home/.agents/skills/$name/SKILL.md"
done
mkdir -p "$tmp_dir/symlink-target"
printf 'preserve link target\n' >"$tmp_dir/symlink-target/marker"
ln -s "$tmp_dir/symlink-target" "$home/.agents/skills/ponytail"

HOME="$home" bash scripts/install.sh >"$tmp_dir/install.out"

assert_file "$home/.agents/skills/teach/SKILL.md"
assert_file "$home/.agents/skills/handoff/SKILL.md"
if [[ -e "$home/.agents/skills/teach/stale.txt" ]]; then
  fail "current skill directory was not replaced"
fi
assert_file "$home/.agents/skills/external-skill/marker.txt"
assert_file "$home/.agents/skills/user-custom/marker.txt"
assert_file "$tmp_dir/symlink-target/marker"
for name in grill-me grill-with-docs evidence-first ponytail; do
  assert_absent "$home/.agents/skills/$name"
done

for resource in grilling/references/communication.md implement/references/evidence.md implement/LICENSE; do
  assert_file "$home/.agents/skills/$resource"
done
cmp skills/productivity/grilling/references/communication.md \
  "$home/.agents/skills/grilling/references/communication.md" || fail "communication reference changed during install"
cmp skills/engineering/implement/references/evidence.md \
  "$home/.agents/skills/implement/references/evidence.md" || fail "evidence reference changed during install"

find skills -name SKILL.md -not -path '*/node_modules/*' -print \
  | sed -E 's#^.*/([^/]+)/SKILL.md$#\1#' >"$tmp_dir/expected-dirs"
printf '%s\n' external-skill user-custom >>"$tmp_dir/expected-dirs"
sort -o "$tmp_dir/expected-dirs" "$tmp_dir/expected-dirs"
find "$home/.agents/skills" -mindepth 1 -maxdepth 1 -print \
  | sed 's#^.*/##' | sort >"$tmp_dir/installed-dirs"
cmp "$tmp_dir/expected-dirs" "$tmp_dir/installed-dirs" || fail "install left an alias, backup, or unexpected entry"

while IFS= read -r skill_md; do
  skill_name="$(basename "$(dirname "$skill_md")")"
  assert_file "$home/.agents/skills/$skill_name/SKILL.md"
  assert_file "$home/.agents/skills/$skill_name/agents/openai.yaml"
done < <(find skills -name SKILL.md -not -path '*/node_modules/*' -print | sort)

if HOME="$tmp_dir/with-args" bash scripts/install.sh teach >"$tmp_dir/args.out" 2>"$tmp_dir/args.err"; then
  fail "install accepted a skill-selection argument"
fi

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

mkdir -p "$tmp_dir/remote-home/.agents/skills/grill-me"
ln -s "$tmp_dir/missing-target" "$tmp_dir/remote-home/.agents/skills/ponytail"
PATH="$tmp_dir/fake-bin:$PATH" FAKE_ARCHIVE="$tmp_dir/fixture.tar.gz" HOME="$tmp_dir/remote-home" \
  bash "$tmp_dir/standalone/install.sh" >"$tmp_dir/remote-upgrade.out" 2>&1
assert_absent "$tmp_dir/remote-home/.agents/skills/grill-me"
assert_absent "$tmp_dir/remote-home/.agents/skills/ponytail"

mkdir -p "$tmp_dir/copy-fail-bin"
for name in grill-me grill-with-docs evidence-first ponytail; do
  mkdir -p "$home/.agents/skills/$name"
  printf 'preserve until replacement succeeds\n' >"$home/.agents/skills/$name/SKILL.md"
done
real_cp="$(command -v cp)"
cat >"$tmp_dir/copy-fail-bin/cp" <<'EOF'
#!/usr/bin/env bash
if [[ "${!#}" == "$COPY_FAILURE_PATH" ]]; then
  exit 72
fi
exec "$REAL_CP" "$@"
EOF
chmod +x "$tmp_dir/copy-fail-bin/cp"
if PATH="$tmp_dir/copy-fail-bin:$PATH" REAL_CP="$real_cp" \
  COPY_FAILURE_PATH="$home/.agents/skills/implement" HOME="$home" \
  bash scripts/install.sh >"$tmp_dir/copy-failure.out" 2>&1; then
  fail "installer ignored a replacement failure"
fi
for name in grill-me grill-with-docs evidence-first ponytail; do
  assert_file "$home/.agents/skills/$name/SKILL.md"
done
if rg -q '^Done\.$' "$tmp_dir/copy-failure.out"; then
  fail "installer reported success after replacement failed"
fi

mkdir -p "$tmp_dir/fail-bin" "$home/.agents/skills/ponytail"
printf 'retirement failure fixture\n' >"$home/.agents/skills/ponytail/SKILL.md"
real_rm="$(command -v rm)"
cat >"$tmp_dir/fail-bin/rm" <<'EOF'
#!/usr/bin/env bash
if [[ "${!#}" == "$RETIREMENT_FAILURE_PATH" ]]; then
  exit 71
fi
exec "$REAL_RM" "$@"
EOF
chmod +x "$tmp_dir/fail-bin/rm"
if PATH="$tmp_dir/fail-bin:$PATH" REAL_RM="$real_rm" \
  RETIREMENT_FAILURE_PATH="$home/.agents/skills/ponytail" HOME="$home" \
  bash scripts/install.sh >"$tmp_dir/retirement-failure.out" 2>&1; then
  fail "installer ignored a retirement failure"
fi
assert_file "$home/.agents/skills/ponytail/SKILL.md"
if rg -q '^Done\.$' "$tmp_dir/retirement-failure.out"; then
  fail "installer reported success after retirement failed"
fi
HOME="$home" bash scripts/install.sh >"$tmp_dir/recover.out"
assert_absent "$home/.agents/skills/ponytail"

HOME="$tmp_dir/idempotent" bash scripts/install.sh >"$tmp_dir/idempotent-1.out"
find "$tmp_dir/idempotent/.agents/skills" -type f -print | sed "s#^$tmp_dir/idempotent/.agents/skills/##" | sort >"$tmp_dir/files-1"
HOME="$tmp_dir/idempotent" bash scripts/install.sh >"$tmp_dir/idempotent-2.out"
find "$tmp_dir/idempotent/.agents/skills" -type f -print | sed "s#^$tmp_dir/idempotent/.agents/skills/##" | sort >"$tmp_dir/files-2"
cmp "$tmp_dir/files-1" "$tmp_dir/files-2" >/dev/null || fail "install is not idempotent"

echo "install shape tests passed"
