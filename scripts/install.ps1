# PowerShell Install Script — AIGC Competition Statement Skill v0.2.2
# Compatible with Windows PowerShell 5.1+ and PowerShell 7+
# Does NOT require admin privileges.

param(
    [ValidateSet("antigravity", "cursor", "codex", "windsurf", "claude", "")]
    [string]$Platform = "",
    [switch]$Uninstall,
    [switch]$DryRun
)

$SKILL_NAME = "aigc-competition-statement"
$SKILL_VERSION = "0.2.2"
$REPO_URL = "https://github.com/thenightmygfcomeoutthecloset/aigc-competition-statement"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir

Write-Host ""
Write-Host "========================================"
Write-Host "  AIGC Competition Statement Skill"
Write-Host "  v$SKILL_VERSION"
if ($DryRun) { Write-Host "  [DRY RUN — no files will be changed]" }
Write-Host "========================================"
Write-Host ""

# ── Platform Selection ─────────────────────────────────────────────────────
if (-not $Platform) {
    Write-Host "Which platform?"
    Write-Host "  1. Google Antigravity (AGY)     [Native Skill — ~/.gemini/config/skills/]"
    Write-Host "  2. Cursor                       [Native Skill — ~/.cursor/skills/]"
    Write-Host "  3. OpenAI Codex                 [Native Skill — ~/.agents/skills/]"
    Write-Host "  4. Windsurf                     [Project Rule — .windsurf/rules/]"
    Write-Host "  5. Claude                       [Project Instructions — manual paste]"
    Write-Host ""
    $choice = Read-Host "Enter number (1-5)"
    switch ($choice) {
        "1" { $Platform = "antigravity" }
        "2" { $Platform = "cursor" }
        "3" { $Platform = "codex" }
        "4" { $Platform = "windsurf" }
        "5" { $Platform = "claude" }
        default { Write-Host "Invalid choice. Exiting."; exit 1 }
    }
}

function Show-Plan($src, $dest, $type) {
    Write-Host ""
    Write-Host "  Action   : $type"
    Write-Host "  Source   : $src"
    Write-Host "  Target   : $dest"
    Write-Host "  Backup   : ${dest}.backup_<timestamp> (if target exists)"
    Write-Host "  Uninstall: .\scripts\install.ps1 -Platform $Platform -Uninstall"
    Write-Host ""
}

function Safe-Copy-Skill($srcRoot, $destDir) {
    if (-not (Test-Path $destDir)) {
        if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $destDir | Out-Null }
        Write-Host "  Created directory: $destDir"
    } else {
        $backup = "$destDir.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Write-Host "  Backup: $backup"
        if (-not $DryRun) { Copy-Item -Recurse $destDir $backup }
    }
    
    $items = @("SKILL.md", "skill", "templates", "adapters", "scripts", "README.md", "LICENSE")
    foreach ($item in $items) {
        $srcPath = Join-Path $srcRoot $item
        if (Test-Path $srcPath) {
            if (-not $DryRun) { Copy-Item -Path $srcPath -Destination $destDir -Recurse -Force }
        }
    }
}

function Safe-Copy-File($srcFile, $destFile) {
    $parentDir = Split-Path -Parent $destFile
    if (-not (Test-Path $parentDir)) {
        if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $parentDir | Out-Null }
    }
    if (Test-Path $destFile) {
        $backup = "$destFile.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        if (-not $DryRun) { Copy-Item $destFile $backup }
    }
    if (-not $DryRun) { Copy-Item -Path $srcFile -Destination $destFile -Force }
}

function Safe-Remove($dest) {
    if (Test-Path $dest) {
        Write-Host "  Removing: $dest"
        if (-not $DryRun) {
            $uninstalled = "$dest.uninstalled_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Move-Item -Path $dest -Destination $uninstalled -Force
            Write-Host "  [OK] Moved to $uninstalled"
        }
    } else {
        Write-Host "  Not found: $dest — nothing to remove."
    }
}

# ── Uninstall ──────────────────────────────────────────────────────────────
if ($Uninstall) {
    Write-Host "Uninstalling from: $Platform"
    switch ($Platform) {
        "antigravity" {
            $dest = Join-Path $HOME ".gemini\config\skills\$SKILL_NAME"
            Show-Plan "" $dest "Safely archive directory"
            Safe-Remove $dest
        }
        "cursor" {
            $skillDest = Join-Path $HOME ".cursor\skills\$SKILL_NAME"
            $ruleDest  = Join-Path $HOME ".cursor\rules\$SKILL_NAME.mdc"
            Show-Plan "" $skillDest "Safely archive directory"
            Safe-Remove $skillDest
            if (Test-Path $ruleDest) {
                Safe-Remove $ruleDest
            }
        }
        "codex" {
            $skillDest = Join-Path $HOME ".agents\skills\$SKILL_NAME"
            Show-Plan "" $skillDest "Safely archive directory"
            Safe-Remove $skillDest
        }
        "windsurf" {
            $curDir = Get-Location
            $ruleDest = Join-Path $curDir ".windsurf\rules\aigc-competition-statement.md"
            Show-Plan "" $ruleDest "Safely archive file"
            Safe-Remove $ruleDest
        }
        "claude" {
            Write-Host "Claude Project Instructions are managed on the web."
            Write-Host "To uninstall: open claude.ai > Project > Project instructions > clear the AIGC content."
        }
    }
    Write-Host ""
    if ($DryRun) { Write-Host "[DRY RUN] No files were changed." }
    exit 0
}

# ── Install ────────────────────────────────────────────────────────────────
switch ($Platform) {

    "antigravity" {
        $dest = Join-Path $HOME ".gemini\config\skills\$SKILL_NAME"
        Show-Plan $repoRoot $dest "Copy skill components"
        Safe-Copy-Skill $repoRoot $dest
        if (-not $DryRun) {
            Write-Host "[OK] Antigravity skill installed at: $dest"
            Write-Host "     Antigravity will auto-detect it. No restart needed."
        }
    }

    "cursor" {
        $dest = Join-Path $HOME ".cursor\skills\$SKILL_NAME"
        Show-Plan $repoRoot $dest "Copy as Cursor Native Skill (~/.cursor/skills/)"
        Safe-Copy-Skill $repoRoot $dest
        if (-not $DryRun) {
            Write-Host "[OK] Cursor skill installed at: $dest"
            Write-Host "     Cursor will discover it automatically."
        }
    }

    "codex" {
        $dest = Join-Path $HOME ".agents\skills\$SKILL_NAME"
        Show-Plan $repoRoot $dest "Copy as Codex Native Skill (~/.agents/skills/)"
        Safe-Copy-Skill $repoRoot $dest
        if (-not $DryRun) {
            Write-Host "[OK] Codex skill installed at: $dest"
            Write-Host "     Codex will discover it from SKILL.md frontmatter."
        }
    }

    "windsurf" {
        $adapterSrc  = Join-Path $repoRoot "adapters\windsurf\aigc-competition-statement.md"
        $curDir      = Get-Location
        $dest        = Join-Path $curDir ".windsurf\rules\aigc-competition-statement.md"
        Show-Plan $adapterSrc $dest "Copy Windsurf Rule file"
        Safe-Copy-File $adapterSrc $dest
        if (-not $DryRun) {
            Write-Host "[OK] Windsurf rule installed at: $dest"
        }
    }

    "claude" {
        $adapterSrc = Join-Path $repoRoot "adapters\claude\project-instructions.md"
        Write-Host "Claude uses Project Instructions (web-based)."
        Write-Host ""
        Write-Host "Steps:"
        Write-Host "  1. Open claude.ai and open or create a Project"
        Write-Host "  2. Click 'Project instructions'"
        Write-Host "  3. Paste the contents of:"
        Write-Host "     $adapterSrc"
        Write-Host ""
        if (-not $DryRun) { Start-Process notepad $adapterSrc }
    }
}

Write-Host ""
if ($DryRun) {
    Write-Host "[DRY RUN] No files were changed. Remove -DryRun to execute."
} else {
    Write-Host "Uninstall: .\scripts\install.ps1 -Platform $Platform -Uninstall"
    Write-Host "Help:      $REPO_URL"
}
Write-Host ""




