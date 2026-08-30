# Source-Aware Intelligence Hub — Claude Contract

## Mission

Build and maintain a public, credential-free portfolio demonstration of source-aware decision support. The product ranks one recommended outcome, preserves two alternatives, surfaces exceptions first, and makes every source's authority, freshness, confidence or availability, and truth state explicit.

This repository is an independent synthetic demonstration and must never contain or imply data, topology, history, integrations, or deployed state from any private system.

## Reading order

1. `CLAUDE.md`
2. `AGENTS.md`
3. `README.md`
4. `docs/architecture.md`
5. `docs/api.md`
6. `docs/threat-model.md`
7. `CONTRIBUTING.md`
8. `.github/workflows/ci.yml`
9. Relevant tests before implementation

When documents disagree, current tests and implementation define behavior; fix stale documentation in the same accepted change.

## Canonical architecture

- `backend/app/main.py`: FastAPI routes, static serving, and response security headers.
- `backend/app/models.py`: strict public wire models.
- `backend/app/service.py`: deterministic normalization and ranking.
- `backend/app/fixtures.py`: fictional in-memory scenarios only.
- `backend/tests/`: API, service, failure, and security assertions.
- `frontend/src/`: React and TypeScript interface.
- `frontend/src/App.test.tsx`: component, interaction, and accessibility coverage.
- `frontend/dist/`: generated production output; never hand-edit or commit unless repository policy explicitly changes.
- `tools/scan_public.py`: current-tree and reachable-history public-boundary scanner.
- `tools/tests/`: scanner negative canaries.

Production is same-origin: Vite builds the frontend and FastAPI serves both `/api/workspace` and compiled assets. There is no database, account system, writable action, external provider, proxy, or arbitrary URL surface.

## Product laws

1. All records, identities, organizations, dates, and failures are fictional and deterministic.
2. Show exactly one recommendation and two alternatives, each with concise source-grounded reasons.
3. Exceptions precede routine records.
4. Truth states are explicit: `live`, `scheduled`, `stale`, `unavailable`, and `conflicting`.
5. Unknown or unavailable is never rendered as healthy, current, or complete.
6. Every source card names authority, freshness, confidence or availability, and safe detail-link state.
7. Apparent actions are read-only demonstrations or local scenario controls and must be labelled accordingly.
8. No credential, environment file, external network connection, analytics, mutation, or live integration is required or permitted for the demo.
9. Deep links are local allowlisted synthetic paths only.
10. Do not claim production deployment, private-system parity, complete screen-reader acceptance, predictive intelligence, or live integrations.

## Public/private boundary

Allowed:

- Generic domain and API contracts.
- Deterministic fictional fixtures.
- Source-aware ranking and explanation logic.
- Accessible frontend components and truthful degraded states.
- Tests, CI, threat model, and synthetic demo documentation.

Forbidden:

- Content or Git objects from any private repository.
- Personal, household, employment, client, account, vault, email, calendar, or operational data.
- Private hostnames, IP addresses, ports, service units, filesystem paths, profile names, provider configuration, account IDs, emails, tokens, credentials, logs, receipts, handoffs, screenshots, or browser captures.
- Private-system adapters, private source names, private extension identities, or statements that this is any deployed private system.

A finding in current files, generated output, staged bytes, package artifacts, or reachable history blocks publication. Do not suppress unexplained findings. Scanner tests must prove forbidden canaries are detected without printing sensitive values.

## API and truth contracts

- Public API is read-only and bounded.
- Scenario values are closed and validated; reject unknown or oversized input.
- Response models reject unexpected fields.
- Errors are concise and sanitized; no exception internals or filesystem details reach clients.
- Ranking is deterministic for identical fixtures.
- Source failures remain visible and influence recommendation reasons.
- CORS and browser access default to same-origin.
- Security headers remain applied to API and static responses.
- Never add a generic fetch, proxy, URL opener, command runner, file reader, provider token, webhook, or mutation endpoint.

Adding authentication, writable actions, live sources, persistence, or deployment changes the trust model and requires a separately approved design before code.

## Accessibility and responsive contract

- One clear page heading, semantic landmarks, skip link, logical heading order, native controls, keyboard completion, and visible focus.
- One restrained polite status channel for loading or scenario changes; no noisy streaming announcements.
- Truth, selection, conflict, failure, and recommendation never rely on color, motion, icon, or position alone.
- Reflow at 320 CSS pixels and 200% zoom without two-dimensional scrolling for the primary workflow.
- Preserve meaning in forced colors and respect reduced motion.
- Loading, empty, stale, unavailable, conflicting, and host-failure states provide named recovery.
- Automated DOM and axe evidence supports but does not replace NVDA, VoiceOver, or installed high-contrast acceptance.

## Security rules

- Validate all inputs at the FastAPI and domain boundaries.
- Keep links same-origin and allowlisted.
- Keep browser bundles free of secrets and private values.
- Use sanitized structured errors and no raw exception display.
- Preserve content-security, frame-denial, referrer, MIME-sniffing, and permissions headers.
- Bound fixture volume and response size.
- Lock dependencies and block unresolved high or critical advisories.
- Do not add arbitrary deserialization, subprocess, shell, filesystem, upload, template injection, or remote-request surfaces.

## Engineering loop

Use vertical RED → GREEN → REFACTOR slices.

1. Prove repository root, branch, status, remote, and writer ownership.
2. Read the relevant tests and contracts.
3. Add one failing behavior or negative test and verify the expected failure.
4. Implement the smallest production change.
5. Run focused tests, then the complete governing suite.
6. Review source, generated output, lockfiles, permissions, staged bytes, and status.
7. Freeze exact candidate bytes for an independent read-only review on meaningful release/security/accessibility changes.
8. Correct blockers and re-run all affected and governing gates.
9. Commit only a verified unit; never force-push or rewrite public history.

Exactly one writer owns the mutable repository/index at a time. Reviewers are read-only.

## Exact commands

Prerequisites: Python 3.12+, `uv`, Node.js 20+, and npm.

Setup and run:

```bash
uv sync --locked
npm ci --prefix frontend
npm run build --prefix frontend
uv run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Governing verification:

```bash
uv run ruff format --check backend tools
uv run ruff check backend tools
uv run mypy
uv run pytest
npm run format:check --prefix frontend
npm run lint --prefix frontend
npm run typecheck --prefix frontend
npm run test:run --prefix frontend
npm run build --prefix frontend
uv run python -m tools.scan_public
uv run python -m tools.scan_public --history
npm audit --prefix frontend --audit-level=high
uv run uv pip check
git diff --check
git status --short --untracked-files=all
```

After build, start the production path and exercise `/`, `/api/health`, and all declared workspace scenarios through real HTTP. Use a real browser for release acceptance when available.

## Release gates

A public release requires:

- Formatter, lint, typecheck, tests, production build, runtime/API smoke, and applicable browser checks pass on exact bytes.
- Current tree, generated output, staged candidate, package inventory, and reachable-history scans return zero unexplained findings.
- Dependency audit has no unresolved high or critical advisory.
- Exact-candidate independent review passes.
- Git status and committed export contain only intended public files.
- Local commit equals remote `main`; GitHub visibility/default branch/CI/public anonymous readback are verified.
- README claims match the actual implementation and evidence.

## Stop and rollback

Stop before publication for any secret/private/topology finding, misleading claim, failing gate, dependency or license issue, accessibility blocker, candidate drift, or unavailable independent review.

If a material issue appears after publication, make the repository private immediately, preserve evidence locally, and report. Never rewrite history or force-push. Do not deploy this app or modify any private repository or runtime under this contract.

## Definition of done

Done means the synthetic full-stack app builds and runs, every scenario is exercised, quality/security/privacy/accessibility gates pass, documentation and implementation agree, exact candidate review passes, the public repository is readable, local and remote commits match, hosted CI is green, and remaining limitations are stated honestly.
