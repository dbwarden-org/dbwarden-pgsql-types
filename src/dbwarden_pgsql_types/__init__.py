from __future__ import annotations

from dbwarden_pgsql_types.handlers import (
    CompositeTypeHandler,
    DomainHandler,
    EnumHandler,
    SequenceHandler,
)

__version__ = "0.1.0"

# The DBWarden plugin contract this package targets. Core refuses to load a
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


def setup(registrar) -> None:
    for handler_class in HANDLER_CLASSES:
        registrar.register_object_handler(handler_class())


__all__ = [
    "CompositeTypeHandler",
    "DomainHandler",
    "EnumHandler",
    "HANDLER_CLASSES",
    "SequenceHandler",
    "setup",
]
