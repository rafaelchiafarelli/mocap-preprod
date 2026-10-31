import os


def pytest_report_header(config):
    # mocap-contracts is not pinned: say which release this run tested against
    return f"mocap-contracts: {os.environ.get('MOCAP_CONTRACTS_TAG', 'not installed')}"
