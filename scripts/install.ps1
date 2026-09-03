#!/usr/bin/env pwsh
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("antigravity", "cursor", "codex", "windsurf", "claude")]
    [string]$Platform,
    [string]$DestinationRoot = "",
    [switch]$Uninstall,
    [switch]$DryRun,
    [switch]$SkipFontInstall
)

$ErrorActionPreference = "Stop"
$SKILL_NAME = "aigc-competition-statement"
$SKILL_VERSION = "0.3.0"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir

function Resolve-Destination {
    if ($DestinationRoot) { return Join-Path $DestinationRoot $SKILL_NAME }
    switch ($Platform) {
        "antigravity" { return Join-Path $HOME ".gemini\config\skills\$SKILL_NAME" }
        "cursor" { return Join-Path $HOME ".cursor\skills\$SKILL_NAME" }
        "codex" { return Join-Path $HOME ".agents\skills\$SKILL_NAME" }
        "windsurf" { return Join-Path (Get-Location) ".windsurf\rules\$SKILL_NAME.md" }
        "claude" { return Join-Path (Get-Location) "$SKILL_NAME-project-instructions.md" }
    }
}

function Install-UserFont {
    $fontSource = Join-Path $repoRoot "assets\fonts\NotoSansSC-Regular.ttf"
    if (-not (Test-Path -LiteralPath $fontSource)) { throw "Bundled redistributable font missing: $fontSource" }
    $fontRoot = Join-Path $env:LOCALAPPDATA "Microsoft\Windows\Fonts"
    $fontTarget = Join-Path $fontRoot "NotoSansSC-Regular.ttf"
    if (-not $DryRun) {
        New-Item -ItemType Directory -Force -Path $fontRoot | Out-Null
        Copy-Item -LiteralPath $fontSource -Destination $fontTarget -Force
        $key = "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts"
        New-Item -Path $key -Force | Out-Null
        New-ItemProperty -Path $key -Name "Noto Sans SC (TrueType)" -Value $fontTarget -PropertyType String -Force | Out-Null
    }
    Write-Host "Font installed: $fontTarget"
}

$destination = Resolve-Destination
Write-Host "AIGC Competition Statement Skill v$SKILL_VERSION"
Write-Host "Target: $destination"

if ($Uninstall) {
    if (Test-Path -LiteralPath $destination) {
        $archive = "$destination.uninstalled_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        if (-not $DryRun) { Move-Item -LiteralPath $destination -Destination $archive }
        Write-Host "Archived: $archive"
    }
    exit 0
}

if ($Platform -eq "windsurf") {
    $source = Join-Path $repoRoot "adapters\windsurf\aigc-competition-statement.md"
    if (-not $DryRun) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $destination) | Out-Null
        Copy-Item -LiteralPath $source -Destination $destination -Force
    }
} elseif ($Platform -eq "claude") {
    $source = Join-Path $repoRoot "adapters\claude\project-instructions.md"
    if (-not $DryRun) { Copy-Item -LiteralPath $source -Destination $destination -Force }
} else {
    if ((Test-Path -LiteralPath $destination) -and -not $DestinationRoot) {
        $backup = "$destination.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        if (-not $DryRun) { Copy-Item -LiteralPath $destination -Destination $backup -Recurse }
        Write-Host "Backup: $backup"
    }
    if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $destination | Out-Null }
    $items = @("SKILL.md", "skill", "templates", "adapters", "agents", "scripts", "schema", "assets", "README.md", "LICENSE", "requirements.txt")
    foreach ($item in $items) {
        $source = Join-Path $repoRoot $item
        if (-not (Test-Path -LiteralPath $source)) { throw "Required install item missing: $source" }
        if (-not $DryRun) { Copy-Item -LiteralPath $source -Destination $destination -Recurse -Force }
    }
}

if (-not $SkipFontInstall -and -not $DestinationRoot) { Install-UserFont }
Write-Host "Installed successfully: $destination"
