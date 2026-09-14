# Way Of Work - img-to-3d

## Objetivo

Mantener el trabajo experimental sobre reconstruccion 3D reproducible, documentado y separado de los repos upstream. Cada hipotesis tecnica debe tener una ruta clara desde backlog, a codigo, a evidencia.

## Documentacion para agentes

- `docs/README.md` es un indice puro: link, una oracion de contenido y cuando abrir cada hoja.
- `README.md` resume proposito, estado actual, dependencias y mapa de docs.
- Los docs vigentes no dependen del backlog para explicar el sistema actual.
- Toda hoja no trivial abre con resumen de 3-5 lineas y vigencia.
- La informacion esencial va primero.

## Backlog

Toda idea que se transforme en plan concreto vive en `backlog/`.

| Carpeta | Uso |
|---|---|
| `backlog/` | Trabajo activo o pendiente |
| `backlog-done/` | Trabajo que llego a existir como codigo |
| `backlog-canceled/` | Investigacion o idea descartada antes de codigo funcional |

Reglas:

- Antes de un cambio relevante, crear o actualizar su spec en `backlog/`.
- Al terminar, moverlo a `backlog-done/` y actualizar `docs/`.
- Si se descarta antes de codigo funcional, moverlo a `backlog-canceled/` con motivo y alternativa.
- No cambiar el nombre al moverlo.

Formato minimo:

```markdown
# Nombre del plan

**Estado:** pendiente | en progreso | completo | cancelado
**Fecha:** YYYY-MM-DD

## Objetivo
## Alcance
## Archivos afectados
## Plan
## Checklist
## Resultado esperado
```

## Git

- Antes de editar, ejecutar `git status` y `git branch --show-current`.
- Cada cambio relevante vive en branch propia desde `main`: `research/stage1-mps`, `tools/checkpoint-download`, `fix/device-selection`.
- No hacer push directo a `main`, salvo typo trivial.
- Commits atomicos, sin `wip` ni mezclas no relacionadas.
- No reescribir historia compartida ni usar operaciones destructivas sin permiso explicito.
- Push de la branch despues de commits utiles para preservar avance.

## Evidencia

- Afirmaciones tecnicas trazables a codigo, comando, log, medicion o fuente primaria.
- Distinguir hipotesis de resultado validado.
- Registrar comandos ejecutados y bloqueos en el spec activo.
- Si no hay checkpoints o entorno, declarar "preparado; pendiente ejecucion", no "funciona".

## Definition Of Done

- `README.md` y `docs/README.md` apuntan a la informacion vigente.
- El spec activo refleja estado, comandos y resultado.
- El codigo experimental tiene un comando de verificacion minimo.
- El repo upstream no queda modificado por experimentos locales.
- La branch tiene commits atomicos y fue pusheada.
