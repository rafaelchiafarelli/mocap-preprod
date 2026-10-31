## 3. The fixture's generator lives in mocap-writer

- **Depends on:** 2; mocap-writer `tools/make_fixture_film.py` (on its
  `dev`, 2026-10-31)
- **Why:** Rafael, 2026-10-31: the script that uses the writer's code
  belongs to the writer, and this repository must rebuild its fixture
  even when downloaded on its own, with no writer checkout beside it.
- **Contract:** `tools/make_fixture_film.sh [ref]` makes a shallow clone
  of mocap-writer over HTTPS at `ref` (default `dev`, submodules
  included), builds the writer's image from it, runs the writer's
  `tools/make_fixture_film.py` there and replaces `tests/fixtures/film/`
  but its `analysis/`, printing the writer commit it used. The copy of the
  generator in this repository goes.
- **Tests:** the rebuilt fixture passes `tests/test_fixture_film.py`
