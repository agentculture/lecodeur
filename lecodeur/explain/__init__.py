"""Explain catalog — markdown keyed by topic-path tuples.

See :mod:`lecodeur.explain.catalog` for the string bodies and :func:`resolve`
for lookup.
"""

from __future__ import annotations

from lecodeur.cli._errors import EXIT_USER_ERROR, LecodeurError
from lecodeur.explain.catalog import ENTRIES


def resolve(path: tuple[str, ...]) -> str:
    """Return the markdown body for ``path`` or raise :class:`LecodeurError`."""
    if path in ENTRIES:
        return ENTRIES[path]
    display = " ".join(path) if path else "<root>"
    raise LecodeurError(
        code=EXIT_USER_ERROR,
        message=f"no explain entry for: {display}",
        remediation="list known topics with: lecodeur explain lecodeur",
    )


def known_paths() -> list[tuple[str, ...]]:
    """Return every catalog path (used by tests)."""
    return list(ENTRIES.keys())
