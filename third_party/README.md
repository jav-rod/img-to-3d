# Third Party Dependencies

This directory is the canonical place for local upstream checkouts used by this repo.

## SAM 3D Objects

Materialize the upstream repo with:

```bash
python tools/bootstrap_sam3d.py
```

Expected path:

```text
third_party/sam-3d-objects
```

The checkout and downloaded checkpoints are ignored by git. Local patches should live in this repo as scripts, docs, or patch files until we intentionally decide to vendor a source snapshot.
