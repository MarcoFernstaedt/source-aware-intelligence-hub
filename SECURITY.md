# Security Policy

## Supported version

Security fixes are maintained on the default branch.

## Report a vulnerability privately

Use this repository's **Security** tab, choose **Advisories**, then select **Report a vulnerability**. GitHub Private Vulnerability Reporting is the supported private intake route; do not open a public issue for a suspected vulnerability or disclosure.

Include the affected route or component, reproduction steps, impact, and any suggested mitigation. Do not include real credentials, personal data, or private system details in a report. Maintainers will acknowledge a complete report as soon as practical and coordinate disclosure after a fix is available.

## Security posture

This demonstration is designed to operate without secrets, accounts, databases, external requests, or writable integrations. Its API is read-only, inputs are bounded, links are local and allowlisted, browser policy headers are set by the application, and errors are intentionally generic.

If a real integration is ever proposed, it requires a separate threat model, secret mechanism, authentication and authorization design, privacy review, negative tests, and explicit release approval before code is accepted.
