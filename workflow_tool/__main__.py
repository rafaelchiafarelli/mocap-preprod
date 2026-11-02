"""python -m workflow_tool <film-root>: run the server on stdio, or refuse to start."""

import argparse
import sqlite3
import sys
from pathlib import Path

from workflow_tool.server import FilmError, make_server, open_database


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("film_root", type=Path)
    root = parser.parse_args().film_root.resolve()
    try:
        open_database(root).close()  # tables made, older ones migrated, before any call
    except (FilmError, sqlite3.Error) as e:
        print(f"workflow_tool: {e}", file=sys.stderr)
        return 1
    make_server(root).run("stdio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
