from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv

REQUIRED_COLUMNS = {
    "dataset_id",
    "species",
    "geo_accession",
    "bioproject_accession",
    "biological_question",
    "analysis_role",
    "status",
}

ALLOWED_STATUS = {"planned", "validated", "ready", "excluded"}


@dataclass(frozen=True)
class ValidationResult:
    rows: int
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_dataset_manifest(path: str | Path) -> ValidationResult:
    manifest = Path(path)
    errors: list[str] = []

    if not manifest.exists():
        return ValidationResult(rows=0, errors=(f"Manifest does not exist: {manifest}",))

    with manifest.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        columns = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_COLUMNS - columns)
        if missing:
            errors.append(f"Missing required columns: {', '.join(missing)}")

        rows = list(reader)

    if not rows:
        errors.append("Manifest contains no dataset rows")

    seen_ids: set[str] = set()
    for line_number, row in enumerate(rows, start=2):
        dataset_id = (row.get("dataset_id") or "").strip()
        species = (row.get("species") or "").strip()
        geo = (row.get("geo_accession") or "").strip()
        bioproject = (row.get("bioproject_accession") or "").strip()
        status = (row.get("status") or "").strip()

        if not dataset_id:
            errors.append(f"Line {line_number}: dataset_id is required")
        elif dataset_id in seen_ids:
            errors.append(f"Line {line_number}: duplicate dataset_id '{dataset_id}'")
        else:
            seen_ids.add(dataset_id)

        if not species:
            errors.append(f"Line {line_number}: species is required")
        if not geo and not bioproject:
            errors.append(f"Line {line_number}: GEO or BioProject accession is required")
        if status not in ALLOWED_STATUS:
            errors.append(
                f"Line {line_number}: status '{status}' is invalid; "
                f"expected one of {sorted(ALLOWED_STATUS)}"
            )

    return ValidationResult(rows=len(rows), errors=tuple(errors))
