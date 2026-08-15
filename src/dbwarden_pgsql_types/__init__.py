from __future__ import annotations

from dbwarden_pgsql_types.handlers import (
    CompositeTypeHandler,
    DomainHandler,
    EnumHandler,
    SequenceHandler,
)

__version__ = "0.2.0"

# The dbwarden plugin contract this package targets. Core refuses to load a
# plugin declaring a version it does not provide, so a mismatched pairing fails
# at load with one clear message instead of somewhere inside a migration.
DBWARDEN_PLUGIN_API = 1

# Enums come first because domains and composite types can be defined over them.
HANDLER_CLASSES = (
    EnumHandler,
    DomainHandler,
    CompositeTypeHandler,
    SequenceHandler,
)


CONFIG_KEYS = (
    "pg_domains",
    "pg_sequences",
    "pg_composite_types",
)


def setup(registrar) -> None:
    for handler_class in HANDLER_CLASSES:
        registrar.register_object_handler(handler_class())
    # Declares the database_config(...) keys this plugin consumes so core can
    # reject them with an install hint when the plugin is absent. Guarded so the
    # plugin still loads against cores predating the config-key registry.
    register_config_key = getattr(registrar, "register_config_key", None)
    if register_config_key is not None:
        register_config_key(*CONFIG_KEYS)


__all__ = [
    "CONFIG_KEYS",
    "CompositeTypeHandler",
    "DomainHandler",
    "EnumHandler",
    "HANDLER_CLASSES",
    "SequenceHandler",
    "setup",
]
