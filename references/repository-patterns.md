# Structure by need

| Condition | Useful structure | Why |
| --- | --- | --- |
| Small library, CLI, single service | Native package layout, tests, README, agent instructions | Low navigation cost and clear verification |
| Independent deployable applications | apps/ and shared packages/ when supported | Explicit ownership and intentional sharing |
| Structured component exchange | Schemas/types, valid/invalid examples, producer/consumer tests | Catch incompatible boundary assumptions |
| External or expensive dependency | Adapter, fake tests, representative integration/replay | Reproduce checks while distinguishing simulation from reality |
| Significant architecture choice | ADR: context, alternatives, decision, consequences | Preserve the reason for constraints |
| Long/multi-agent effort | Existing plan/handoff docs, acceptance and current evidence | Resume without trusting stale completion claims |
| Automated delivery | CI tied to revision being shipped | A green run on another commit is not release evidence |
| Configuration/credentials | Examples, ignore rules, documented variable names | Reproduce setup without secrets |

Only create directories with a present use. Keep domain-specific invariants with their component. Choose commands from manifests and observed behavior. Architecture docs explain dependencies and decisions; a directory listing alone does not explain a system.

For larger systems, consult [the public reference analysis](../docs/public-reference-analysis.md). Transfer the useful discipline: separate check classes, invalid-input regression cases, reviewed snapshot changes, discoverable contribution steps and CI coverage aligned with supported platforms. Document what each check covers; do not copy large test matrices or workspaces into smaller products.
