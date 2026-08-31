#!/usr/bin/env bash
# install.sh — AIGC Competition Statement Skill
# macOS / Linux. Does NOT require sudo.
set -e

SKILL_NAME="aigc-competition-statement"
SKILL_VERSION="0.1.0"
REPO_URL="https://github.com/thenightmygfcomeoutthecloset/aigc-competition-statement"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo ""
echo "========================================"
echo "  AIGC Competition Statement Skill"
echo "  v$SKILL_VERSION"
echo "========================================"
echo ""

# ── Uninstall ──────────────────────────────────────────────────────────────
if [[ "$1" == "--uninstall" ]]; then
    DEST="$HOME/.gemini/config/skills/$SKILL_NAME"
    if [[ -d "$DEST" ]]; then
        rm -rf "$DEST"
        echo "Removed: $DEST"
    else
        echo "Not found at $DEST — nothing to remove."
    fi
    echo "To remove from other platforms, delete the adapter file you placed."
    echo "See: $REPO_URL#uninstall"
    exit 0
fi

# ── Select Platform ────────────────────────────────────────────────────────
PLATFORM="${1:-}"
if [[ -z "$PLATFORM" ]]; then
    echo "Which platform are you installing for?"
    echo "  1. Google Antigravity (AGY)  [Native — Recommended]"
    echo "  2. Cursor                    [Adapter]"
    echo "  3. Windsurf                  [Adapter]"
    echo "  4. Claude                    [Project Instructions — manual]"
    echo "  5. Codex                     [Setup Instructions — manual]"
    echo ""
    read -rp "Enter number (1-5): " CHOICE
    case "$CHOICE" in
        1) PLATFORM="antigravity" ;;
        2) PLATFORM="cursor" ;;
        3) PLATFORM="windsurf" ;;
        4) PLATFORM="claude" ;;
        5) PLATFORM="codex" ;;
        *) echo "Invalid choice. Exiting."; exit 1 ;;
    esac
fi

backup_if_exists() {
    local target="$1"
    if [[ -e "$target" ]]; then
        local backup="${target}.backup_$(date +%Y%m%d_%H%M%S)"
        cp -r "$target" "$backup"
        echo "Backup created: $backup"
    fi
}

# ── Install ────────────────────────────────────────────────────────────────
case "$PLATFORM" in

    antigravity)
        DEST="$HOME/.gemini/config/skills/$SKILL_NAME"
        echo "Installing to: $DEST"
        backup_if_exists "$DEST"
        mkdir -p "$(dirname "$DEST")"
        cp -r "$REPO_ROOT" "$DEST"
        echo ""
        echo "[OK] Skill installed. Antigravity will auto-detect it."
        echo ""
        echo "To use: tell your agent"
        echo "  '帮我写 AIGC 创作说明' or '帮我整理比赛的 AI 说明书'"
        ;;

    cursor)
        RULES_DIR="$(pwd)/.cursor/rules"
        DEST="$RULES_DIR/aigc-competition-statement.mdc"
        SRC="$REPO_ROOT/adapters/cursor/aigc-competition-statement.mdc"
        echo "Installing Cursor adapter to: $DEST"
        mkdir -p "$RULES_DIR"
        backup_if_exists "$DEST"
        cp "$SRC" "$DEST"
        echo ""
        echo "[OK] Cursor adapter installed."
        echo "     Cursor will load this rule automatically."
        ;;

    windsurf)
        RULES_DIR="$(pwd)/.windsurf/rules"
        DEST="$RULES_DIR/aigc-competition-statement.md"
        SRC="$REPO_ROOT/adapters/windsurf/aigc-competition-statement.md"
        echo "Installing Windsurf adapter to: $DEST"
        mkdir -p "$RULES_DIR"
        backup_if_exists "$DEST"
        cp "$SRC" "$DEST"
        echo ""
        echo "[OK] Windsurf adapter installed."
        ;;

    claude)
        SRC="$REPO_ROOT/adapters/claude/project-instructions.md"
        echo "Claude uses Project Instructions (web-based, cannot auto-install)."
        echo ""
        echo "Steps:"
        echo "  1. Open claude.ai and go to your Project"
        echo "  2. Click 'Project instructions'"
        echo "  3. Paste the content of:"
        echo "     $SRC"
        echo ""
        if command -v cat &>/dev/null; then
            echo "--- Content to copy ---"
            cat "$SRC"
            echo "--- End ---"
        fi
        ;;

    codex)
        SRC="$REPO_ROOT/adapters/codex/setup-instructions.md"
        echo "Codex uses Setup Instructions (web-based, cannot auto-install)."
        echo ""
        echo "Steps:"
        echo "  1. Open codex.com, open or create an Agent"
        echo "  2. Go to Setup Instructions"
        echo "  3. Paste the content of:"
        echo "     $SRC"
        echo ""
        if command -v cat &>/dev/null; then
            echo "--- Content to copy ---"
            cat "$SRC"
            echo "--- End ---"
        fi
        ;;

    *)
        echo "Unknown platform: $PLATFORM"
        echo "Valid: antigravity, cursor, windsurf, claude, codex"
        exit 1
        ;;
esac

echo ""
echo "To uninstall: ./scripts/install.sh --uninstall"
echo "For help: $REPO_URL"
echo ""