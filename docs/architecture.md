# Architecture

## Goal

Turn heterogeneous source records into an honest decision brief without hiding freshness, availability, or disagreement.

## Components

- `backend/app/models.py` defines strict normalized source, attention, decision, and workspace contracts.
- `backend/app/fixtures.py` owns deterministic fictional fixtures and scenario transforms.
- `backend/app/service.py` owns deterministic ranking and explanations.
- `backend/app/main.py` exposes two read-only API routes, applies browser security headers, sanitizes validation errors, and serves the production frontend when built.
- `frontend/src/api.ts` owns same-origin fetch and minimal runtime contract verification.
- `frontend/src/App.tsx` owns scenario state and accessible projection of recommendations, exceptions, and source truth.
- `frontend/src/security.ts` independently allowlists local synthetic deep links.
- `tools/scan_public.py` scans current text and every reachable commit/path/blob occurrence for disclosure classes without printing values.

## Data flow

1. The browser requests one of three bounded scenarios.
2. The service creates the same baseline fixture on every request.
3. A scenario transform changes source truth without deleting provenance.
4. The service returns one recommendation, two alternatives, attention items, and normalized source cards.
5. The interface renders the result only after basic response-shape verification.
6. Missing, malformed, or failed responses produce an explicit unavailable state with retry; they do not fabricate healthy content.

## Product laws

1. Truth state is data, not decoration.
2. Recommendations cite the exact normalized sources used.
3. Unavailable confidence is `null`, never zero or an invented percentage.
4. Conflicts remain visible until an authority resolves them.
5. Exceptions precede ordinary evidence in reading order.
6. No route mutates external or durable state.
7. No browser destination escapes the local synthetic detail namespace.

## Deployment and rollback

The supported demonstration path builds the frontend and starts FastAPI on loopback. There is no production deployment in this repository. Rollback is a normal revert to the last verified commit; there are no migrations, credentials, background jobs, or durable data to compensate.
