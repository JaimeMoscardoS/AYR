# Coordinating agents

Choose responsibilities from project needs, then map them to available agents. Do not require a fixed catalog, provider, model, or team size.

| Responsibility | When useful | Deliverable |
| --- | --- | --- |
| Lead / integrator | Always; can be the main assistant | Scope, dependencies, acceptance, reviewed integration |
| Explorer / domain analyst | Unfamiliar code or domain constraints | File-backed findings and open questions |
| Implementer | Bounded change ready | Owned diff, checks and limits |
| Reviewer / tester | Independent assurance adds value | Reproduction, defects and evidence |
| Security specialist | Auth, secrets, hostile input, external execution | Threat paths and verified mitigations |
| UI/accessibility specialist | Interfaces and interaction | Existing-system fit and observed checks |
| Data/domain specialist | Specialized data or engineering | Domain invariants and deterministic validation |

A small CLI may need only a lead implementing and verifying. A web app can have API and UI implementers after contracts are agreed. A domain-sensitive system may need analysis before implementation. The existence of a role is not a reason to launch it.

## Task contract

Give each worker: objective; minimal context and source paths; owned files; prerequisites and input artifacts; allowed side effects; acceptance; meaningful checks; expected return (changed paths, evidence, unresolved issues). Tell workers others may be editing and to preserve those changes. Use worktrees/separate workspaces when needed; do not grant overlapping write ownership.

Typical order: inspect constraints -> agree boundaries/acceptance -> implement independent tasks -> check components -> integrate -> check cross-component behavior -> review -> close. Dependencies express actual prerequisites, not a mandatory waterfall. New findings can update the plan with evidence.

When requirements or shared contracts change, identify affected tasks and acceptance criteria, update the brief and dependencies, and notify or pause only the affected workers before they continue against obsolete inputs. Preserve independent progress. Recheck impacted handoffs and integration evidence; previous checks do not validate changed behavior. Ask the user only when the change exceeds authorized scope or needs a decision they have not delegated.

The lead inspects diffs and verifies material claims. Reviewers should not merely restate implementer conclusions. An unavailable agent becomes a sequential responsibility, not a fabricated run. Failed tests are evidence to investigate, not permission to route around a gate. Finish with completed acceptance or named outstanding work.
