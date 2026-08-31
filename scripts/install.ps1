# PowerShell Install Script — AIGC Competition Statement Skill
# Compatible with Windows PowerShell 5.1+ and PowerShell 7+
# Does NOT require admin privileges.

param(
    [string]$Platform = "",
    [switch]$Uninstall
)

$SKILL_NAME = "aigc-competition-statement"
$SKILL_VERSION = "0.1.0"
$REPO_URL = "https://github.com/thenightmygfcomeoutthecloset/aigc-competition-statement"

Write-Host ""
Write-Host "========================================"
Write-Host "  AIGC Competition Statement Skill"
Write-Host "  v$SKILL_VERSION"
Write-Host "========================================"
Write-Host ""

# ── Uninstall ──────────────────────────────────────────────────────────────
if ($Uninstall) {
    Write-Host "Uninstall: removing skill from Antigravity..."
    $globalSkillPath = Join-Path $HOME ".gemini\config\skills\$SKILL_NAME"
    if (Test-Path $globalSkillPath) {
        Remove-Item -Recurse -Force $globalSkillPath
        Write-Host "Removed: $globalSkillPath"
    } else {
        Write-Host "Not found at $globalSkillPath — nothing to remove."
    }
    Write-Host ""
    Write-Host "To remove from other platforms, delete the adapter file you copied."
    Write-Host "See: $REPO_URL#uninstall"
    exit 0
}

# ── Select Platform ────────────────────────────────────────────────────────
if (-not $Platform) {
    Write-Host "Which platform are you installing for?"
    Write-Host "  1. Google Antigravity (AGY)  [Native — Recommended]"
    Write-Host "  2. Cursor                    [Adapter]"
    Write-Host "  3. Windsurf                  [Adapter]"
    Write-Host "  4. Claude                    [Project Instructions]"
    Write-Host "  5. Codex                     [Setup Instructions — manual paste]"
    Write-Host ""
    $choice = Read-Host "Enter number (1-5)"
    switch ($choice) {
        "1" { $Platform = "antigravity" }
        "2" { $Platform = "cursor" }
        "3" { $Platform = "windsurf" }
        "4" { $Platform = "claude" }
        "5" { $Platform = "codex" }
        default {
            Write-Host "Invalid choice. Exiting."
            exit 1
        }
    }
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir

# ── Install ────────────────────────────────────────────────────────────────
switch ($Platform.ToLower()) {

    "antigravity" {
        $dest = Join-Path $HOME ".gemini\config\skills\$SKILL_NAME"
        Write-Host "Installing to: $dest"
        Write-Host ""
        if (Test-Path $dest) {
            $backup = "$dest.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Write-Host "Existing installation found. Creating backup at:"
            Write-Host "  $backup"
            Copy-Item -Recurse $dest $backup
        }
        Copy-Item -Recurse $repoRoot $dest -Force
        Write-Host ""
        Write-Host "[OK] Skill installed. Antigravity will auto-detect it."
        Write-Host ""
        Write-Host "To use: tell your agent"
        Write-Host "  '帮我写 AIGC 创作说明' or '帮我整理比赛的 AI 说明书'"
    }

    "cursor" {
        $adapterSrc = Join-Path $repoRoot "adapters\cursor\aigc-competition-statement.mdc"
        $cursorRulesDir = Join-Path (Get-Location) ".cursor\rules"
        $dest = Join-Path $cursorRulesDir "aigc-competition-statement.mdc"
        Write-Host "Installing Cursor adapter to: $dest"
        if (-not (Test-Path $cursorRulesDir)) {
            New-Item -ItemType Directory -Force -Path $cursorRulesDir | Out-Null
        }
        if (Test-Path $dest) {
            $backup = "$dest.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Copy-Item $dest $backup
            Write-Host "Backup created: $backup"
        }
        Copy-Item $adapterSrc $dest -Force
        Write-Host ""
        Write-Host "[OK] Cursor adapter installed."
        Write-Host "     File: $dest"
        Write-Host "     Cursor will load this rule automatically."
    }

    "windsurf" {
        $adapterSrc = Join-Path $repoRoot "adapters\windsurf\aigc-competition-statement.md"
        $windsurfRulesDir = Join-Path (Get-Location) ".windsurf\rules"
        $dest = Join-Path $windsurfRulesDir "aigc-competition-statement.md"
        Write-Host "Installing Windsurf adapter to: $dest"
        if (-not (Test-Path $windsurfRulesDir)) {
            New-Item -ItemType Directory -Force -Path $windsurfRulesDir | Out-Null
        }
        if (Test-Path $dest) {
            $backup = "$dest.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Copy-Item $dest $backup
            Write-Host "Backup created: $backup"
        }
        Copy-Item $adapterSrc $dest -Force
        Write-Host ""
        Write-Host "[OK] Windsurf adapter installed."
        Write-Host "     File: $dest"
    }

    "claude" {
        $adapterSrc = Join-Path $repoRoot "adapters\claude\project-instructions.md"
        Write-Host "Claude uses Project Instructions (web-based, cannot auto-install)."
        Write-Host ""
        Write-Host "Steps:"
        Write-Host "  1. Open claude.ai and go to your Project"
        Write-Host "  2. Click 'Project instructions'"
        Write-Host "  3. Paste the content of this file:"
        Write-Host "     $adapterSrc"
        Write-Host ""
        Write-Host "Opening the file for you to copy..."
        Start-Process notepad $adapterSrc
    }

    "codex" {
        $adapterSrc = Join-Path $repoRoot "adapters\codex\setup-instructions.md"
        Write-Host "Codex uses Setup Instructions (web-based, cannot auto-install)."
        Write-Host ""
        Write-Host "Steps:"
        Write-Host "  1. Open codex.com and open or create an Agent"
        Write-Host "  2. Go to Setup Instructions"
        Write-Host "  3. Paste the content of this file:"
        Write-Host "     $adapterSrc"
        Write-Host ""
        Write-Host "Opening the file for you to copy..."
        Start-Process notepad $adapterSrc
    }

    default {
        Write-Host "Unknown platform: $Platform"
        Write-Host "Valid options: antigravity, cursor, windsurf, claude, codex"
        exit 1
    }
}

Write-Host ""
Write-Host "To uninstall, run: .\scripts\install.ps1 -Uninstall"
Write-Host "For help: $REPO_URL"
Write-Host ""