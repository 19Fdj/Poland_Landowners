# Legal and Compliance Guardrails

## Intended use

This application is for lawful due diligence in renewable-energy land acquisition workflows. It is designed to help analysts validate and enrich Polish cadastral parcel identifiers and to organize evidence-backed ownership workflows.

## Explicit prohibitions

- No CAPTCHA bypassing.
- No authentication, paywall, or access-control evasion.
- No scraping of non-public personal data.
- No unsupported owner-identity inference.

## Ownership workflow rules

- Store ownership information only when it comes from a lawful public source or a user-supplied verified record.
- Keep provenance for every ownership field: source type, source reference, verified by, verified at, and confidence.
- Prefer linking users to official registry search pages instead of automating around registry controls.

## GDPR-conscious design

- Data minimization: store only the fields required for diligence.
- Retention: define and configure retention periods before production use.
- Access logging: all reads and changes to ownership-related data should be logged.
- Lawful basis: users must confirm the legal basis for personal-data processing within their organization.

## Integration review required before production

- Confirm each cadastral or geospatial source permits the planned access pattern.
- Validate export controls for downstream CRMs, outreach tooling, and external sharing.
- Review role-based permissions and retention settings with counsel and DPO.

