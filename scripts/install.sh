#!/usr/bin/env bash
# AIGC Competition Statement Skill installer (macOS/Linux)
set -euo pipefail

SKILL_NAME="aigc-competition-statement"
SKILL_VERSION="0.1.2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
USER_HOME="${AIGC_SKILL_HOME:-$HOME}"
PLATFORM=""
DRY_RUN=false
UNINSTALL=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --uninstall) UNINSTALL=true ;;
        antigravity|cursor|codex|windsurf|claude) PLATFORM="$arg" ;;
        *) echo "Unknown argument: $arg" >&2; exit 2 ;;
    esac
done

if [[ -z "$PLATFORM" ]]; then
    printf '1. Antigravity  2. Cursor  3. OpenAI Codex  4. Windsurf  5. Claude\n'
    read -r -p 'Choose platform (1-5): ' choice
    case "$choice" in
        1) PLATFORM=antigravity ;; 2) PLATFORM=cursor ;; 3) PLATFORM=codex ;;
        4) PLATFORM=windsurf ;; 5) PLATFORM=claude ;; *) echo "Invalid selection" >&2; exit 2 ;;
    esac
fi

case "$PLATFORM" in
    antigravity) parent="$USER_HOME/.gemini/config/skills"; target="$parent/$SKILL_NAME" ;;
    cursor) parent="$USER_HOME/.cursor/skills"; target="$parent/$SKILL_NAME" ;;
    codex) parent="$USER_HOME/.agents/skills"; target="$parent/$SKILL_NAME" ;;
    windsurf) parent="$(pwd)/.windsurf/rules"; target="$parent/$SKILL_NAME.md" ;;
    claude)
        echo "Paste adapters/claude/project-instructions.md into Claude Project Instructions."
        exit 0 ;;
esac

assert_exact_child() {
    local expected="$1/$SKILL_NAME"
    [[ "$PLATFORM" == windsurf ]] && expected="$1/$SKILL_NAME.md"
    [[ "$2" == "$expected" ]] || { echo "Unsafe destination: $2" >&2; exit 3; }
}

show_plan() {
    echo "AIGC Competition Statement Skill v$SKILL_VERSION"
    echo "Action : $1"
    echo "Source : $2"
    echo "Target : $3"
    echo "Backup : $3.backup_<timestamp>"
    [[ "$DRY_RUN" == true ]] && echo "Mode   : DRY RUN"
}

copy_payload() {
    assert_exact_child "$parent" "$target"
    if [[ -e "$target" ]]; then
        backup="$target.backup_$(date +%Y%m%d_%H%M%S)"
        echo "Backup : $backup"
        [[ "$DRY_RUN" == false ]] && mv "$target" "$backup"
    fi
    [[ "$DRY_RUN" == true ]] && return
    mkdir -p "$target"
    cp "$REPO_ROOT/SKILL.md" "$target/"
    cp -R "$REPO_ROOT/skill" "$REPO_ROOT/templates" "$target/"
}

uninstall_recoverably() {
    assert_exact_child "$parent" "$target"
    if [[ ! -e "$target" ]]; then echo "Not installed: $target"; return; fi
    backup="$target.uninstalled_$(date +%Y%m%d_%H%M%S)"
    echo "Recoverable uninstall target: $backup"
    [[ "$DRY_RUN" == false ]] && mv "$target" "$backup"
}

if [[ "$PLATFORM" == windsurf ]]; then
    show_plan "$([[ "$UNINSTALL" == true ]] && echo 'Uninstall rule' || echo 'Install rule')" "$REPO_ROOT/adapters/windsurf/$SKILL_NAME.md" "$target"
    if [[ "$UNINSTALL" == true ]]; then uninstall_recoverably
    elif [[ "$DRY_RUN" == false ]]; then
        mkdir -p "$parent"
        [[ -e "$target" ]] && mv "$target" "$target.backup_$(date +%Y%m%d_%H%M%S)"
        cp "$REPO_ROOT/adapters/windsurf/$SKILL_NAME.md" "$target"
    fi
else
    show_plan "$([[ "$UNINSTALL" == true ]] && echo 'Uninstall skill' || echo 'Install skill payload')" "$REPO_ROOT" "$target"
    [[ "$UNINSTALL" == true ]] && uninstall_recoverably || copy_payload
fi

[[ "$DRY_RUN" == true ]] && echo "DRY RUN complete; no files changed." || echo "Done: $target"
