## 1. The Visual Development Analyst has no question cap

- **Symptom:** unlike the other six specialists, its file has no "Bounded
  creator decisions" section: no limit of three questions, no "one
  recommendation and at most one alternative".
- **Where:** `.claude/agents/visual-development-analyst.md:87-115` (Work and
  specification, nothing between); compare
  `.claude/agents/props-continuity-planner.md:96-111`.
- **Reproduce:** found by reading the code.
- **Impact:** the pilot film's first lesson (unbounded questions and option
  menus stall the creator) is not enforced for visual tasks; `README.md`
  says every specialist is bounded.
- **Likely fix:** add the section as the other specialists have it.
- **Status:** Open
