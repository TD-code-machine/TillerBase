CREATE TABLE IF NOT EXISTS studies (
    study_id TEXT PRIMARY KEY,
    species TEXT NOT NULL,
    geo_accession TEXT,
    bioproject_accession TEXT,
    biological_question TEXT NOT NULL,
    analysis_role TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS samples (
    sample_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL REFERENCES studies(study_id),
    run_accession TEXT UNIQUE,
    biosample_accession TEXT,
    genotype TEXT,
    tissue TEXT,
    treatment TEXT,
    timepoint TEXT,
    replicate TEXT,
    library_layout TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS contrasts (
    contrast_id TEXT PRIMARY KEY,
    study_id TEXT NOT NULL REFERENCES studies(study_id),
    numerator_label TEXT NOT NULL,
    denominator_label TEXT NOT NULL,
    design_formula TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS differential_expression (
    contrast_id TEXT NOT NULL REFERENCES contrasts(contrast_id),
    gene_id TEXT NOT NULL,
    log2_fold_change DOUBLE PRECISION,
    p_value DOUBLE PRECISION,
    adjusted_p_value DOUBLE PRECISION,
    base_mean DOUBLE PRECISION,
    PRIMARY KEY (contrast_id, gene_id)
);

CREATE TABLE IF NOT EXISTS orthologues (
    species TEXT NOT NULL,
    gene_id TEXT NOT NULL,
    orthogroup_id TEXT NOT NULL,
    reference_gene_id TEXT,
    mapping_source TEXT,
    PRIMARY KEY (species, gene_id, orthogroup_id)
);
