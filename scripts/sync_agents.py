"""Regenerate the Copilot adapters in .github/agents/ from .claude/agents/.

The Claude files are canonical. Run after editing any of them:

    python3 scripts/sync_agents.py          # write adapters
    python3 scripts/sync_agents.py --check  # exit 1 if an adapter is stale
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_DIR = ROOT / ".claude" / "agents"
COPILOT_DIR = ROOT / ".github" / "agents"

# Claude Code tool -> Copilot tool set.
TOOL_MAP = {"Read": "read", "Grep": "search", "Glob": "search", "Edit": "edit", "Write": "edit", "Bash": "execute"}
COPILOT_ORDER = ["read", "search", "edit", "execute"]

DISPLAY_RE = re.compile(r"^\*\*Display name:\*\* (.+)$", re.M)
INVOKE_RE = re.compile(r"^\*\*Invoke with:\*\* (.+)$", re.M)


def parse(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        raise ValueError(f"{path}: missing frontmatter")
    meta = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, match.group(2)


def adapter(path: Path) -> str:
    meta, body = parse(path)
    display = DISPLAY_RE.search(body)
    invoke = INVOKE_RE.search(body)
    if not display or not invoke:
        raise ValueError(f"{path}: needs **Display name:** and **Invoke with:** lines")
    tools = {TOOL_MAP[t.strip()] for t in meta["tools"].split(",")}
    body = DISPLAY_RE.sub("", INVOKE_RE.sub("", body)).lstrip("\n")
    description = meta["description"].strip('"')
    return (
        "---\n"
        f'name: "{display.group(1)}"\n'
        f'description: "{description}"\n'
        f'argument-hint: "{invoke.group(1)}"\n'
        f"tools: [{', '.join(t for t in COPILOT_ORDER if t in tools)}]\n"
        "---\n"
        f"<!-- Generated from .claude/agents/{path.name} by scripts/sync_agents.py. Edit that file, not this one. -->\n\n"
        f"{body}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="report stale adapters without writing")
    args = parser.parse_args()

    stale = []
    expected = set()
    for source in sorted(CLAUDE_DIR.glob("*.md")):
        target = COPILOT_DIR / f"{source.stem}.agent.md"
        expected.add(target.name)
        content = adapter(source)
        if not target.exists() or target.read_text(encoding="utf-8") != content:
            stale.append(target.name)
            if not args.check:
                target.write_text(content, encoding="utf-8")
    orphans = sorted(p.name for p in COPILOT_DIR.glob("*.agent.md") if p.name not in expected)

    for name in stale:
        print(f"{'stale' if args.check else 'wrote'}: .github/agents/{name}")
    for name in orphans:
        print(f"orphan (no .claude source): .github/agents/{name}")
    return 1 if args.check and (stale or orphans) else 0


if __name__ == "__main__":
    sys.exit(main())
