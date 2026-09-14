#!/usr/bin/env python3
"""Download SAM 3D Objects checkpoints into the local third_party checkout."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from huggingface_hub import snapshot_download
from huggingface_hub.errors import GatedRepoError


DEFAULT_REPO_ID = "facebook/sam-3d-objects"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", default=DEFAULT_REPO_ID)
    parser.add_argument("--sam3d-repo", default="third_party/sam-3d-objects")
    parser.add_argument("--tag", default="hf")
    parser.add_argument("--max-workers", type=int, default=1)
    parser.add_argument(
        "--keep-partial",
        action="store_true",
        help="Keep the temporary download directory if the download fails.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    sam3d_repo = (root / args.sam3d_repo).resolve()
    if not sam3d_repo.exists():
        raise FileNotFoundError(
            f"Missing {sam3d_repo}. Run tools/bootstrap_sam3d.py first."
        )

    checkpoints_dir = sam3d_repo / "checkpoints"
    final_dir = checkpoints_dir / args.tag
    download_dir = checkpoints_dir / f"{args.tag}-download"

    if final_dir.exists():
        print(f"already exists: {final_dir}")
        return

    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    try:
        snapshot_download(
            repo_id=args.repo_id,
            repo_type="model",
            local_dir=download_dir,
            max_workers=args.max_workers,
        )
    except GatedRepoError as exc:
        if download_dir.exists() and not args.keep_partial:
            shutil.rmtree(download_dir)
        raise SystemExit(
            "Cannot access gated Hugging Face repo. Request access to "
            f"{args.repo_id}, run `hf auth login`, then retry."
        ) from exc
    except Exception:
        if download_dir.exists() and not args.keep_partial:
            shutil.rmtree(download_dir)
        raise

    nested_checkpoints = download_dir / "checkpoints"
    if not nested_checkpoints.exists():
        raise FileNotFoundError(
            f"Download completed, but expected {nested_checkpoints} was not found."
        )

    shutil.move(str(nested_checkpoints), str(final_dir))
    shutil.rmtree(download_dir)
    print(f"downloaded checkpoints to {final_dir}")


if __name__ == "__main__":
    main()
