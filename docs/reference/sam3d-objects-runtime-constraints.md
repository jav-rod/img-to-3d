# SAM 3D Objects Runtime Constraints

**Vigencia:** investigacion inicial contra `facebookresearch/sam-3d-objects` el 2026-09-13.

SAM 3D Objects no esta preparado upstream para Mac/MPS. La restriccion importante no es solo el device de PyTorch, sino el stack CUDA alrededor de sparse tensors, rasterizacion y postprocess. La etapa `stage1_only` es el recorte mas prometedor porque evita textura, gaussian splats, mesh refinement y GLB.

## Restricciones Estructurales

- `sam3d_objects/model/backbone/tdfy_dit/modules/sparse/__init__.py` fija `BACKEND = "spconv"` por default.
- `sam3d_objects/model/backbone/tdfy_dit/modules/sparse/basic.py` importa `spconv.pytorch` cuando el backend es `spconv`.
- El checkout menciona `torchsparse`, pero no trae implementacion `conv_torchsparse.py`; no hay backend alternativo funcional listo.
- `requirements.txt` incluye `spconv-cu121`, `cuda-python` y `nvidia-cuda-nvcc-cu12`.
- `requirements.p3d.txt` incluye `flash_attn`.
- `requirements.inference.txt` incluye `kaolin` y `gsplat`.

## Restricciones Accidentales

Estas son candidatas a parche local:

- `device="cuda"` como default en pipeline y modelos auxiliares.
- `torch.cuda.current_device()` durante inicializacion.
- `load_file(..., device="cuda")` para `.safetensors`.
- `torch.autocast(device_type="cuda", ...)` en stage1/stage2 y pointmap.
- Varios `.cuda()` en render, postprocess y utilidades de visualizacion.

## Recorte Inicial

`stage1_only=True` devuelve:

- `coords`: voxels ocupados en grilla sparse `64^3`.
- `voxel`: centros normalizados por `coords[:, 1:] / 64 - 0.5`.
- `rotation`, `translation`, `scale`: pose/layout del objeto.
- `pointmap` y `pointmap_colors` en el pipeline con pointmap.

No devuelve textura, gaussian splat, mesh ni GLB.

## Hipotesis

La primera meta practica es correr solo stage1 en MPS/CPU. Si eso funciona, la salida ya puede visualizarse como nube de puntos o voxel mesh basica. Stage2 requiere resolver o reemplazar `spconv`, que es un trabajo mayor.

## Validado Contra

- Checkout esperado: `third_party/sam-3d-objects`, materializado con `tools/bootstrap_sam3d.py`.
- Archivos inspeccionados: `doc/setup.md`, `requirements*.txt`, `sam3d_objects/pipeline/inference_pipeline.py`, `sam3d_objects/pipeline/inference_pipeline_pointmap.py`, `sam3d_objects/model/backbone/tdfy_dit/modules/sparse/*`.
