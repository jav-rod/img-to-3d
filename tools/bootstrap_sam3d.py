#!/usr/bin/env python3
"""Materialize third-party SAM 3D Objects under this repo."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


DEFAULT_REPO = "https://github.com/facebookresearch/sam-3d-objects.git"


def run(cmd: list[str], cwd: Path) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--dest", default="third_party/sam-3d-objects")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    dest = root / args.dest
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists():
        print(f"already exists: {dest}")
        return

    run(["git", "clone", args.repo, str(dest)], cwd=root)


if __name__ == "__main__":
    main()
