"""Config-driven model_spec coverage moved here from core's PostgreSQL doc gate."""

from __future__ import annotations

from types import SimpleNamespace

from dbwarden_pgsql_types import SequenceHandler


def test_sequences_config() -> None:
    config = SimpleNamespace()
    config.pg_sequences = [
        {
            "name": "order_number_seq",
            "start": 1000,
            "increment": 1,
            "minvalue": 1,
            "maxvalue": 999999,
            "cycle": False,
        },
    ]
    result = SequenceHandler().model_spec_from_config(config)
    assert "order_number_seq" in result
    assert result["order_number_seq"]["start"] == 1000
