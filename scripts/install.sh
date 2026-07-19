#!/usr/bin/env bash
set -euo pipefail

owner="charSLee013"
repo="Agent-Skill-Forge"
ref="master"
tmp_dir=""

if [[ "$#" -ne 0 ]]; then
  echo "error: install.sh takes no arguments" >&2
  echo "Usage: bash scripts/install.sh" >&2
  exit 2
fi

cleanup() {
  if [[ -n "$tmp_dir" && -d "$tmp_dir" ]]; then
    rm -rf "$tmp_dir"
  fi
}
trap cleanup EXIT

script_source="${BASH_SOURCE[0]-}"
if [[ -n "$script_source" ]]; then
  repo_root="$(cd "$(dirname "$script_source")/.." 2>/dev/null && pwd || pwd)"
else
  repo_root="$(pwd)"
fi

if [[ ! -d "$repo_root/skills" ]]; then
  tmp_dir="$(mktemp -d)"
  archive_path="$tmp_dir/repo.tar.gz"
  tarball_url="https://codeload.github.com/${owner}/${repo}/tar.gz/refs/heads/${ref}"

  echo "Local skills directory not found. Downloading ${owner}/${repo}@${ref}..." >&2
  curl -fsSL "$tarball_url" -o "$archive_path"
  tar -xzf "$archive_path" -C "$tmp_dir"

  repo_root="$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -type d | head -n1)"
  if [[ -z "$repo_root" || ! -d "$repo_root/skills" ]]; then
    echo "error: downloaded repository does not contain a skills directory" >&2
    exit 1
  fi
fi

declare -a skill_names=()
declare -a skill_dirs=()

while IFS= read -r skill_md; do
  skill_dir="$(dirname "$skill_md")"
  skill_name="$(basename "$skill_dir")"
  skill_names+=("$skill_name")
  skill_dirs+=("$skill_dir")
done < <(find "$repo_root/skills" -name SKILL.md -not -path '*/node_modules/*' -print | sort)

if [[ "${#skill_names[@]}" -eq 0 ]]; then
  echo "error: no skills found under $repo_root/skills" >&2
  exit 1
fi

dest_root="$HOME/.agents/skills"
mkdir -p "$dest_root"

echo "Installing ${#skill_names[@]} current skill(s):"
echo "  $dest_root"

for i in "${!skill_names[@]}"; do
  name="${skill_names[$i]}"
  src="${skill_dirs[$i]}"
  dest="$dest_root/$name"

  rm -rf "$dest"
  cp -R "$src" "$dest"

  if [[ ! -f "$dest/SKILL.md" ]]; then
    echo "error: install verification failed for $name at $dest" >&2
    exit 1
  fi

  echo "  installed $name"
done

echo "Done."
