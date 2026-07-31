"""Snapshot-diff coverage moved here from core's tests/engine/snapshot/test_backend.py."""

from __future__ import annotations

from dbwarden.engine.core import ModelColumn, ModelTable
from dbwarden.engine.snapshot import diff_models_against_snapshot, snapshot_diff_to_sql


def _mc(name: str, typ: str, pk: bool = False, nullable: bool = True) -> ModelColumn:
    return ModelColumn(name, typ, nullable, pk, False, None, None)


class TestPGDomainSequenceOps:
    def test_create_domain_op(self):
        ops = [
            {
                "type": "create_domain",
                "name": "positive_int",
                "schema": "app",
                "domain_type": "integer",
                "not_null": True,
                "check": "VALUE > 0",
            },
        ]
        rollback_ops = [
            {
                "type": "drop_domain",
                "name": "positive_int",
                "schema": "app",
                "domain_type": "integer",
                "not_null": True,
                "check": "VALUE > 0",
            },
        ]
        sql, rb_sql, changes = snapshot_diff_to_sql(ops, rollback_ops, db_name=None)
        assert "CREATE DOMAIN app.positive_int AS integer NOT NULL CHECK (VALUE > 0);" in sql
        assert "DROP DOMAIN IF EXISTS app.positive_int;" in rb_sql
        assert any(c.operation == "create_domain" for c in changes)

    def test_drop_domain_op(self):
        ops = [
            {
                "type": "drop_domain",
                "name": "positive_int",
                "schema": "app",
                "domain_type": "integer",
            },
        ]
        rollback_ops = [
            {
                "type": "create_domain",
                "name": "positive_int",
                "schema": "app",
                "domain_type": "integer",
            },
        ]
        sql, rb_sql, changes = snapshot_diff_to_sql(ops, rollback_ops, db_name=None)
        assert "DROP DOMAIN IF EXISTS app.positive_int;" in sql
        assert "CREATE DOMAIN app.positive_int AS integer;" in rb_sql
        assert any(c.operation == "drop_domain" for c in changes)

    def test_create_domain_op_with_default(self):
        ops = [
            {
                "type": "create_domain",
                "name": "my_email",
                "schema": None,
                "domain_type": "citext",
                "default": "'nobody@example.com'",
                "check": "VALUE ~* '^.+@.+$'",
            },
        ]
        rollback_ops = [
            {
                "type": "drop_domain",
                "name": "my_email",
                "domain_type": "citext",
            },
        ]
        sql, rb_sql, changes = snapshot_diff_to_sql(ops, rollback_ops, db_name=None)
        assert "CREATE DOMAIN my_email AS citext DEFAULT 'nobody@example.com'" in sql
        assert "CHECK (VALUE ~* '^.+@.+$')" in sql

    def test_create_sequence_op(self):
        ops = [
            {
                "type": "create_sequence",
                "name": "order_number_seq",
                "schema": "app",
                "start": 1000,
                "increment": 1,
                "minvalue": 1,
                "maxvalue": 999999,
                "cycle": True,
                "owned_by": "app.orders.id",
            },
        ]
        rollback_ops = [
            {
                "type": "drop_sequence",
                "name": "order_number_seq",
                "schema": "app",
            },
        ]
        sql, rb_sql, changes = snapshot_diff_to_sql(ops, rollback_ops, db_name=None)
        assert "CREATE SEQUENCE IF NOT EXISTS app.order_number_seq" in sql
        assert "INCREMENT BY 1" in sql
        assert "START WITH 1000" in sql
        assert "MINVALUE 1" in sql
        assert "MAXVALUE 999999" in sql
        assert "CYCLE" in sql
        assert "OWNED BY app.orders.id" in sql
        assert "DROP SEQUENCE IF EXISTS app.order_number_seq;" in rb_sql
        assert any(c.operation == "create_sequence" for c in changes)

    def test_drop_sequence_op(self):
        ops = [
            {
                "type": "drop_sequence",
                "name": "order_number_seq",
                "schema": None,
                "start": 1,
                "increment": 1,
            },
        ]
        rollback_ops = [
            {
                "type": "create_sequence",
                "name": "order_number_seq",
                "start": 1,
                "increment": 1,
            },
        ]
        sql, rb_sql, changes = snapshot_diff_to_sql(ops, rollback_ops, db_name=None)
        assert "DROP SEQUENCE IF EXISTS order_number_seq;" in sql
        assert "CREATE SEQUENCE IF NOT EXISTS order_number_seq" in rb_sql
        assert "INCREMENT BY 1" in rb_sql
        assert any(c.operation == "drop_sequence" for c in changes)

    def test_create_sequence_op_minimal(self):
        ops = [
            {
                "type": "create_sequence",
                "name": "simple_seq",
            },
        ]
        rollback_ops = [
            {
                "type": "drop_sequence",
                "name": "simple_seq",
            },
        ]
        sql, rb_sql, changes = snapshot_diff_to_sql(ops, rollback_ops, db_name=None)
        assert "CREATE SEQUENCE IF NOT EXISTS simple_seq" in sql
        assert "NO CYCLE" in sql
        assert "DROP SEQUENCE IF EXISTS simple_seq;" in rb_sql

