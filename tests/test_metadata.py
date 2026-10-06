from pathlib import Path

from tillerbase.metadata import validate_dataset_manifest


def test_repository_manifest_is_valid() -> None:
    result = validate_dataset_manifest(Path("metadata/datasets.tsv"))
    assert result.ok, result.errors
    assert result.rows >= 5


def test_duplicate_dataset_ids_are_rejected(tmp_path: Path) -> None:
    manifest = tmp_path / "datasets.tsv"
    manifest.write_text(
        "dataset_id\tspecies\tgeo_accession\tbioproject_accession\tbiological_question\tanalysis_role\tstatus\n"
        "dup\tSorghum bicolor\tGSE1\t\tQuestion\trole\tplanned\n"
        "dup\tOryza sativa\tGSE2\t\tQuestion\trole\tplanned\n",
        encoding="utf-8",
    )
    result = validate_dataset_manifest(manifest)
    assert not result.ok
    assert any("duplicate dataset_id" in error for error in result.errors)
