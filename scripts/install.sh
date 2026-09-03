#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="aigc-competition-statement"
SKILL_VERSION="0.3.1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
PLATFORM="${1:-}"
shift || true
DESTINATION_ROOT=""
DRY_RUN=false
UNINSTALL=false
SKIP_FONT=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --destination-root) DESTINATION_ROOT="$2"; shift 2 ;;
        --dry-run) DRY_RUN=true; shift ;;
        --uninstall) UNINSTALL=true; shift ;;
        --skip-font-install) SKIP_FONT=true; shift ;;
        *) echo "Unknown argument: $1" >&2; exit 2 ;;
    esac
done

case "$PLATFORM" in
    antigravity) default_dest="$HOME/.gemini/config/skills/$SKILL_NAME" ;;
    cursor) default_dest="$HOME/.cursor/skills/$SKILL_NAME" ;;
    codex) default_dest="$HOME/.agents/skills/$SKILL_NAME" ;;
    windsurf) default_dest="$(pwd)/.windsurf/rules/$SKILL_NAME.md" ;;
    claude) default_dest="$(pwd)/$SKILL_NAME-project-instructions.md" ;;
    *) echo "Usage: $0 {antigravity|cursor|codex|windsurf|claude} [options]" >&2; exit 2 ;;
esac
if [[ -n "$DESTINATION_ROOT" ]]; then destination="$DESTINATION_ROOT/$SKILL_NAME"; else destination="$default_dest"; fi

echo "AIGC Competition Statement Skill v$SKILL_VERSION"
echo "Target: $destination"

if [[ "$UNINSTALL" == true ]]; then
    if [[ -e "$destination" ]]; then
        archive="${destination}.uninstalled_$(date +%Y%m%d_%H%M%S)"
        if [[ "$DRY_RUN" == false ]]; then mv "$destination" "$archive"; fi
        echo "Archived: $archive"
    fi
    exit 0
fi

if [[ "$PLATFORM" == "windsurf" ]]; then
    if [[ "$DRY_RUN" == false ]]; then mkdir -p "$(dirname "$destination")"; cp "$REPO_ROOT/adapters/windsurf/aigc-competition-statement.md" "$destination"; fi
elif [[ "$PLATFORM" == "claude" ]]; then
    if [[ "$DRY_RUN" == false ]]; then cp "$REPO_ROOT/adapters/claude/project-instructions.md" "$destination"; fi
else
    if [[ -e "$destination" && -z "$DESTINATION_ROOT" ]]; then
        backup="${destination}.backup_$(date +%Y%m%d_%H%M%S)"
        if [[ "$DRY_RUN" == false ]]; then cp -R "$destination" "$backup"; fi
        echo "Backup: $backup"
    fi
    if [[ "$DRY_RUN" == false ]]; then
        mkdir -p "$destination"
        for item in SKILL.md skill templates adapters agents scripts schema assets README.md LICENSE requirements.txt; do
            [[ -e "$REPO_ROOT/$item" ]] || { echo "Required install item missing: $item" >&2; exit 1; }
            cp -R "$REPO_ROOT/$item" "$destination/"
        done
        find "$destination/scripts" -maxdepth 1 -type f \( -name '*.py' -o -name '*.sh' \) -exec chmod 755 {} +
    fi
fi

if [[ "$SKIP_FONT" == false && -z "$DESTINATION_ROOT" ]]; then
    font_source="$REPO_ROOT/assets/fonts/NotoSansSC-Regular.ttf"
    [[ -f "$font_source" ]] || { echo "Bundled redistributable font missing: $font_source" >&2; exit 1; }
    if [[ "$(uname -s)" == "Darwin" ]]; then font_dir="$HOME/Library/Fonts"; else font_dir="$HOME/.local/share/fonts"; fi
    if [[ "$DRY_RUN" == false ]]; then
        mkdir -p "$font_dir"
        cp "$font_source" "$font_dir/NotoSansSC-Regular.ttf"
        command -v fc-cache >/dev/null 2>&1 && fc-cache -f "$font_dir" >/dev/null || true
    fi
    echo "Font installed: $font_dir/NotoSansSC-Regular.ttf"
fi

echo "Installed successfully: $destination"
