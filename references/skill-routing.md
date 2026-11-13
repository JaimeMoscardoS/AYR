# Integrating existing skills

## Purpose and selection

AYR handles project understanding, repository preparation and capability selection. It integrates existing specialist skills and can hand off execution to an established workflow such as GSD. No framework, skill collection or named provider below is a required dependency, and no third-party instructions are bundled.

Select by current need, not by a fixed checklist. Read the selected skill and its relevant resources before invoking it; do not load the whole catalog. Match installed names and versions rather than assume a slash command, tool API or agent exists. Record each selection in the existing project documentation: phase, trigger, resolved capability, availability, workflow owner, input, expected output and evidence. External acquisition still follows [discovery and trust](discovery.md).

| Need or phase | Candidate existing skills | Activation condition and output |
| --- | --- | --- |
| Clarify an idea | AYR interview; `brainstorming` if available | Use AYR's brief first; add deeper design exploration only for unresolved consequential decisions. Carry accepted answers forward and preserve the selected skill's own gates. |
| Discover missing capabilities | `find-skills` or a user-selected equivalent | Only for an unmet need. Produce reviewed candidates; search results are not activated dependencies. |
| Research a technical/domain decision | Available research skill or domain specialist | Resolve a concrete uncertainty with sources and explicit limits; avoid repeating completed research. |
| Start a substantial staged project | `gsd-new-project` | No existing GSD project state; initialization is within scope. Produce GSD's own requirements, roadmap and state through its workflow. |
| Resume or locate next work | `gsd-resume-work`, `gsd-progress` | Existing GSD state or interrupted work. Inspect and route from that state instead of recreating it. |
| Clarify or plan a GSD phase | `gsd-discuss-phase`, `gsd-plan-phase` | A phase exists and its inputs are ready. Respect discussion/design gates and return executable plans through GSD. |
| Execute a planned phase | `gsd-execute-phase` | Plans and prerequisites are ready and implementation is authorized. GSD owns dependency waves and state updates. |
| Handle a bounded GSD task | `gsd-quick` | A small task warrants GSD tracking. Read its prerequisites first; quick mode is not a guarantee of zero agents or zero setup. |
| Design a user interface | `frontend-design`; available accessibility skill/role | UI work is present. Use the project's design system and verify real interaction where tools permit. |
| Diagnose a failure | `systematic-debugging` or an available debugging skill | A reproducible error or uncertainty about cause exists. Gather evidence before selecting a fix. |
| Review and verify | Available code-review and verification skills; `gsd-verify-work` for GSD UAT | Choose the check needed for the actual risk. User acceptance and automated checks are different evidence. |

The names above are routing examples observed in installed skill definitions, not universal command syntax or an endorsement of every package version. A specialist skill runs inside the owning workflow; it does not create a second project director. Do not chain every row for every project.

## One workflow owner and one source of state

1. Inspect project instructions and recognized planning artifacts before deciding a route. The existence of a directory named `.planning` alone does not prove that it belongs to GSD. Look for GSD's project, requirements, roadmap, state and configuration files and their content.
2. When GSD already owns work, use its progress/resume entry point and preserve active plans, checkpoints and incomplete work. Missing files are a recovery question, not permission to reinitialize or delete the directory. Do not create a parallel AYR state system.
3. For new substantial work, choose GSD only when its benefits fit and its installation is usable. An existing project need not migrate to GSD. A small script can use AYR plus one implementer and the relevant checks without a roadmap.
4. At handoff, give the chosen owner the user's brief, scope and acceptance, decisions already settled, existing artifact paths, selected capabilities and checks, unresolved questions and next bounded task. Reuse known answers while preserving the invoked workflow's required gates.
5. The invoked workflow becomes responsible for its own planning/execution/state updates. AYR does not simultaneously launch another planner or write competing status. Do not bounce back to AYR's interview after each substep. Return only for a new bootstrap/capability decision or the agreed final report.

Do not silently add automatic, skip-research, skip-verification or other flags. Read the installed workflow's supported options and honor explicit user choices. A recommendation to use a workflow does not authorize its unrelated remote publication, paid services or broad configuration changes.

## Verify availability before handoff

Classify candidates as **ready**, **recommendation only**, or **blocked**, with reasons. For a skill to be ready, check its entry point, required referenced resources/scripts, installed runtime support and needed tools. A stale installation path is a real integration issue even when SKILL.md is listed. Do not fabricate a successful invocation or silently install/repair user-wide dependencies.

If references point to a missing installation root, locate the matching installed package only through actual evidence and verify its version and resources. Record any explicit per-session resource mapping; never substitute another package or bypass its gates. If equivalence cannot be established, keep the integration blocked and name the repair needed.

With no GSD state and an unavailable optional skill, continue the independent authorized work with available capabilities and record the fallback. With existing GSD state and an unavailable required runtime/resource, preserve that state, report the blocker and continue only independent work. Do not pretend a handoff succeeded or reproduce a competing roadmap to get around the failure.

## Examples

- **Small CLI, complete brief:** use the available implementer and relevant checks; no external search or GSD initialization solely to populate a catalog.
- **New multi-phase application:** finish the brief, check GSD readiness, hand off initialization and follow its plan/execute/verify routing. Add UI or domain skills only to the tasks needing them.
- **Existing GSD repository:** start with progress/resume, consume its current requirements and checkpoints, and avoid duplicate requirements or roadmaps.
- **Broken GSD resource path:** keep the capability blocked until the matching resources are resolved; do not claim that installation or execution works merely because its skill is discoverable.
