# TillerBase

**TillerBase** is a reproducible bioinformatics project for integrating public grass tillering and axillary-bud transcriptomics datasets across species.

The project is designed as a portfolio-quality analysis platform rather than a one-off notebook: public RNA-seq studies are described in a structured manifest, processed through a Nextflow workflow, analysed within study, mapped to orthologue groups, and then compared across species to identify conserved regulators of tiller-bud activation.

## Scientific question

**Which transcriptional programmes are conserved when a dormant or arrested grass axillary bud transitions into an actively growing tiller?**

The initial cohort focuses on sorghum, wheat and rice studies that perturb bud activation, branching or tillering. The first objective is not to pool raw counts across heterogeneous experiments. Instead, TillerBase estimates contrasts independently within each study and compares effect directions and orthologous gene-level signals downstream.

## Initial public datasets

| Species | GEO / BioProject | Biological contrast | Role in TillerBase |
|---|---|---|---|
| *Sorghum bicolor* | GSE79389 / PRJNA315679 | Growing versus arrested axillary buds in WT / `phyB-1` context | Developmental-state contrast |
| *Sorghum bicolor* | GSE127822 / PRJNA525462 | Bud activation following leaf removal (1 h, 3 h, 6 h) | Early activation time course |
| *Triticum aestivum* | GSE124767 / PRJNA513351 | `TaD27` / strigolactone-related tillering perturbation | Hormonal branching regulation |
| *Oryza sativa* | GSE178359 / PRJNA738596 | Axillary-meristem genotype comparison | Genetic control of shoot branching |
| *Oryza sativa* | PRJNA1247236 | Effective versus ineffective tillers; multi-omics study | Tiller-state validation / extension |

> Dataset metadata will be validated before any automated download or analysis. Public accession IDs are tracked separately from analysis-ready sample metadata so corrections can be made without changing the workflow code.

## Architecture

```text
Public SRA / GEO studies
        |
        v
metadata/datasets.tsv
        |
        v
Nextflow ingestion + QC
        |
        +--> FastQC / MultiQC
        +--> trimming (optional)
        +--> STAR/HISAT2 or transcript quantification
        |
        v
study-level expression matrices
        |
        v
within-study differential expression
        |
        v
orthologue mapping + harmonisation
        |
        v
cross-study conserved-signature analysis
        |
        +--> ranked conserved genes
        +--> pathway enrichment
        +--> regulatory-network candidates
        +--> visual summaries
```

## Repository layout

```text
TillerBase/
├── .github/workflows/ci.yml
├── config/
│   └── nextflow.config
├── database/
│   └── schema.sql
├── metadata/
│   └── datasets.tsv
├── modules/
│   ├── fastqc.nf
│   └── multiqc.nf
├── src/tillerbase/
│   ├── __init__.py
│   ├── cli.py
│   └── metadata.py
├── tests/
│   └── test_metadata.py
├── .gitignore
├── Dockerfile
├── LICENSE
├── main.nf
├── pyproject.toml
└── README.md
```

## Quick start

### Python metadata tooling

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
tillerbase validate metadata/datasets.tsv
```

### Nextflow dry run

```bash
nextflow run main.nf -profile test
```

## Design principles

1. **Analyse studies independently first.** Batch, genotype, tissue, time point and library effects remain study-specific.
2. **Compare biological effects, not raw counts.** Cross-study integration is performed using differential-expression statistics and orthologue mappings.
3. **Make metadata explicit.** Every sample and contrast should be machine-readable and traceable to a public accession.
4. **Keep the workflow reproducible.** Nextflow, containers, versioned configuration and CI are used from the start.
5. **Separate evidence from interpretation.** The database stores provenance and computed outputs so downstream biological claims can be traced to source studies.

## Planned milestones

### v0.1 — scaffold
- [x] Python package and CLI
- [x] metadata schema and validation
- [x] Nextflow workflow structure
- [x] Docker environment
- [x] PostgreSQL starter schema
- [x] unit tests and GitHub Actions CI
- [x] initial public dataset cohort

### v0.2 — reproducible ingestion
- [ ] Resolve run-level SRA accessions for each study
- [ ] Add automated ENA/SRA metadata retrieval
- [ ] Download FASTQ subsets for a small reproducible test dataset
- [ ] FastQC + MultiQC
- [ ] reference-genome configuration by species

### v0.3 — expression analysis
- [ ] Quantification / alignment workflow
- [ ] study-specific count matrices
- [ ] DESeq2-compatible design metadata
- [ ] automated contrast definitions
- [ ] QC report generation

### v0.4 — TillerNet conserved signature
- [ ] orthologue mapping across sorghum, wheat and rice
- [ ] effect-direction concordance analysis
- [ ] rank aggregation / meta-analysis
- [ ] GO / pathway enrichment
- [ ] candidate regulatory network

### v1.0 — searchable tillering atlas
- [ ] PostgreSQL-backed results store
- [ ] API endpoints
- [ ] interactive visualisation layer
- [ ] documented reproducible release

## Why this project exists

Tillering is controlled by conserved developmental and hormonal pathways, but the relevant transcriptomic evidence is distributed across species, genotypes and experiments. TillerBase aims to turn those disconnected studies into a reproducible cross-species resource while demonstrating production-style bioinformatics skills: Linux workflows, RNA-seq processing, Python, Nextflow, containers, databases, testing and CI.

## Status

Early development. The current repository establishes the project architecture and dataset manifest; biological conclusions should not be drawn until the study metadata and raw-data mappings have been independently verified and the analysis workflow has been run.

## License

MIT License.
