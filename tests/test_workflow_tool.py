"""preprod-link workflow-tool/1: the MCP server starts, answers and refuses."""

import asyncio
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import mocap_contracts as mc
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "film"
AGENT = "props-continuity-planner"

sys.path.insert(0, str(ROOT / "scripts"))
import sync_agents  # noqa: E402


def _copy(tmp_path) -> Path:
    root = tmp_path / "film"
    shutil.copytree(FIXTURE, root)
    return root


@pytest.fixture
def plain_film(tmp_path):
    """The fixture as the writer makes it: no workflow part yet."""
    return _copy(tmp_path)


@pytest.fixture
def film_root(plain_film):
    """The fixture with what mocap-writer workflow-link registers: the part and an agent's space."""
    path = plain_film / "film.json"
    film = mc.from_json(mc.Film, path.read_text())
    film.parts.add(name="workflow", path="workflow.sqlite", owner="shared")
    film.spaces.add(code="props", owner=AGENT)
    path.write_text(mc.to_json(film))
    return plain_film


def _start(root) -> list[str]:
    return [sys.executable, "-m", "workflow_tool", str(root)]


def _session(root, use):
    async def run():
        params = StdioServerParameters(command=sys.executable, args=_start(root)[1:],
                                       env=dict(os.environ), cwd=str(ROOT))
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return await use(session)
    return asyncio.run(asyncio.wait_for(run(), 60))


def _call(root, tool, **args):
    return _session(root, lambda s: s.call_tool(tool, args))


def _text(result) -> str:
    return "".join(c.text for c in result.content)


def test_starts_on_the_fixture_and_answers_film_spaces(film_root):
    result = _call(film_root, "film_spaces", agent=AGENT)
    assert not result.is_error, _text(result)
    assert result.structured_content["result"] == [{"agent": AGENT, "space": "props"}]


def test_read_tools_only(film_root):
    async def tools(session):
        return (await session.list_tools()).tools
    assert [t.name for t in _session(film_root, tools)] == ["film_spaces"]


def test_start_makes_the_database_with_its_tables(film_root):
    _call(film_root, "film_spaces", agent=AGENT)
    conn = sqlite3.connect(film_root / "workflow.sqlite")
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    conn.close()
    assert {"proposal_table", "review_table", "request_table"} <= tables


def test_the_database_is_where_the_part_says(film_root):
    path = film_root / "film.json"
    film = mc.from_json(mc.Film, path.read_text())
    next(p for p in film.parts if p.name == "workflow").path = "analysis/flow.sqlite"
    path.write_text(mc.to_json(film))
    _call(film_root, "film_spaces", agent=AGENT)
    assert (film_root / "analysis" / "flow.sqlite").exists()
    assert not (film_root / "workflow.sqlite").exists()


@pytest.mark.parametrize("name", ["sound-design-planner", "writer", "creator", ""])
def test_refuses_who_owns_no_agent_space(film_root, name):
    result = _call(film_root, "film_spaces", agent=name)
    assert result.is_error
    assert "has no space in film.json" in _text(result)


def test_a_space_registered_while_running_is_seen(film_root):
    async def use(session):
        path = film_root / "film.json"
        film = mc.from_json(mc.Film, path.read_text())
        film.spaces.add(code="sound", owner="sound-design-planner")
        path.write_text(mc.to_json(film))
        return await session.call_tool("film_spaces", {"agent": "sound-design-planner"})
    assert not _session(film_root, use).is_error


def test_a_film_json_broken_while_running_is_named(film_root):
    async def use(session):
        (film_root / "film.json").write_text("{}")
        return await session.call_tool("film_spaces", {"agent": AGENT})
    result = _session(film_root, use)
    assert result.is_error and "film.json" in _text(result)


def test_refuses_a_film_without_the_part(plain_film):
    done = subprocess.run(_start(plain_film), cwd=ROOT, capture_output=True, text=True, timeout=60)
    assert done.returncode == 1
    assert "has no 'workflow' part" in done.stderr
    assert done.stdout == ""
    assert not (plain_film / "workflow.sqlite").exists()


def test_refuses_a_folder_that_is_no_film(tmp_path):
    done = subprocess.run(_start(tmp_path), cwd=ROOT, capture_output=True, text=True, timeout=60)
    assert done.returncode == 1
    assert "film.json" in done.stderr


def test_refuses_a_broken_film_json(film_root):
    (film_root / "film.json").write_text("{}")
    done = subprocess.run(_start(film_root), cwd=ROOT, capture_output=True, text=True, timeout=60)
    assert done.returncode == 1
    assert "Film" in done.stderr


def test_refuses_a_workflow_file_that_is_no_database(film_root):
    (film_root / "workflow.sqlite").write_text("not a database, and long enough to be read as one")
    done = subprocess.run(_start(film_root), cwd=ROOT, capture_output=True, text=True, timeout=60)
    assert done.returncode == 1
    assert "workflow_tool:" in done.stderr


def test_clients_start_the_server_through_the_image():
    claude = json.loads((ROOT / ".mcp.json").read_text())["mcpServers"]["workflow"]
    code = json.loads((ROOT / ".vscode" / "mcp.json").read_text())["servers"]["workflow"]
    assert claude["command"] == "docker/mcp.sh"
    assert code["command"] == "${workspaceFolder}/docker/mcp.sh"
    assert os.access(ROOT / "docker" / "mcp.sh", os.X_OK)


def test_mcp_tools_map_to_their_server_for_copilot():
    assert sync_agents.copilot_tool("mcp__workflow__propose") == "workflow/*"
    assert sync_agents.copilot_tool("Read") == "read"


def test_an_adapter_lists_the_mcp_server_after_the_tool_sets(tmp_path):
    source = tmp_path / "x.md"
    source.write_text("---\nname: x\ndescription: \"d\"\ntools: Read, mcp__workflow__film_spaces, "
                      "mcp__workflow__propose\n---\n\n**Display name:** X\n**Invoke with:** y\n\nBody\n")
    assert "tools: [read, workflow/*]\n" in sync_agents.adapter(source)
