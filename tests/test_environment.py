import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_mocap_contracts_imports():
    import mocap_contracts

    assert os.environ["MOCAP_CONTRACTS_TAG"].startswith("v")
    assert Path(mocap_contracts.__file__).is_relative_to("/opt/mocap-contracts")


def test_copilot_adapters_are_current():
    # the Claude agents are canonical; a stale or orphaned adapter fails here
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync_agents.py"), "--check"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
