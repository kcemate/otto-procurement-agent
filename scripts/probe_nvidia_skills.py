#!/usr/bin/env python3
"""Record access to NVIDIA's verified agent skills catalog.

The contest post calls out NVIDIA's extensive agent skills. This script records
that the repo can discover that catalog without installing unneeded skills into
the project.
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
COMMAND = ["npx", "--yes", "skills", "add", "nvidia/skills", "--list", "--full-depth"]


def now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def parse(output: str) -> dict:
    found = None
    match = re.search(r"Found\s+(\d+)\s+skills", output)
    if match:
        found = int(match.group(1))
    samples = []
    for line in output.splitlines():
        clean = re.sub(r"\x1b\[[0-9;]*m", "", line).strip(" │")
        if clean and re.match(r"^[a-z0-9][a-z0-9-]+$", clean) and clean not in {"skills"}:
            samples.append(clean)
        if len(samples) >= 16:
            break
    return {"found_count": found, "sample_skills": samples}


def main() -> None:
    DATA.mkdir(exist_ok=True)
    try:
        proc = subprocess.run(COMMAND, cwd=ROOT, text=True, capture_output=True, timeout=180)
        output = proc.stdout + ("\nSTDERR:\n" + proc.stderr if proc.stderr else "")
        parsed = parse(output)
        status = "ok" if proc.returncode == 0 else "failed"
    except Exception as exc:
        output = repr(exc)
        parsed = {"found_count": None, "sample_skills": []}
        status = "failed"
    artifact = {
        "generated_at": now(),
        "source": "https://github.com/nvidia/skills",
        "command": " ".join(COMMAND),
        "status": status,
        "installed_into_project": False,
        "usage": "Catalog discovery proof for NVIDIA verified agent skills; no large skill payload is installed into this demo repo.",
        **parsed,
        "raw_excerpt": output[:5000],
    }
    (DATA / "nvidia_skills_access.json").write_text(json.dumps(artifact, indent=2))
    print(json.dumps({"ok": status == "ok", "found_count": artifact["found_count"], "samples": artifact["sample_skills"][:5], "output": str(DATA / "nvidia_skills_access.json")}, indent=2))


if __name__ == "__main__":
    main()
