#!/usr/bin/env bash
# install.sh — AIGC Competition Statement Skill v0.1.1
# macOS / Linux. Does NOT require sudo.
set -e

SKILL_NAME="aigc-competition-statement"
SKILL_VERSION="0.1.1"
REPO_URL="https://github.com/thenightmygfcomeoutthecloset/aigc-competition-statement"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

DRY_RUN=false
PLATFORM="${1:-}"
UNINSTALL=false

# Parse args
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --uninstall) UNINSTALL=true ;;
    esac
done
# Remove flags, keep platform
PLATFORM="${1:-}"
if [[ "$PLATFORM" == --* ]]; then PLATFORM=""; fi

echo ""
echo "========================================"
echo "  AIGC Competition Statement Skill"
echo "  v$SKILL_VERSION"
if [[ "$DRY_RUN" == true ]]; then echo "  [DRY RUN — no files will be changed]"; fi
echo "========================================"
echo ""

# ── Platform Selection ────────────────────────────────────────────────────
if [[ -z "$PLATFORM" ]]; then
    echo "Which platform?"
    echo "  1. Google Antigravity (AGY)     [Native Skill]"
    echo "  2. Cursor                       [Native Skill — ~/.cursor/skills/]"
    echo "  3. OpenAI Codex                 [Native Skill — ~/.codex/skills/ + AGENTS.md]"
    echo "  4. Windsurf                     [Project Rule — .windsurf/rules/]"
    echo "  5. Claude                       [Project Instructions — manual paste]"
    echo ""
    read -rp "Enter number (1-5): " CHOICE
    case "$CHOICE" in
        1) PLATFORM="antigravity" ;;
        2) PLATFORM="cursor" ;;
        3) PLATFORM="codex" ;;
        4) PLATFORM="windsurf" ;;
        5) PLATFORM="claude" ;;
        *) echo "Invalid choice. Exiting."; exit 1 ;;
    esac
fi

show_plan() {
    local src="$1" dest="$2" action="$3"
    echo ""
    echo "  Action   : $action"
    echo "  Source   : $src"
    echo "  Target   : $dest"
    echo "  Backup   : ${dest}.backup_<timestamp> (if target exists)"
    echo "  Uninstall: bash scripts/install.sh $PLATFORM --uninstall"
    echo ""
}

safe_copy() {
    local src="$1" dest="$2"
    local destdir
    destdir="$(dirname "$dest")"
    if [[ ! -d "$destdir" ]]; then
        echo "  Creating directory: $destdir"
        if [[ "$DRY_RUN" == false ]]; then mkdir -p "$destdir"; fi
    fi
    if [[ -e "$dest" ]]; then
        local backup="${dest}.backup_$(date +%Y%m%d_%H%M%S)"
        echo "  Backup: $backup"
        if [[ "$DRY_RUN" == false ]]; then cp -r "$dest" "$backup"; fi
    fi
    if [[ "$DRY_RUN" == false ]]; then cp -r "$src" "$dest"; fi
}

safe_remove() {
    local dest="$1"
    if [[ -e "$dest" ]]; then
        echo "  Removing: $dest"
        if [[ "$DRY_RUN" == false ]]; then rm -rf "$dest"; fi
        echo "  [OK] Removed."
    else
        echo "  Not found: $dest — nothing to remove."
    fi
}

# ── Uninstall ─────────────────────────────────────────────────────────────
if [[ "$UNINSTALL" == true ]]; then
    echo "Uninstalling from: $PLATFORM"
    case "$PLATFORM" in
        antigravity)
            dest="$HOME/.gemini/config/skills/$SKILL_NAME"
            show_plan "" "$dest" "Remove directory"
            safe_remove "$dest"
            ;;
        cursor)
            skill_dest="$HOME/.cursor/skills/$SKILL_NAME"
            rule_dest="$HOME/.cursor/rules/${SKILL_NAME}.mdc"
            show_plan "" "$skill_dest" "Remove directory"
            safe_remove "$skill_dest"
            if [[ -e "$rule_dest" ]]; then
                echo "  Also found Cursor rule file: $rule_dest"
                safe_remove "$rule_dest"
            fi
            ;;
        codex)
            dest="$HOME/.codex/skills/$SKILL_NAME"
            show_plan "" "$dest" "Remove directory"
            safe_remove "$dest"
            ;;
        windsurf)
            dest="$(pwd)/.windsurf/rules/aigc-competition-statement.md"
            show_plan "" "$dest" "Remove file"
            safe_remove "$dest"
            ;;
        claude)
            echo "Claude Project Instructions are managed on the web."
            echo "To uninstall: open claude.ai > Project > Project instructions > clear the AIGC content."
            ;;
        *)
            echo "Unknown platform: $PLATFORM"
            exit 1
            ;;
    esac
    echo ""
    if [[ "$DRY_RUN" == true ]]; then echo "[DRY RUN] No files were changed."; fi
    exit 0
fi

# ── Install ────────────────────────────────────────────────────────────────
case "$PLATFORM" in

    antigravity)
        dest="$HOME/.gemini/config/skills/$SKILL_NAME"
        show_plan "$REPO_ROOT" "$dest" "Copy entire skill directory"
        safe_copy "$REPO_ROOT" "$dest"
        if [[ "$DRY_RUN" == false ]]; then
            echo "[OK] Antigravity skill installed at: $dest"
            echo "     Antigravity will auto-detect it."
        fi
        ;;

    cursor)
        dest="$HOME/.cursor/skills/$SKILL_NAME"
        show_plan "$REPO_ROOT" "$dest" "Copy as Cursor Native Skill (~/.cursor/skills/)"
        safe_copy "$REPO_ROOT" "$dest"
        if [[ "$DRY_RUN" == false ]]; then
            echo "[OK] Cursor skill installed at: $dest"
            echo "     Cursor will discover it automatically."
            echo ""
            echo "     Alternatively, for project-level Rule use:"
            echo "     cp $REPO_ROOT/adapters/cursor/aigc-competition-statement.mdc .cursor/rules/"
        fi
        ;;

    codex)
        dest="$HOME/.codex/skills/$SKILL_NAME"
        show_plan "$REPO_ROOT" "$dest" "Copy as Codex Native Skill (~/.codex/skills/)"
        safe_copy "$REPO_ROOT" "$dest"
        if [[ "$DRY_RUN" == false ]]; then
            echo "[OK] Codex skill installed at: $dest"
            echo "     Codex will discover it from SKILL.md frontmatter."
            echo ""
            echo "     For project-level AGENTS.md context:"
            echo "     cp $REPO_ROOT/adapters/codex/AGENTS.md ./AGENTS.md"
        fi
        ;;

    windsurf)
        adapter_src="$REPO_ROOT/adapters/windsurf/aigc-competition-statement.md"
        dest="$(pwd)/.windsurf/rules/aigc-competition-statement.md"
        show_plan "$adapter_src" "$dest" "Copy Windsurf Rule file"
        safe_copy "$adapter_src" "$dest"
        if [[ "$DRY_RUN" == false ]]; then
            echo "[OK] Windsurf rule installed at: $dest"
        fi
        ;;

    claude)
        adapter_src="$REPO_ROOT/adapters/claude/project-instructions.md"
        echo "Claude uses Project Instructions (web-based)."
        echo ""
        echo "Steps:"
        echo "  1. Open claude.ai and open or create a Project"
        echo "  2. Click 'Project instructions'"
        echo "  3. Paste the contents of:"
        echo "     $adapter_src"
        echo ""
        if command -v cat &>/dev/null; then
            echo "--- Content to paste ---"
            cat "$adapter_src"
            echo "--- End ---"
        fi
        echo ""
        echo "To 'uninstall': clear the pasted content from Project instructions."
        ;;

    *)
        echo "Unknown platform: $PLATFORM"
        echo "Valid: antigravity, cursor, codex, windsurf, claude"
        exit 1
        ;;
esac

echo ""
if [[ "$DRY_RUN" == true ]]; then
    echo "[DRY RUN] No files were changed. Remove --dry-run to execute."
else
    echo "Uninstall: bash scripts/install.sh $PLATFORM --uninstall"
    echo "Help:      $REPO_URL"
fi
echo ""