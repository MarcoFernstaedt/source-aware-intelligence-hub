# API Contract

Base path: `/api`. Responses use JSON. The API is read-only and requires no credentials because it serves deterministic fictional data only.

## `GET /api/health`

Response:

```json
{ "status": "ok", "mode": "synthetic-demo" }
```

## `GET /api/workspace`

Query parameter:

- `scenario`: optional, maximum 16 characters, exactly `baseline`, `degraded`, or `conflict`; defaults to `baseline`.

Success returns:

- `scenario`: selected scenario.
- `generated_at`: fixed fictional snapshot timestamp.
- `recommendation`: title, summary, one to three reasons, and source identifiers.
- `alternatives`: exactly two decisions with the same grounding contract.
- `attention`: zero or more exception-first items with severity and source identifiers.
- `sources`: normalized records with identifier, type, title, summary, authority, freshness, truth state, confidence or `null`, and a local synthetic deep link.

`truth_state` is one of `live`, `scheduled`, `stale`, `unavailable`, or `conflicting`.

Validation failures return status 422 and a generic bounded-input message. Internal traces and exception details are not returned.

## Non-contract surfaces

There are no POST, PUT, PATCH, DELETE, proxy, command, upload, authentication, provider, callback, or webhook routes. Frontend detail paths are static demo routes and do not dereference external URLs.
