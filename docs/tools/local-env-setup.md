# Local Environment Setup

**Vigencia:** setup inicial para macOS/MPS, pendiente de inferencia real con checkpoints.

Este repo usa un entorno local chico para probar la etapa `stage1_only` antes de intentar instalar el stack completo de SAM 3D Objects. El entorno no incluye `spconv`, `kaolin`, `gsplat`, `flash_attn` ni otros paquetes CUDA-only.

## Crear Entorno

Preferido con `uv`:

```bash
uv venv --python 3.11 .venv
source .venv/bin/activate
uv pip install -r requirements-mps-probe.txt
```

Fallback con Python disponible:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-mps-probe.txt
```

## Verificar

```bash
python tools/check_local_env.py
```

El resultado esperado antes de bajar checkpoints es:

- `sam3d checkout: ok`
- `sam3d config: missing`
- `mps available: True` en Mac compatible
- `hf auth` puede decir `Not logged in` hasta autenticar Hugging Face

## Checkpoints

SAM 3D Objects esta gated en Hugging Face. Primero autenticar y tener acceso aprobado:

```bash
hf auth login
python tools/download_sam3d_checkpoints.py
```

Destino esperado:

```text
third_party/sam-3d-objects/checkpoints/hf/pipeline.yaml
```

## Limite

Este entorno solo valida tooling y dependencias PyTorch/MPS. La inferencia stage1 puede requerir parches adicionales sobre el pipeline upstream porque todavia hay `cuda` hardcodeado en SAM 3D Objects.

## Validado Contra

- Creado para `img-to-3d` branch `research/stage1-mps`.
- `.venv` con CPython 3.11.15 via `uv`.
