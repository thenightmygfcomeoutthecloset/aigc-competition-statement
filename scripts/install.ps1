# AIGC Competition Statement Skill installer (Windows PowerShell 5.1+)
[CmdletBinding()]
param(
    [ValidateSet("antigravity", "cursor", "codex", "windsurf", "claude", "")]
    [string]$Platform = "",
    [switch]$Uninstall,
    [switch]$DryRun,
    [string]$UserHome = $HOME
)

$ErrorActionPreference = "Stop"
$SkillName = "aigc-competition-statement"
$SkillVersion = "0.1.2"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

function Select-Platform {
    Write-Host "1. Google Antigravity  2. Cursor  3. OpenAI Codex  4. Windsurf  5. Claude"
    switch (Read-Host "Choose platform (1-5)") {
        "1" { return "antigravity" }
        "2" { return "cursor" }
        "3" { return "codex" }
        "4" { return "windsurf" }
        "5" { return "claude" }
        default { throw "Invalid platform selection." }
    }
}

function Assert-ExactChild([string]$Path, [string]$Parent) {
    $resolvedParent = [System.IO.Path]::GetFullPath($Parent).TrimEnd('\')
    $resolvedPath = [System.IO.Path]::GetFullPath($Path)
    if ((Split-Path -Parent $resolvedPath).TrimEnd('\') -ne $resolvedParent) {
        throw "Unsafe destination: $resolvedPath"
    }
}

function Show-Plan([string]$Action, [string]$Source, [string]$Target) {
    Write-Host ""
    Write-Host "Action : $Action"
    Write-Host "Source : $Source"
    Write-Host "Target : $Target"
    Write-Host "Backup : $Target.backup_<timestamp>"
    if ($DryRun) { Write-Host "Mode   : DRY RUN" }
}

function Copy-Payload([string]$Target, [string]$ExpectedParent) {
    Assert-ExactChild $Target $ExpectedParent
    if (Test-Path -LiteralPath $Target) {
        $backup = "$Target.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Write-Host "Backup : $backup"
        if (-not $DryRun) { Move-Item -LiteralPath $Target -Destination $backup }
    }
    if ($DryRun) { return }
    New-Item -ItemType Directory -Force -Path $Target | Out-Null
    Copy-Item -LiteralPath (Join-Path $RepoRoot "SKILL.md") -Destination $Target
    foreach ($directory in @("skill", "templates")) {
        Copy-Item -LiteralPath (Join-Path $RepoRoot $directory) -Destination $Target -Recurse
    }
}

function Remove-Recoverably([string]$Target, [string]$ExpectedParent) {
    Assert-ExactChild $Target $ExpectedParent
    if (-not (Test-Path -LiteralPath $Target)) {
        Write-Host "Not installed: $Target"
        return
    }
    $backup = "$Target.uninstalled_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Write-Host "Recoverable uninstall target: $backup"
    if (-not $DryRun) { Move-Item -LiteralPath $Target -Destination $backup }
}

if (-not $Platform) { $Platform = Select-Platform }
$UserHome = [System.IO.Path]::GetFullPath($UserHome)
Write-Host "AIGC Competition Statement Skill v$SkillVersion"

switch ($Platform) {
    "antigravity" { $parent = Join-Path $UserHome ".gemini\config\skills"; $target = Join-Path $parent $SkillName }
    "cursor"      { $parent = Join-Path $UserHome ".cursor\skills"; $target = Join-Path $parent $SkillName }
    "codex"       { $parent = Join-Path $UserHome ".agents\skills"; $target = Join-Path $parent $SkillName }
    "windsurf"    { $parent = Join-Path (Get-Location) ".windsurf\rules"; $target = Join-Path $parent "$SkillName.md" }
    "claude"      {
        Write-Host "Paste the contents of adapters\claude\project-instructions.md into Claude Project Instructions."
        exit 0
    }
}

if ($Platform -eq "windsurf") {
    Show-Plan $(if ($Uninstall) { "Uninstall rule" } else { "Install rule" }) (Join-Path $RepoRoot "adapters\windsurf\$SkillName.md") $target
    if ($Uninstall) { Remove-Recoverably $target $parent }
    elseif (-not $DryRun) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
        if (Test-Path -LiteralPath $target) { Move-Item -LiteralPath $target -Destination "$target.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')" }
        Copy-Item -LiteralPath (Join-Path $RepoRoot "adapters\windsurf\$SkillName.md") -Destination $target
    }
} else {
    Show-Plan $(if ($Uninstall) { "Uninstall skill" } else { "Install skill payload" }) $RepoRoot $target
    if ($Uninstall) { Remove-Recoverably $target $parent } else { Copy-Payload $target $parent }
}

if ($DryRun) { Write-Host "DRY RUN complete; no files changed." } else { Write-Host "Done: $target" }
