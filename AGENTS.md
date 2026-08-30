# AGENTS.md

## Purpose

This repository is the public Source-Aware Intelligence Hub: a credential-free React and FastAPI portfolio demonstration using deterministic fictional fixtures. It is an independent synthetic product with no live integrations, external mutations, accounts, or private data.

## Authority and ownership

- `CLAUDE.md` is the complete product and engineering contract.
- `README.md` is the public product description.
- `docs/architecture.md`, `docs/api.md`, and `docs/threat-model.md` define the public architecture and trust boundary.
- Tests and implementation are behavioral authority; reconcile stale docs in the same change.
- The designated repository maintainer owns repository mutation.
- Exactly one writer may own this repository, worktree, branch, index, lockfiles, and generated output at a time.
- Reviewers are read-only and bound to exact candidate bytes.

Before changing anything, prove:

```bash
git rev-parse --show-toplevel
git branch --show-current
git status --short --untracked-files=all
git log -1 --oneline
git remote -v
git worktree list --porcelain
```

Never reset, clean, stash, checkout-overwrite, rewrite history, delete branches, or force-push to hide or simplify state.

## Repository map

- `backend/app/`: FastAPI routes, strict models, fictional fixtures, deterministic ranking.
- `backend/tests/`: API and domain tests.
- `frontend/src/`: React/TypeScript UI, API client, URL policy, styles, and component tests.
- `frontend/dist/`: generated production assets; do not hand-edit or commit unless policy changes explicitly.
- `tools/scan_public.py`: public-boundary scanner for current files and Git history.
- `tools/tests/`: scanner canary tests.
- `.github/workflows/ci.yml`: hosted governing checks.
- `docs/`: public architecture, API, and threat-model reference.

## Public scope

Allowed:

- Generic source-aware domain/API models.
- Fictional deterministic inbox, calendar, task, news, and service-status fixtures.
- Truth states: `live`, `scheduled`, `stale`, `unavailable`, `conflicting`.
- Recommendation, alternatives, exception-first queue, source authority/freshness/confidence display.
- Local read-only scenario controls, tests, CI, and public docs.

Forbidden:

- Private repository Git objects or copied operational artifacts.
- Personal, household, employment, client, account, email, calendar, vault, or live provider data.
- Real names or stable identifiers, private hosts/IPs/ports/services/paths, credentials, token references, runtime logs, handoffs, receipts, screenshots, or browser captures.
- Private-system adapters, extension identities, deployment topology, or claims of parity with any private deployment.
- Authentication, writable actions, live sources, proxying, arbitrary URLs, file/command execution, analytics, persistence, or deployment without a separately approved design.

Unknown scanner findings block publication. Do not allowlist or redact a finding until its origin and safety are proven. Canary tests must detect forbidden synthetic samples without printing values.

## Product invariants

- Exactly one recommended outcome and two alternatives.
- Every reason is grounded in named fictional sources.
- Exceptions precede routine records.
- Unavailable or unknown never becomes healthy/current.
- Source authority, freshness, confidence or availability, and safe detail state are visible in text.
- Scenario controls are labelled synthetic and read-only.
- All deep links remain same-origin and allowlisted.
- Error output is sanitized and nontechnical.
- API input and responses are closed and bounded.

## Accessibility

Use semantic HTML and native controls before ARIA. Maintain one page heading, landmarks, skip link, logical headings, full keyboard operation, visible focus, restrained polite status, non-color-only truth states, 320 CSS-pixel and 200% reflow, forced-colors support, and reduced motion. Every loading, empty, stale, unavailable, conflicting, and failure state must identify a safe recovery.

Automated DOM/axe results do not prove complete NVDA, VoiceOver, or installed high-contrast acceptance. State that limitation publicly.

## Security

- Validate at API and domain boundaries.
- Same-origin browser requests and local allowlisted links only.
- Strict response models; no unexpected fields.
- Sanitized client/server errors and no exception internals.
- Preserve CSP, frame denial, referrer, MIME-sniffing, and permissions headers.
- No browser secrets, external requests, generic proxy, command/file surface, unsafe deserialization, uploads, or templates accepting untrusted markup.
- Lock dependencies; unresolved high or critical advisories block release.

## TDD and implementation

Use vertical RED → GREEN → REFACTOR:

1. Add one focused failing behavior or negative test.
2. Run it and confirm the expected failure.
3. Add the smallest implementation.
4. Run focused and governing checks.
5. Refactor only while green.
6. Review tracked, staged, untracked, generated, and lockfile changes.
7. Freeze meaningful release candidates for independent exact-byte review.

Do not weaken tests, suppress errors, broaden allowlists, or label a focused pass as full acceptance.

## Setup and run

```bash
uv sync --locked
npm ci --prefix frontend
npm run build --prefix frontend
uv run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`.

## Governing verification

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

For a release candidate, also exercise the built same-origin app over real HTTP, cover every scenario, inspect generated assets, verify the exact committed export, and run a real-browser accessibility/responsive smoke where available.

## Git and public release

- Keep clean, professional, focused commits.
- Never commit `.env`, secrets, caches, virtual environments, `node_modules`, test caches, local databases, editor state, or evidence sprawl.
- Scan current files, generated output, staged bytes, package inventory, and all reachable history before public push.
- Require a fresh read-only exact-candidate review for release/security/accessibility changes.
- Verify local SHA equals remote `main`, CI is green on that SHA, visibility/default branch/settings are correct, and the repository is anonymously readable.
- Public publication is protected; it requires the repository owner's explicit approval.

## Stop and rollback

Stop for any private/secret/topology finding, candidate drift, access-boundary ambiguity, misleading claim, test/build/typecheck/lint failure, unresolved high/critical advisory, accessibility blocker, license problem, or unavailable independent review.

If a material issue is found after publication, make this new repository private immediately and report. Preserve evidence locally. Never force-push or rewrite public history. Do not deploy or touch any private runtime or repository.

## Definition of done

Done requires a working built app, exercised API and scenarios, passing governing checks, clean public and Git history scans, current documentation, accepted exact-candidate review, clean Git state, matching local/remote commit, green hosted CI, verified public readback, and honest residual limitations.
