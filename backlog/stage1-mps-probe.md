# Stage1 MPS Probe

**Estado:** en progreso
**Fecha:** 2026-09-13

## Objetivo

Aislar la etapa de geometria gruesa de SAM 3D Objects y probar si puede correr en Mac/MPS o CPU sin resolver todavia gaussian splats, mesh, texturas ni postprocess.

## Alcance

- Inicializar repo `img-to-3d` con way of work adaptado.
- Documentar restricciones CUDA/MPS observadas.
- Agregar runner experimental `stage1_only`.
- Mantener el checkout upstream bajo `third_party/sam-3d-objects`, ignorado por git.
- Commit y push por incrementos.

## Fuera De Alcance

- Port completo de `spconv`.
- Mesh/GLB/textura.
- Descarga de checkpoints sin login Hugging Face.
- Validar calidad de reconstruccion.

## Archivos Afectados

- `WAY_OF_WORK.md`
- `README.md`
- `docs/README.md`
- `docs/reference/sam3d-objects-runtime-constraints.md`
- `docs/tools/stage1-only-runner.md`
- `docs/tools/local-env-setup.md`
- `requirements-mps-probe.txt`
- `tools/check_local_env.py`
- `tools/bootstrap_sam3d.py`
- `tools/download_sam3d_checkpoints.py`
- `tools/run_stage1_only.py`
- `third_party/README.md`

## Plan

1. Inicializar documentacion y backlog.
2. Agregar runner stage1-only.
3. Verificar sintaxis local.
4. Commit y push de branch.
5. Crear siguiente spec para parches MPS si el runner alcanza un bloqueo concreto.

## Checklist

- [x] Clonar `img-to-3d`.
- [x] Adaptar way of work dentro de este repo.
- [x] Crear branch `research/stage1-mps`.
- [x] Limpiar cambios locales en el checkout upstream usado para investigar.
- [x] Agregar runner.
- [x] Agregar bootstrap upstream autocontenido.
- [x] Agregar entorno minimo y checker local.
- [x] Agregar downloader de checkpoints.
- [x] Verificar sintaxis.
- [x] Commit.
- [x] Push.

## Resultado Esperado

Una base de trabajo versionada para seguir investigando SAM 3D Objects stage1 en Mac/MPS con evidencia incremental.

## Evidencia

- `rg -n "codex-mobile-tmux|\\.\\./sam-3d-objects|/Users/javierrodriguez/claude-workspace/sam-3d-objects" . || true` no encontro referencias.
- `python3 -m py_compile tools/bootstrap_sam3d.py tools/run_stage1_only.py` paso.
- Commit inicial: `f94903e Initialize stage1 MPS probe workspace`.
- Push inicial: branch `research/stage1-mps` publicada en `origin`.
- `uv venv --python 3.11 .venv` creo `.venv` con CPython 3.11.15.
- `uv pip install --python .venv/bin/python -r requirements-mps-probe.txt` instalo entorno minimo.
- `.venv/bin/python tools/check_local_env.py` reporto `mps available: True`, `torch: 2.14.0`, `sam3d config: missing`, `hf auth: Error: Not logged in`.
- `.venv/bin/python tools/run_stage1_only.py --image missing-image.png --mask missing-mask.png` fallo temprano por `third_party/sam-3d-objects/checkpoints/hf/pipeline.yaml` faltante.
- `.venv/bin/python tools/download_sam3d_checkpoints.py` fallo por repo gated sin login/acceso y limpio `checkpoints/hf-download`.
- Luego de `hf auth login`, `.venv/bin/hf auth whoami` reporto `user: Javier-godsmack`.
- `.venv/bin/python tools/download_sam3d_checkpoints.py` sigue fallando por repo gated; la cuenta esta autenticada pero todavia no tiene acceso aprobado a `facebook/sam-3d-objects`.
