#!/usr/bin/env bash
set -euo pipefail

forge_owner="charSLee013"
forge_repo="Agent-Skill-Forge"
forge_ref="master"
expected_ctf_repository="https://github.com/ljagiello/ctf-skills"
tmp_dir="$(mktemp -d)"
transaction_active=false
dest_root=""
backup_root=""
dest_stage=""
receipt_dir=""
receipt_tmp=""
declare -a skill_names=()
declare -a installed_names=()

if [[ "$#" -ne 0 ]]; then
  echo "error: install-with-ctf.sh takes no arguments" >&2
  echo "Usage: bash scripts/install-with-ctf.sh" >&2
  exit 2
fi

contains_name() {
  local wanted="$1"
  shift
  local candidate
  for candidate in "$@"; do
    [[ "$candidate" == "$wanted" ]] && return 0
  done
  return 1
}

rollback_external() {
  local name
  set +e
  for name in "${installed_names[@]}"; do
    rm -rf "$dest_root/$name"
  done
  for name in "${skill_names[@]}"; do
    if [[ -e "$backup_root/$name" ]]; then
      mv "$backup_root/$name" "$dest_root/$name"
    fi
  done
  set -e
}

cleanup() {
  if [[ "$transaction_active" == true ]]; then
    rollback_external
  fi
  if [[ -n "$dest_stage" && "$dest_stage" == "$dest_root"/.ctf-skills-stage.* ]]; then
    rm -rf "$dest_stage"
  fi
  if [[ -n "$receipt_tmp" && "$receipt_tmp" == "$receipt_dir"/.ctf-skills.* ]]; then
    rm -f "$receipt_tmp"
  fi
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

command -v python3 >/dev/null || {
  echo "error: python3 is required to read the bundle lock" >&2
  exit 1
}

script_source="${BASH_SOURCE[0]-}"
repo_root=""
if [[ -n "$script_source" ]]; then
  candidate_root="$(cd "$(dirname "$script_source")/.." 2>/dev/null && pwd || true)"
  if [[ -d "$candidate_root/skills" && -f "$candidate_root/scripts/install.sh" && -f "$candidate_root/bundles/ctf-skills.lock.json" ]]; then
    repo_root="$candidate_root"
  fi
fi

if [[ -z "$repo_root" ]]; then
  forge_archive="$tmp_dir/agent-skill-forge.tar.gz"
  forge_url="https://codeload.github.com/${forge_owner}/${forge_repo}/tar.gz/refs/heads/${forge_ref}"

  echo "Local bundle files not found. Downloading ${forge_owner}/${forge_repo}@${forge_ref}..." >&2
  curl -fsSL "$forge_url" -o "$forge_archive"
  mkdir -p "$tmp_dir/forge"
  tar -xzf "$forge_archive" -C "$tmp_dir/forge"
  repo_root="$(find "$tmp_dir/forge" -mindepth 1 -maxdepth 1 -type d | head -n1)"

  if [[ -z "$repo_root" || ! -d "$repo_root/skills" || ! -f "$repo_root/scripts/install.sh" || ! -f "$repo_root/bundles/ctf-skills.lock.json" ]]; then
    echo "error: downloaded repository does not contain the bundle installer files" >&2
    exit 1
  fi
fi

lock_file="$repo_root/bundles/ctf-skills.lock.json"
lock_records="$tmp_dir/lock-records"
python3 - "$lock_file" >"$lock_records" <<'PY'
import json
import re
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    lock = json.load(handle)

required = {"schema_version", "name", "repository", "commit", "license", "skills"}
if set(lock) != required:
    raise SystemExit("bundle lock has unexpected fields")
if lock["schema_version"] != 1 or lock["name"] != "ctf-skills" or lock["license"] != "MIT":
    raise SystemExit("bundle lock metadata is invalid")
if not re.fullmatch(r"[0-9a-f]{40}", lock["commit"]):
    raise SystemExit("bundle lock commit is invalid")
if not isinstance(lock["skills"], list) or not lock["skills"] or len(lock["skills"]) != len(set(lock["skills"])):
    raise SystemExit("bundle lock skills must be a non-empty unique list")
if not all(isinstance(name, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]*", name) for name in lock["skills"]):
    raise SystemExit("bundle lock contains an invalid skill name")

print("repository\t" + lock["repository"])
print("commit\t" + lock["commit"])
for name in lock["skills"]:
    print("skill\t" + name)
PY

ctf_repository=""
ctf_commit=""
while IFS=$'\t' read -r kind value; do
  case "$kind" in
    repository) ctf_repository="$value" ;;
    commit) ctf_commit="$value" ;;
    skill) skill_names+=("$value") ;;
  esac
done <"$lock_records"

if [[ "$ctf_repository" != "$expected_ctf_repository" || ! "$ctf_commit" =~ ^[0-9a-f]{40}$ || "${#skill_names[@]}" -eq 0 ]]; then
  echo "error: unsupported CTF bundle lock" >&2
  exit 1
fi

while IFS= read -r core_skill_md; do
  core_name="$(basename "$(dirname "$core_skill_md")")"
  if contains_name "$core_name" "${skill_names[@]}"; then
    echo "error: CTF bundle skill collides with a core skill: $core_name" >&2
    exit 1
  fi
done < <(find "$repo_root/skills" -name SKILL.md -not -path '*/node_modules/*' -print | sort)

ctf_archive="$tmp_dir/ctf-skills.tar.gz"
ctf_url="https://codeload.github.com/ljagiello/ctf-skills/tar.gz/${ctf_commit}"
curl -fsSL "$ctf_url" -o "$ctf_archive"
mkdir -p "$tmp_dir/ctf-source"
tar -xzf "$ctf_archive" -C "$tmp_dir/ctf-source"
ctf_root="$(find "$tmp_dir/ctf-source" -mindepth 1 -maxdepth 1 -type d | head -n1)"

if [[ -z "$ctf_root" ]]; then
  echo "error: downloaded CTF archive is empty" >&2
  exit 1
fi

staged_root="$tmp_dir/staged"
mkdir -p "$staged_root"
for name in "${skill_names[@]}"; do
  if [[ ! -f "$ctf_root/$name/SKILL.md" ]]; then
    echo "error: locked CTF skill is missing SKILL.md: $name" >&2
    exit 1
  fi
  cp -R "$ctf_root/$name" "$staged_root/$name"
done

dest_root="$HOME/.agents/skills"
receipt_dir="$HOME/.agents/skill-sources/agent-skill-forge"
receipt_file="$receipt_dir/ctf-skills.json"
declare -a owned_names=()

if [[ -f "$receipt_file" ]]; then
  owned_records="$tmp_dir/owned-records"
  python3 - "$receipt_file" "$expected_ctf_repository" >"$owned_records" <<'PY'
import json
import re
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    receipt = json.load(handle)
if receipt.get("repository") != sys.argv[2]:
    raise SystemExit("existing CTF bundle receipt has a different repository")
skills = receipt.get("skills")
if not isinstance(skills, list) or not all(isinstance(name, str) and re.fullmatch(r"[a-z0-9][a-z0-9-]*", name) for name in skills):
    raise SystemExit("existing CTF bundle receipt is invalid")
for name in skills:
    print(name)
PY
  while IFS= read -r name; do
    owned_names+=("$name")
  done <"$owned_records"
fi

for name in "${skill_names[@]}"; do
  if [[ -e "$dest_root/$name" ]] && ! contains_name "$name" "${owned_names[@]}"; then
    echo "error: refusing to replace unowned skill directory: $dest_root/$name" >&2
    exit 1
  fi
done

bash "$repo_root/scripts/install.sh"

mkdir -p "$dest_root" "$receipt_dir"
dest_stage="$(mktemp -d "$dest_root/.ctf-skills-stage.XXXXXX")"
for name in "${skill_names[@]}"; do
  cp -R "$staged_root/$name" "$dest_stage/$name"
done

backup_root="$tmp_dir/backups"
mkdir -p "$backup_root"
transaction_active=true

for name in "${skill_names[@]}"; do
  if [[ -e "$dest_root/$name" ]]; then
    mv "$dest_root/$name" "$backup_root/$name"
  fi
  mv "$dest_stage/$name" "$dest_root/$name"
  installed_names+=("$name")
done

receipt_tmp="$(mktemp "$receipt_dir/.ctf-skills.XXXXXX")"
python3 - "$receipt_tmp" "$ctf_repository" "$ctf_commit" "${skill_names[@]}" <<'PY'
import json
import sys

path, repository, commit, *skills = sys.argv[1:]
with open(path, "w", encoding="utf-8") as handle:
    json.dump(
        {"repository": repository, "commit": commit, "skills": skills},
        handle,
        indent=2,
    )
    handle.write("\n")
PY
mv "$receipt_tmp" "$receipt_file"

transaction_active=false
echo "Installed ${#skill_names[@]} optional CTF skill(s) from ${ctf_repository}@${ctf_commit}."
