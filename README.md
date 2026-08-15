# dbwarden-pgsql-types

[![Python](https://img.shields.io/badge/Python-3.12.7%2B-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/dbwarden-pgsql-types?logo=pypi&logoColor=white&style=for-the-badge)](https://pypi.org/project/dbwarden-pgsql-types/)
[![CI](https://img.shields.io/github/actions/workflow/status/dbwarden-org/dbwarden-pgsql-types/test.yml?logo=github&logoColor=white&style=for-the-badge)](https://github.com/dbwarden-org/dbwarden-pgsql-types/actions/workflows/test.yml)

PostgreSQL custom type and sequence object handlers for [dbwarden](https://github.com/dbwarden-org/dbwarden).

## Object types

| Object type | Manages |
|---|---|
| `enum` | `CREATE TYPE ... AS ENUM`, plus `ADD VALUE` for additive changes |
| `domain` | `CREATE/ALTER/DROP DOMAIN`, with constraints and defaults |
| `composite_type` | `CREATE/ALTER/DROP TYPE ... AS (...)` |
| `sequence` | `CREATE/ALTER/DROP SEQUENCE`, including start, increment, bounds, and cycle |

Enums register first, because domains and composite types can be defined over them.

## Installation

```bash
dbwarden plugin add dbwarden-pgsql-types
```

## Trust tier

This is an **official** dbwarden plugin. Its distribution name is classified before any of its code is imported, and `dbwarden plugin add` verifies the PyPI Trusted-Publishing attestation (PEP 740) against `dbwarden-org/dbwarden-pgsql-types` before installing. It loads automatically once installed, with no `dbwarden plugin trust` step.

## Development

```bash
uv venv && uv pip install -e . -e ../dbwarden pytest
pytest -q
```

The `tests/test_conformance.py` suite runs dbwarden's shared conformance harness (`dbwarden.plugin_conformance`): entry point resolution, no import-time side effects, hook signatures, public-API-only imports, and idempotent `setup()`.

## License

MIT
