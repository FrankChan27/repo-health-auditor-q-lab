# GitHub Repo Health Auditor

A lightweight CLI tool to assess basic engineering health of local Git repositories.

## Features

Checks for:
- **README** file existence (case-insensitive: README, README.md, README.rst, etc.)
- **Tests** presence using standard conventions
- **CI configuration** (GitHub Actions, GitLab CI, CircleCI, Jenkins)
- **Metadata files** (package.json, pyproject.toml, setup.py, go.mod, Cargo.toml, pom.xml)
- **Ecosystem detection** via metadata file mapping

## Installation

No external dependencies required. Uses Python standard library only.

Requirements:
- Python 3.7+

## Usage

Basic usage:
```bash
python health_checker.py /path/to/repository
```

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `repo_path` | Path to local git repository (required) | - |
| `-f, --format` | Output format: `json`, `text`, or `markdown` | `text` |
| `-o, --output` | Output file path | stdout |

### Examples

Check current directory with text output:
```bash
python health_checker.py .
```

Generate JSON report:
```bash
python health_checker.py /path/to/repo --format json
```

Save Markdown report to file:
```bash
python health_checker.py /path/to/repo --format markdown --output report.md
```

## Output Formats

### Text Format (default)

Human-readable plain text output:
```
============================================================
Repository Health Report
============================================================
Path: /path/to/repository

README: YES
Tests: YES
CI Config: YES
  github: ci.yml
Metadata: FOUND
  package.json
Ecosystems: Node.js

Health Score: 4/4
============================================================
```

### JSON Format

Machine-readable structured output:
```json
{
  "path": "/path/to/repository",
  "readme": true,
  "tests": true,
  "ci": true,
  "ci_details": {"github": ["ci.yml"]},
  "metadata": {"package.json": true, "go.mod": false, ...},
  "no_metadata": false,
  "ecosystems": ["Node.js"],
  "score": "4/4"
}
```

### Markdown Format

Markdown-formatted report with emojis:
```markdown
# Repository Health Report

**Path:** `/path/to/repository`

## Checks

- README: ✅
- Tests: ✅
...
```

## Running Tests

Run the automated test suite:
```bash
python test_health_checker.py
```

All tests should pass in a clean Python environment with no external dependencies.
