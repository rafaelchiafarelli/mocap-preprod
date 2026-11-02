import os
import shutil

import mocap_contracts as mc
import pytest
from mcp_client import AGENT, FIXTURE, register


def pytest_report_header(config):
    # mocap-contracts is not pinned: say which release this run tested against
    return f"mocap-contracts: {os.environ.get('MOCAP_CONTRACTS_TAG', 'not installed')}"


@pytest.fixture
def plain_film(tmp_path):
    """The fixture film as the writer makes it: no workflow part yet."""
    root = tmp_path / "film"
    shutil.copytree(FIXTURE, root)
    return root


@pytest.fixture
def film_root(plain_film):
    """The fixture with what mocap-writer workflow-link registers: the part and an agent's space."""
    path = plain_film / "film.json"
    film = mc.from_json(mc.Film, path.read_text())
    film.parts.add(name="workflow", path="workflow.sqlite", owner="shared")
    path.write_text(mc.to_json(film))
    register(plain_film, AGENT, "props")
    return plain_film
