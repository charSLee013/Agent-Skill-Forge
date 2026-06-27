#!/usr/bin/env bash
set -euo pipefail

agent="${AGENT:-agents}"
owner="${AGENT_SKILL_FORGE_OWNER:-charSLee013}"
repo="${AGENT_SKILL_FORGE_REPO:-Agent-Skill-Forge}"
ref="${AGENT_SKILL_FORGE_REF:-master}"
tmp_dir=""

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

print_help() {
  cat <<'EOF'
Install skills from this repository.

Usage:
  bash scripts/install.sh
  bash scripts/install.sh teach handoff grill-me
  curl -fsSL https://raw.githubusercontent.com/charSLee013/Agent-Skill-Forge/master/scripts/install.sh | bash
  AGENT=codex bash scripts/install.sh

Default:
  Installs all skills to $HOME/.agents/skills.

Supported AGENT values:
  agents    -> $HOME/.agents/skills
  codex     -> ${CODEX_HOME:-$HOME/.codex}/skills
  claude    -> $HOME/.claude/skills
  opencode  -> $HOME/.config/opencode/skills
EOF

  echo
  echo "Available skills:"
  printf '  %s\n' "${skill_names[@]}"
}

fail_with_help() {
  echo "error: $*" >&2
  echo >&2
  print_help >&2
  exit 1
}

if [[ "${1:-}" == "-h" ]] || [[ "${1:-}" == "--help" ]]; then
  print_help
  exit 0
fi

if [[ "${#skill_names[@]}" -eq 0 ]]; then
  echo "error: no skills found under $repo_root/skills" >&2
  exit 1
fi

case "$agent" in
  agents)
    dest_root="$HOME/.agents/skills"
    ;;
  codex)
    dest_root="${CODEX_HOME:-$HOME/.codex}/skills"
    ;;
  claude)
    dest_root="$HOME/.claude/skills"
    ;;
  opencode)
    dest_root="$HOME/.config/opencode/skills"
    ;;
  *)
    fail_with_help "unsupported AGENT '$agent'"
    ;;
esac

declare -a selected_names=()
declare -a selected_dirs=()

select_skill() {
  local requested="$1"
  local found=0

  for i in "${!skill_names[@]}"; do
    if [[ "${skill_names[$i]}" == "$requested" ]]; then
      selected_names+=("${skill_names[$i]}")
      selected_dirs+=("${skill_dirs[$i]}")
      found=1
      break
    fi
  done

  if [[ "$found" -eq 0 ]]; then
    fail_with_help "unknown skill '$requested'"
  fi
}

if [[ "$#" -eq 0 ]]; then
  selected_names=("${skill_names[@]}")
  selected_dirs=("${skill_dirs[@]}")
else
  for requested in "$@"; do
    select_skill "$requested"
  done
fi

mkdir -p "$dest_root"

echo "Installing ${#selected_names[@]} skill(s) for $agent:"
echo "  $dest_root"

for i in "${!selected_names[@]}"; do
  name="${selected_names[$i]}"
  src="${selected_dirs[$i]}"
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
