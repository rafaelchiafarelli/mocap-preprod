"""Talk to workflow_tool as a client does: a real server process, over stdio."""

import asyncio
import os
import sys
from pathlib import Path

import mocap_contracts as mc
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "film"
AGENT = "props-continuity-planner"


def start(root) -> list[str]:
    return [sys.executable, "-m", "workflow_tool", str(root)]


def session(root, use):
    async def run():
        params = StdioServerParameters(command=sys.executable, args=start(root)[1:],
                                       env=dict(os.environ), cwd=str(ROOT))
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as s:
                await s.initialize()
                return await use(s)
    return asyncio.run(asyncio.wait_for(run(), 60))


def call(root, tool, **args):
    return session(root, lambda s: s.call_tool(tool, args))


def text(result) -> str:
    return "".join(c.text for c in result.content)


def answer(result):
    """A tool's result; a refusal fails the test with its reason."""
    assert not result.is_error, text(result)
    return result.structured_content.get("result", result.structured_content)


def register(root, agent: str, code: str) -> None:
    """Add an agent's space to the film, as mocap-writer workflow-link does."""
    path = root / "film.json"
    film = mc.from_json(mc.Film, path.read_text())
    film.spaces.add(code=code, owner=agent)
    path.write_text(mc.to_json(film))
