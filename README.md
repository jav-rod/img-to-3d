# img-to-3d

Experimentos para correr reconstruccion 3D desde imagen en hardware local, empezando por aislar el `stage1_only` de SAM 3D Objects para probar si la etapa de geometria gruesa puede correr en Mac/MPS o CPU.

Estado actual: repo inicializado, sin checkpoints incluidos. El objetivo inmediato es validar la primera etapa del modelo, que devuelve voxels `64^3` y pose/layout, antes de intentar gaussian splats, mesh o texturas.

## Mapa

- [Way of work](WAY_OF_WORK.md): reglas de backlog, docs, evidencia y git.
- [Docs index](docs/README.md): indice canonico de documentacion vigente.
- [Restricciones SAM 3D Objects](docs/reference/sam3d-objects-runtime-constraints.md): bloqueo CUDA/MPS observado en el repo upstream.
- [Local env setup](docs/tools/local-env-setup.md): entorno minimo para smoke tests en Mac/MPS.
- [Stage1 runner](docs/tools/stage1-only-runner.md): uso esperado de la herramienta experimental.
- [Plan activo](backlog/stage1-mps-probe.md): alcance, checklist y evidencia pendiente.
- [Third party](third_party/README.md): ubicacion canonica para checkouts upstream locales.

## Estado De Ejecucion

No hay ejecucion de modelo todavia porque faltan:

- checkpoints de Hugging Face para `facebook/sam-3d-objects`;
- entorno Python con PyTorch y dependencias minimas;
- prueba local de imports en este repo.

El checkout upstream debe vivir en `third_party/sam-3d-objects` y se materializa con:

```bash
python tools/bootstrap_sam3d.py
```

Verificar entorno local:

```bash
python tools/check_local_env.py
```

Bajar checkpoints despues de autenticar Hugging Face:

```bash
python tools/download_sam3d_checkpoints.py
```
