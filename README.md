# Mocap Pre-Production Workhorse

This folder is the reusable pre-production workhorse for an animation-focused
production house. Keep shared worker guidance and production-house
documentation here; keep each film's script, creative decisions, and
project-specific work in that film's own project root.

## First agent

`.github/agents/script-readiness-analyst.agent.md` analyzes a script and
related creative materials, then turns gaps, ambiguities, and dependencies
into a prioritized set of work to complete or explicitly defer before
production. It distinguishes explicit information, ambiguity, and material
not found; it does not rewrite the script or make creative decisions.

This workflow is project-agnostic: provide the film project's root and script
when invoking the agent. It writes that project's deliverable to
`<project-root>/analysis/pre-production-readiness.md`. Do not add film-specific
paths, assumptions, or findings to this reusable workhorse documentation.

## Agent configuration by platform

The current `.github/agents/` file is for VS Code Copilot; Claude Code does
not load it as a native Claude agent. If both platforms should run this
workhorse, keep a native agent adapter under `.claude/agents/` as well.
Platform adapters may need different frontmatter and tool names, but should
follow the same reusable workflow and documentation so the process does not
drift. Moving the Copilot agent into `.claude/` would make it unavailable as
a VS Code Copilot custom agent.

## Shared production-house documentation

Reusable documentation for the production workflow should be built separately
from any one film's analysis. Since animation is the main product, this
documentation can establish shared terms and handoffs across story, assets,
scenes, animation, and sound. Keep early guidance explicit about what is
established versus still to be learned from the pilot production.

The eventual location of this workhorse within or alongside Mocap Studio is
not fixed; its contents should remain usable either way.
# mocap-preprod
