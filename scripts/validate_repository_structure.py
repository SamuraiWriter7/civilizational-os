#!/usr/bin/env python3
"""
Validate repository structure for Civilizational OS.

This script checks whether required documentation, schemas, examples,
scripts, and GitHub Actions workflow files exist.

It is intended to complement scripts/validate_examples.py.

Checks:

* README.md
* CHANGELOG.md
* required docs/
* required schemas/
* required examples/
* validation scripts
* GitHub Actions workflow
  """

from **future** import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(**file**).resolve().parents[1]

REQUIRED_FILES = [
"README.md",
"CHANGELOG.md",

```
# Documentation
"docs/civilizational-os-requirements-v0.1.md",
"docs/architecture-overview.md",
"docs/dynamic-equilibrium.md",
"docs/trace-and-royalty-layer.md",
"docs/validation-and-cooling.md",
"docs/multi-wing-governance.md",

# Schemas
"schemas/equilibrium-state.schema.json",
"schemas/trace-and-royalty-record.schema.json",
"schemas/validation-record.schema.json",

# Examples
"examples/equilibrium-state.example.yaml",
"examples/trace-and-royalty-record.example.yaml",
"examples/validation-record.example.yaml",

# Scripts
"scripts/validate_examples.py",
"scripts/validate_repository_structure.py",

# GitHub Actions
".github/workflows/validate-examples.yml",
```

]

REQUIRED_DIRECTORIES = [
"docs",
"schemas",
"examples",
"scripts",
".github",
".github/workflows",
]

def check_required_directories() -> list[str]:
"""Return a list of missing required directories."""
missing: list[str] = []

```
for relative_path in REQUIRED_DIRECTORIES:
    path = REPO_ROOT / relative_path
    if not path.exists():
        missing.append(relative_path)
    elif not path.is_dir():
        missing.append(f"{relative_path} exists but is not a directory")

return missing
```

def check_required_files() -> list[str]:
"""Return a list of missing required files."""
missing: list[str] = []

```
for relative_path in REQUIRED_FILES:
    path = REPO_ROOT / relative_path
    if not path.exists():
        missing.append(relative_path)
    elif not path.is_file():
        missing.append(f"{relative_path} exists but is not a file")

return missing
```

def print_section(title: str) -> None:
"""Print a readable section header."""
print(title)
print("-" * len(title))

def main() -> int:
"""Run repository structure validation."""
print("Civilizational OS repository structure validation")
print("=" * 55)
print()

```
print_section("Checking required directories")
missing_directories = check_required_directories()

if missing_directories:
    for item in missing_directories:
        print(f"Missing directory: {item}")
else:
    print("All required directories exist.")

print()

print_section("Checking required files")
missing_files = check_required_files()

if missing_files:
    for item in missing_files:
        print(f"Missing file: {item}")
else:
    print("All required files exist.")

print()

if missing_directories or missing_files:
    print("Repository structure validation failed.", file=sys.stderr)
    return 1

print("Repository structure validation passed.")
return 0
```

if **name** == "**main**":
raise SystemExit(main())
