"""End-to-end validation against a real PostgreSQL server.

Moved here from core's tests/test_pg_e2e.py when these handlers became a plugin.

Prerequisites:
    docker run -d --name pg13-e2e -e POSTGRES_PASSWORD=postgres \\
        -e POSTGRES_DB=dbwarden_test -p 15432:5432 postgres:13-alpine

Run:
    DBWARDEN_E2E=1 python -m pytest tests/test_pg_e2e.py -v
"""

import os

import pytest
import sqlalchemy as sa

PG_URL = "postgresql://postgres:postgres@localhost:15432/dbwarden_test"

pytestmark = pytest.mark.skipif(
    not os.environ.get("DBWARDEN_E2E"),
    reason="set DBWARDEN_E2E=1 to run PG end-to-end tests",
)


@pytest.fixture(scope="module")
def engine():
    e = sa.create_engine(PG_URL)
    yield e
    e.dispose()


@pytest.fixture(scope="module")
def snap(engine):
    return _refresh()


def _refresh():
    from dbwarden.engine.snapshot import extract_full_schema_snapshot

    return extract_full_schema_snapshot(
        sqlalchemy_url=PG_URL,
        database_type="postgresql",
    )


def _drop(*names):
    e = sa.create_engine(PG_URL)
    with e.begin() as conn:
        for n in names:
            for tmpl in (
                "DROP TABLE IF EXISTS {n} CASCADE",
                "DROP TYPE IF EXISTS {n} CASCADE",
            ):
                try:
                    conn.execute(sa.text(tmpl.format(n=n)))
                except Exception:
                    pass
    e.dispose()


def test_domain_extraction(engine, snap):
    from dbwarden_pgsql_types import DomainHandler

    assert isinstance(DomainHandler().extract(snap), dict)


def test_enum_extraction(engine, snap):
    from dbwarden_pgsql_types import EnumHandler

    assert isinstance(EnumHandler().extract(snap), dict)


def test_sequence_extraction(engine, snap):
    from dbwarden_pgsql_types import SequenceHandler

    assert isinstance(SequenceHandler().extract(snap), dict)


def test_composite_type_extraction(engine, snap):
    from dbwarden_pgsql_types import CompositeTypeHandler

    _drop("e2e_comp")
    with engine.begin() as conn:
        conn.execute(sa.text("CREATE TYPE e2e_comp AS (a int, b text)"))

    try:
        spec = CompositeTypeHandler().extract(_refresh())
        assert "e2e_comp" in spec, f"e2e_comp not found in {list(spec.keys())}"
        cols = spec["e2e_comp"]["columns"]
        assert any(c["name"] == "a" and "int" in c["type"] for c in cols)
        assert any(c["name"] == "b" and "text" in c["type"] for c in cols)
    finally:
        _drop("e2e_comp")
