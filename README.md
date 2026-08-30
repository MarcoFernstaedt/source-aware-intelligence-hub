# Source-Aware Intelligence Hub

A public, credential-free full-stack demonstration of source-aware decision support.

Most dashboards make every record look equally reliable. This product makes truth state part of the interface: one recommended outcome is grounded in named sources, two alternatives remain visible, exceptions come first, and every source reports its authority, freshness, confidence or availability, and safe local detail state.

## What the product demonstrates

- A deterministic recommendation with short, source-grounded reasons.
- Two ranked alternatives rather than a single opaque answer.
- An exception-first attention queue.
- Normalized inbox, calendar, task, news, and service-status records.
- Explicit `live`, `scheduled`, `stale`, `unavailable`, and `conflicting` states.
- Interactive baseline, source-failure, and source-conflict scenarios.
- A responsive, keyboard-operable React interface with semantic landmarks and text equivalents.
- A small read-only FastAPI contract with bounded inputs and same-origin production serving.

All organizations, records, times, and source behavior are fictional and deterministic. The application has no credentials, live integrations, external mutation, proxy, command, or arbitrary URL surface. It is a portfolio demonstration, not a deployed production system.

## Architecture

```text
Browser
  └─ React + TypeScript interface
       └─ GET /api/workspace?scenario=...
            └─ FastAPI
                 └─ deterministic normalization and ranking service
                      └─ fictional in-memory fixtures
```

The production path is same-origin: Vite builds static assets, then FastAPI serves both the API and compiled interface. Business logic lives outside route handlers, response models reject unexpected fields, and deep links are restricted to local synthetic source paths.

More detail: [Architecture](docs/architecture.md) · [API contract](docs/api.md) · [Threat model](docs/threat-model.md)

## Run locally

Prerequisites: Python 3.12+, [uv](https://docs.astral.sh/uv/), Node.js 20+, and npm.

```bash
uv sync --locked
npm ci --prefix frontend
npm run build --prefix frontend
uv run uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`. Use the three failure-lab controls to compare ordinary, unavailable, and conflicting source conditions. No environment file or network credential is required.

## Verification

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
```

The scanner test includes synthetic negative canaries to prove detection without printing matched values. CI repeats all source, type, test, build, dependency, and current/history privacy gates.

## Accessibility

The interface uses native controls, visible focus, a skip link, heading and landmark structure, polite loading feedback, text labels for every truth state, 320 CSS-pixel reflow, reduced-motion behavior, and forced-colors-specific selected/error affordances. Automated axe coverage is included. Automated checks do not claim complete screen-reader, installed high-contrast, or physical-device acceptance.

## Limitations

- Data is deliberately synthetic and in memory.
- Ranking is deterministic rule logic, not a predictive model.
- Source detail links return to the demo interface; they do not open external systems.
- There is no authentication because there is no private data or writable action.
- Local and automated accessibility evidence does not replace assistive-technology testing for a production deployment.

## Development and security

Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes and [SECURITY.md](SECURITY.md) for private vulnerability reporting. Public-boundary checks are mandatory for every change. See [AGENTS.md](AGENTS.md) and [CLAUDE.md](CLAUDE.md) for the full repository contract.

Licensed under the [MIT License](LICENSE).
