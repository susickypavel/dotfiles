# AGENTS.md

These are general guidelines to apply across every sessions.

## Dependency supply-chain safety

- Never install, select, or update to a package version that is newer than the repository's minimum release age policy allows. Never bypass, disable, weaken, or work around that policy, including for an explicitly requested "latest" version.
- Before adding or updating any dependency, determine the applicable repository policy and verify that the selected version satisfies it. This requirement applies to direct and transitive dependencies and to every package manager.
- If the policy, a package version's release age, or a compliant resolution cannot be determined, do not install or change the dependency. Stop and ask the user for direction instead. Treat violating the policy as a serious supply-chain security risk.

## Response style

Write all responses in ASD-STE100 Simplified Technical English. Use short, direct sentences and consistent terminology. Keep technical identifiers, code, commands, and quoted text unchanged when required for accuracy.

End every final answer delivered to the user with a self-contained `TL;DR` section. Apply this rule only to the final user-facing answer—not to internal reasoning, working notes, intermediate progress updates, tool calls, or generated files. The `TL;DR` must contain all important information that the user needs, including the outcome, actions taken, key details, caveats, and required next steps. Write it so the user can skip the main response and still understand the complete result. Keep it proportional to the task, but do not make it so short that it loses useful information. Prefer a multi-line format for readability. Use bullet points when they make the information easier to scan.

Don't write TL;DR when using /grill-me, /grilling, /wayfinder or /grill-with-docs skill is used, it clutters the questions with redundant TLDRs.
