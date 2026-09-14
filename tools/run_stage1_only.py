#!/usr/bin/env python3
"""Experimental SAM 3D Objects stage1-only runner.

This runner lives outside the upstream repo on purpose. It tries to exercise the
geometry stage only and exports predicted voxel centers as a simple PLY point
cloud if inference succeeds.
"""

from __future__ import annotations

import argparse
import builtins
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image


def choose_device() -> str:
    import torch

    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_rgb(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB"), dtype=np.uint8)


def load_mask(path: Path) -> np.ndarray:
    mask = np.array(Image.open(path).convert("L"), dtype=np.uint8)
    return (mask > 127).astype(np.uint8) * 255


def write_voxel_ply(path: Path, voxels: np.ndarray) -> None:
    voxels = np.asarray(voxels, dtype=np.float32)
    header = "\n".join(
        [
            "ply",
            "format ascii 1.0",
            f"element vertex {len(voxels)}",
            "property float x",
            "property float y",
            "property float z",
            "end_header",
        ]
    )
    with path.open("w", encoding="ascii") as f:
        f.write(header)
        f.write("\n")
        for x, y, z in voxels:
            f.write(f"{x:.8f} {y:.8f} {z:.8f}\n")


def check_hydra_safety(config) -> None:
    from hydra.utils import get_method
    from omegaconf import DictConfig, ListConfig

    blacklist = {
        builtins.exec,
        builtins.eval,
        builtins.__import__,
        os.kill,
        os.system,
        os.putenv,
        os.remove,
        os.removedirs,
        os.rmdir,
        os.fchdir,
        os.setuid,
        os.fork,
        os.forkpty,
        os.killpg,
        os.rename,
        os.renames,
        os.truncate,
        os.replace,
        os.unlink,
        os.fchmod,
        os.fchown,
        os.chmod,
        os.chown,
        os.chroot,
        os.lchown,
        os.getcwd,
        os.chdir,
        shutil.rmtree,
        shutil.move,
        shutil.chown,
        subprocess.Popen,
        builtins.help,
    }

    to_check = [config]
    while to_check:
        node = to_check.pop()
        if isinstance(node, DictConfig):
            to_check.extend(list(node.values()))
            target = node.get("_target_")
            if target is None:
                continue
            package = target.split(".", 1)[0]
            if package not in {"sam3d_objects", "torch", "torchvision", "moge"}:
                raise RuntimeError(f"Hydra target is not allowlisted: {target}")
            if get_method(target) in blacklist:
                raise RuntimeError(f"Hydra target is blocklisted: {target}")
        elif isinstance(node, ListConfig):
            to_check.extend(list(node))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sam3d-repo",
        default="third_party/sam-3d-objects",
        help="Path to a local facebookresearch/sam-3d-objects checkout.",
    )
    parser.add_argument(
        "--config",
        default="third_party/sam-3d-objects/checkpoints/hf/pipeline.yaml",
        help="Path to downloaded SAM 3D Objects pipeline.yaml.",
    )
    parser.add_argument("--image", required=True, help="Input RGB image.")
    parser.add_argument("--mask", required=True, help="Binary object mask.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default=None, choices=["cuda", "mps", "cpu"])
    parser.add_argument("--output", default="stage1_voxels.ply")
    args = parser.parse_args()

    sam3d_repo = Path(args.sam3d_repo).resolve()
    if not sam3d_repo.exists():
        raise FileNotFoundError(f"Missing SAM 3D Objects repo: {sam3d_repo}")
    sys.path.insert(0, str(sam3d_repo))

    os.environ.setdefault("ATTN_BACKEND", "sdpa")
    os.environ.setdefault("SPARSE_ATTN_BACKEND", "sdpa")
    os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
    os.environ.setdefault("LIDRA_SKIP_INIT", "true")

    config_path = Path(args.config).resolve()
    if not config_path.exists():
        raise FileNotFoundError(
            f"Missing {config_path}. Download checkpoints from Hugging Face first."
        )

    import torch
    from hydra.utils import instantiate
    from omegaconf import OmegaConf

    import sam3d_objects  # noqa: F401

    device = args.device or choose_device()
    config = OmegaConf.load(config_path)
    config.rendering_engine = "pytorch3d"
    config.compile_model = False
    config.workspace_dir = str(config_path.parent)
    config.device = device

    if device != "cuda":
        config.dtype = "float32"
        config.shape_model_dtype = "float32"

    check_hydra_safety(config)
    pipeline = instantiate(config)

    image = load_rgb(Path(args.image))
    mask = load_mask(Path(args.mask))

    with torch.inference_mode():
        output = pipeline.run(
            image,
            mask,
            seed=args.seed,
            stage1_only=True,
            stage1_inference_steps=None,
        )

    voxels = output["voxel"].detach().cpu().numpy()
    write_voxel_ply(Path(args.output), voxels)

    print(f"wrote {len(voxels)} voxel centers to {args.output}")
    for key in ("translation", "rotation", "scale"):
        if key in output:
            value = output[key].detach().cpu().numpy()
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
