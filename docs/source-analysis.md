# Design rationale and public sources

## Method and limits

This package documents general repository-bootstrap practices and references publicly maintained projects. Descriptions are original summaries, not copies of third-party implementation. Source inspection is distinct from running a project's tests or verifying its CI. Popularity is discovery context, not a safety or quality guarantee.

Do not publish private-project names, contributor identities, internal paths, endpoints, source revisions, file fingerprints or excerpts in bootstrap documentation without explicit authorization. Keep private retrieval evidence inside the authorized project boundary. Public-facing rationale should use public sources or describe general patterns without identifying private origins.

## General design patterns

| Pattern | Benefit | When to apply |
| --- | --- | --- |
| Product purpose and scope before implementation | Makes acceptance and exclusions explicit | Every project, proportionate to size |
| Explicit component ownership and interfaces | Reduces conflicting edits and implicit assumptions | Real component or team boundaries |
| Valid and invalid contract examples | Makes compatibility and rejection behavior observable | Structured producer/consumer interfaces |
| Adapters and representative integration checks | Separates local feedback from external-service behavior | External or expensive dependencies |
| Architecture decisions with alternatives | Preserves reasons and consequences | Significant lasting tradeoffs |
| Evidence-based continuation | Distinguishes completed work from pending checks | Long-running or delegated work |
| Configuration examples without secrets | Reproduces setup without distributing credentials | Configurable applications |
| Checks tied to the delivered revision | Prevents unrelated green runs being used as release evidence | Automated delivery |

These patterns do not prescribe a monorepo, fixed agent team, mandatory RAG provider or heavyweight planning system.

## Public references

The [large public repository analysis](public-reference-analysis.md) provides immutable source links and transfer limits for VS Code, uv, Django and FastAPI.

- [Vercel Skills](https://github.com/vercel-labs/skills) documents capability discovery. Skill searches and runtime agent discovery are different activities.
- [GitHub Spec Kit](https://github.com/github/spec-kit) connects specifications, plans and tasks. Adopt traceability when useful without imposing the full toolkit.
- [Anthropic Skills](https://github.com/anthropics/skills) provides examples of discoverable instruction packages and supporting resources. Review the selected content's license and behavior independently.

The ecosystem links above are documentation references, not installed or certified dependencies. No external capability is installed by this package.
