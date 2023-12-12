"""Various generic constants and functions used by the CLI."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

try:
    from rich import get_console
    from rich import print as rich_print
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "Please install the DLite entities service utility CLI with 'pip install "
        f"{Path(__file__).resolve().parent.parent.parent.parent.resolve()}[cli]'"
    ) from exc

from rich.console import Console

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, TextIO


EXC_MSG_INSTALL_PACKAGE = (
    "Please install the DLite entities service utility CLI with "
    f"'pip install {Path(__file__).resolve().parent.parent.parent.parent.resolve()}"
    "[cli]' or 'pip install dlite-entities-service[cli]'"
)

OUTPUT_CONSOLE = get_console()
ERROR_CONSOLE = Console(stderr=True)


def print(
    *objects: Any,
    sep: str | None = None,
    end: str | None = None,
    file: TextIO | None = None,
    flush: bool | None = None,
) -> None:
    """Print to the output console."""
    file = file or OUTPUT_CONSOLE.file
    kwargs = {"sep": sep, "end": end, "file": file, "flush": flush}
    for key, value in list(kwargs.items()):
        if value is None:
            del kwargs[key]

    rich_print(*objects, **kwargs)
