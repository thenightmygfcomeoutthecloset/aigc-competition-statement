#!/usr/bin/env python3
"""Test-only external provider stub: copy declared complete-image fixtures."""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path


def main() -> int:
    request = json.loads(sys.stdin.read())
    plan = json.loads(os.environ["AIGC_FIXTURE_GENERATION_PLAN"])
    source = Path(plan[request["stage_id"]])
    output = Path(os.environ["AIGC_OUTPUT_PATH"])
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output)
    print(json.dumps({"provider_request_id": f"fixture-{request['stage_id']}", "test_only": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
