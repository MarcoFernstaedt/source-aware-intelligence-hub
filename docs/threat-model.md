# Threat Model

## Assets and trust boundaries

The repository contains only public source, deterministic fictional fixtures, tests, and documentation. The browser trusts same-origin application responses but must treat deep-link strings and response shapes as untrusted. The FastAPI boundary accepts one bounded query value. Git history is part of the public release surface.

## Primary threats and controls

- **Disclosure through source or history:** a fail-closed scanner checks current text and every reachable commit/path/blob occurrence; canary tests prove detector sensitivity without echoing values.
- **Secret exposure:** the design requires no secret; ignore rules cover local environment and credential files; CI performs dependency and disclosure checks.
- **Fabricated health:** unavailable confidence is `null`, conflicts are explicit, failed fetches render an error, and tests cover all truth states.
- **Unsafe navigation:** backend validation and frontend `safeLocalLink` restrict destinations to the local synthetic source namespace.
- **Injection and arbitrary network access:** no HTML injection, proxy, fetch-by-URL, command, upload, or provider surface exists.
- **Cross-origin or external mutation:** the API exposes GET only, browser requests use same-origin credentials policy, and the interface labels all apparent activity as read-only demonstration.
- **Browser embedding and content loading:** content security, frame denial, referrer, MIME-sniffing, and permissions headers are applied to responses.
- **Denial of service:** query length and enum values are bounded; fixture volume and response size are fixed.
- **Dependency compromise:** Python and JavaScript dependency graphs are locked, CI audits them, and the stack is intentionally small.

## Out of scope

Authentication, authorization, multi-user isolation, live data retention, provider tokens, writable actions, webhooks, and production hosting are intentionally absent. Adding any one changes the trust model and requires a new security design and approval before implementation.
