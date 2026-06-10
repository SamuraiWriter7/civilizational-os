#!/usr/bin/env python3
"""
Validate YAML examples against JSON Schemas for Civilizational OS.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

REPO_ROOT = Path(__file__).resolve().parents[1]

VALIDATION_TARGETS = [
    {
        "name": "Equilibrium State",
        "schema": "schemas/equilibrium-state.schema.json",
        "example": "examples/equilibrium-state.example.yaml",
    },
    {
        "name": "Trace and Royalty Record",
        "schema": "schemas/trace-and-royalty-record.schema.json",
        "example": "examples/trace-and-royalty-record.example.yaml",
    },
    {
        "name": "Validation Record",
        "schema": "schemas/validation-record.schema.json",
        "example": "examples/validation-record.example.yaml",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON file."""
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise RuntimeError(f"JSON file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {path}: {exc}") from exc


def load_yaml(path: Path) -> Any:
    """Load a YAML file."""
    try:
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except FileNotFoundError as exc:
        raise RuntimeError(f"YAML file not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise RuntimeError(f"Invalid YAML in {path}: {exc}") from exc


def format_validation_path(error: ValidationError) -> str:
    """Format the path where validation failed."""
    if not error.absolute_path:
        return "<root>"
    return ".".join(str(part) for part in error.absolute_path)


def validate_example(name: str, schema_path: Path, example_path: Path) -> None:
    """Validate one YAML example against one JSON Schema."""
    print(f"Validating target: {name}")
    print(f"Validating example: {example_path.relative_to(REPO_ROOT)}")
    print(f"Using schema: {schema_path.relative_to(REPO_ROOT)}")

    schema = load_json(schema_path)
    example = load_yaml(example_path)

    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )

    errors = sorted(
        validator.iter_errors(example),
        key=lambda err: list(err.absolute_path),
    )

    if errors:
        first_error = errors[0]
        error_path = format_validation_path(first_error)

        raise RuntimeError(
            "\n".join(
                [
                    "Validation failed.",
                    f"Target: {name}",
                    f"Path: {error_path}",
                    f"Error: {first_error.message}",
                ]
            )
        )

    print("Validation passed.\n")


def main() -> int:
    """Run all validation targets."""
    print("Civilizational OS example validation")
    print("=" * 40)
    print()

    try:
        for target in VALIDATION_TARGETS:
            schema_path = REPO_ROOT / target["schema"]
            example_path = REPO_ROOT / target["example"]

            validate_example(
                name=target["name"],
                schema_path=schema_path,
                example_path=example_path,
            )

    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print("All examples passed validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

