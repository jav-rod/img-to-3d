# Stage1-only Runner

**Vigencia:** herramienta experimental inicial, pendiente de ejecucion con checkpoints reales.

El runner `tools/run_stage1_only.py` intenta cargar el pipeline de SAM 3D Objects y pedir solo `stage1_only=True`. Su objetivo es producir una nube PLY con centros de voxels, sin gaussian splats, mesh, textura ni postprocess.

## Uso Esperado

```bash
python tools/run_stage1_only.py \
  --sam3d-repo third_party/sam-3d-objects \
  --config third_party/sam-3d-objects/checkpoints/hf/pipeline.yaml \
  --image path/to/image.png \
  --mask path/to/mask.png \
  --device mps \
  --output stage1_voxels.ply
```

## Salida

- `stage1_voxels.ply`: point cloud ASCII con centros de voxels normalizados.
- `translation`, `rotation`, `scale` impresos por stdout si el pipeline los devuelve.

## Limitaciones

- Requiere checkpoints descargados; este repo no los versiona.
- Todavia puede fallar por CUDA hardcodeado en el pipeline upstream.
- No evita automaticamente dependencias importadas por configs Hydra.
- No implementa reemplazo para `spconv`.

## Bootstrap Upstream

```bash
python tools/bootstrap_sam3d.py
```

## Validacion Pendiente

- Crear entorno Python con PyTorch.
- Confirmar disponibilidad MPS.
- Ejecutar sin checkpoints para verificar error esperado.
- Ejecutar con checkpoints y registrar primer bloqueo real.
