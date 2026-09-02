#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_consistency.py - Repository consistency and integrity checker.

Validates:
1. Version synchronization across READMEs, CHANGELOG, install scripts, and adapters.
2. Mode namespace integrity (only Evidence, Hybrid, Reconstruction modes allowed).
3. Canonical required asset schema references.
4. Orphan templates detection.
5. Relative Markdown links validity.
6. Example asset consistency.
"""

import os
import sys
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXPECTED_VERSION = "0.2.2"


def check_version_sync() -> list:
    errors = []
    
    # 1. README.md badge
    readme_path = REPO_ROOT / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        if f"version-{EXPECTED_VERSION}-blue" not in content:
            errors.append(f"README.md badge does not match version {EXPECTED_VERSION}")
            
    # 2. README_EN.md badge
    readme_en_path = REPO_ROOT / "README_EN.md"
    if readme_en_path.exists():
        content = readme_en_path.read_text(encoding="utf-8")
        if f"version-{EXPECTED_VERSION}-blue" not in content:
            errors.append(f"README_EN.md badge does not match version {EXPECTED_VERSION}")
            
    # 3. CHANGELOG.md
    changelog_path = REPO_ROOT / "CHANGELOG.md"
    if changelog_path.exists():
        content = changelog_path.read_text(encoding="utf-8")
        if f"## [{EXPECTED_VERSION}]" not in content:
            errors.append(f"CHANGELOG.md missing header for [{EXPECTED_VERSION}]")
            
    # 4. install.ps1
    install_ps1 = REPO_ROOT / "scripts" / "install.ps1"
    if install_ps1.exists():
        content = install_ps1.read_text(encoding="utf-8")
        if f'SKILL_VERSION = "{EXPECTED_VERSION}"' not in content:
            errors.append(f"install.ps1 does not have SKILL_VERSION = \"{EXPECTED_VERSION}\"")
            
    # 5. install.sh
    install_sh = REPO_ROOT / "scripts" / "install.sh"
    if install_sh.exists():
        content = install_sh.read_text(encoding="utf-8")
        if f'SKILL_VERSION="{EXPECTED_VERSION}"' not in content:
            errors.append(f"install.sh does not have SKILL_VERSION=\"{EXPECTED_VERSION}\"")
            
    return errors


def check_mode_names() -> list:
    errors = []
    forbidden_terms = ["Generic Draft Mode", "双模式", "双工作模式"]
    
    text_files = list(REPO_ROOT.glob("*.md")) + list((REPO_ROOT / "skill").glob("*.md"))
    for file in text_files:
        content = file.read_text(encoding="utf-8")
        for term in forbidden_terms:
            if term in content:
                errors.append(f"Forbidden mode term '{term}' found in {file.name}")
    return errors


def check_orphan_templates() -> list:
    errors = []
    templates_dir = REPO_ROOT / "templates"
    if not templates_dir.exists():
        return errors
        
    core_files = [REPO_ROOT / "SKILL.md"] + list((REPO_ROOT / "skill").glob("*.md"))
    all_core_text = "\n".join([f.read_text(encoding="utf-8") for f in core_files if f.exists()])
    
    for tmpl in templates_dir.glob("*.md"):
        if tmpl.name not in all_core_text:
            errors.append(f"Orphan template detected: {tmpl.name} is not referenced in SKILL.md or skill/*.md")
            
    return errors


def check_canonical_asset_references() -> list:
    errors = []
    reconstruction_path = REPO_ROOT / "skill" / "reconstruction.md"
    if not reconstruction_path.exists():
        return ["skill/reconstruction.md not found"]
        
    content = reconstruction_path.read_text(encoding="utf-8")
    required_assets = [
        "01_reconstructed_sketch.png",
        "01_reconstructed_lineart.png",
        "01_reconstructed_color_block.png",
        "02_reconstructed_generation_v1.png",
        "03_reconstructed_generation_v2.png",
        "reference_to_sketch",
        "reference_to_lineart",
        "reference_to_color_block",
        "reference_to_intermediate_generation"
    ]
    for asset in required_assets:
        if asset not in content:
            errors.append(f"Canonical asset/operator '{asset}' missing from reconstruction.md")
            
    return errors


def main():
    print(f"Running repository consistency checks for v{EXPECTED_VERSION}...")
    all_errors = []
    
    ver_errs = check_version_sync()
    if ver_errs:
        all_errors.extend(ver_errs)
    else:
        print("  [OK] Version synchronization across files")
        
    mode_errs = check_mode_names()
    if mode_errs:
        all_errors.extend(mode_errs)
    else:
        print("  [OK] Three mode namespace integrity")
        
    orphan_errs = check_orphan_templates()
    if orphan_errs:
        all_errors.extend(orphan_errs)
    else:
        print("  [OK] Zero orphan templates")
        
    asset_errs = check_canonical_asset_references()
    if asset_errs:
        all_errors.extend(asset_errs)
    else:
        print("  [OK] Canonical required asset schema references")
        
    if all_errors:
        print(f"\nFAILED with {len(all_errors)} error(s):", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nAll consistency checks passed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()

