## 2. The specialists' state words differ

- **Symptom:** the Story & Editorial Analyst, the Visual Development
  Analyst and the Character Design Planner use `established`;
  Performance, Props and Sound use `script-stated`; the Cinematography Planner has neither. The bible's
  value states (`mocap-contracts` `bible.harpia`, `ValueState`) are
  `script-stated`, `creator-approved`, `proposal`, `tbd`.
- **Where:** `.claude/agents/story-editorial-analyst.md:94`,
  `.claude/agents/visual-development-analyst.md:81`,
  `.claude/agents/character-design-planner.md:88`,
  `.claude/agents/cinematography-planner.md:90`.
- **Reproduce:** found by reading the code.
- **Impact:** registers from different agents can't be compared or parsed
  the same way (the dashboard, the bible proposals of `preprod-link`).
- **Likely fix:** one set of words, the bible's, in every specialist;
  `preprod-link` agents/3 touches the same lines.
- **Status:** Open
