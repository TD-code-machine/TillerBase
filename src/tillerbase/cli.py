from __future__ import annotations

import argparse
from pathlib import Path

from .metadata import validate_dataset_manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tillerbase",
        description="Utilities for the TillerBase cross-species tillering project.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate a dataset manifest")
    validate.add_argument("manifest", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.command == "validate":
        result = validate_dataset_manifest(args.manifest)
        if result.ok:
            print(f"OK: {result.rows} dataset rows validated")
            return 0
        for error in result.errors:
            print(f"ERROR: {error}")
        return 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
