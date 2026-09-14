#!/usr/bin/env python3
"""Report local readiness for the stage1 MPS probe."""

from __future__ import annotations

import importlib.util
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def command_output(cmd: list[str]) -> str:
    try:
        result = subprocess.run(
            cmd,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except FileNotFoundError:
        return "missing"
    return result.stdout.strip() or f"exit={result.returncode}"


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    sam3d = root / "third_party" / "sam-3d-objects"
    config = sam3d / "checkpoints" / "hf" / "pipeline.yaml"

    print(f"platform: {platform.platform()}")
    print(f"python: {sys.version.split()[0]}")
    print(f"repo: {root}")
    print(f"sam3d checkout: {'ok' if sam3d.exists() else 'missing'} ({sam3d})")
    print(f"sam3d config: {'ok' if config.exists() else 'missing'} ({config})")
    print(f"hf cli: {shutil.which('hf') or 'missing'}")
    print(f"hf auth: {command_output(['hf', 'auth', 'whoami'])}")

    if not has_module("torch"):
        print("torch: missing")
        return

    import torch

    print(f"torch: {torch.__version__}")
    print(f"cuda available: {torch.cuda.is_available()}")
    print(f"mps built: {torch.backends.mps.is_built()}")
    print(f"mps available: {torch.backends.mps.is_available()}")


if __name__ == "__main__":
    main()
