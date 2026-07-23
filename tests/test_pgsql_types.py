def test_import():
    from dbwarden_pgsql_types import setup
    assert callable(setup)
