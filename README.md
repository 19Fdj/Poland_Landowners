# Poland Rural Landowner Finder

Internal web application for renewable-energy land acquisition teams working on Polish rural parcels. The app validates cadastral parcel identifiers, resolves parcel intelligence through connector-based public/demo sources, maps parcels, manages lawful ownership workflows, and records evidence and audit logs.

## Architecture

- `backend/`: FastAPI, SQLAlchemy, Alembic, Celery, Redis cache hooks, RBAC/auth, audit logging, connector pattern for parcel resolution.
- `frontend/`: Next.js 15 + TypeScript analyst UI with dashboard, parcel detail, imports, exports, and admin areas.
- `seeds/`: local demo parcel dataset for development without live cadastral dependencies.
- `docker-compose.yml`: app, worker, PostGIS, and Redis services.

## Compliance guardrails

- No CAPTCHA bypassing, paywall evasion, or access-control circumvention.
- Ownership data is only intended for lawful public or user-supplied records.
- Every ownership field must retain provenance, verification details, and confidence.
- Users remain responsible for confirming GDPR/legal basis before processing personal data.

## Local setup

1. Copy `.env.example` to `.env` and adjust secrets.
2. Run `make setup`.
3. Run database migrations or initialize demo data with `make seed`.
4. Start the stack with `make run`.
5. Open [http://localhost:3000](http://localhost:3000) and API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

Demo login seed:

- Email: `admin@example.com`
- Password: `password123`

## What is implemented

- Parcel validation endpoint: `POST /api/v1/parcels/validate`
- Bulk import endpoint: `POST /api/v1/parcels/import`
- Parcel listing/detail/refresh endpoints
- Ownership and document creation endpoints
- Export job lookup endpoint
- Health check endpoint
- Audit log admin endpoint
- Demo cadastral connector with source attribution
- Dashboard, parcel detail page, import/export/admin screens
- Pytest and Playwright starter coverage

## What is mocked

- Official cadastral resolution currently uses `DemoPolandParcelConnector`.
- Export generation is represented by job metadata rather than a full file worker.
- Document upload persists metadata, not binary file storage.
- Frontend falls back to local demo data when the backend is unavailable.

## What needs real credentials or legal review

- Live cadastral/public geospatial connectors and their rate limits.
- Production auth hardening, email delivery, and secure secret management.
- Final GDPR retention policy, DPA review, and ownership-data lawful-basis process.
- Storage policy for uploaded evidence files and screenshots.

## Testing

- Backend: `cd backend && pytest`
- Frontend E2E: `cd frontend && npm run test:e2e`

## Deployment

- Recommended frontend: `Vercel`
- Recommended backend: `Render`
- CI is configured in [ci.yml](/Users/josefranco/Documents/New%20project/.github/workflows/ci.yml)
- CD is configured in [deploy.yml](/Users/josefranco/Documents/New%20project/.github/workflows/deploy.yml)
- Render infrastructure blueprint lives in [render.yaml](/Users/josefranco/Documents/New%20project/render.yaml)

Required GitHub repository secrets for deployment:

- `VERCEL_TOKEN`: created in Vercel account settings
- `VERCEL_ORG_ID`: from the Vercel team/project settings
- `VERCEL_PROJECT_ID`: from the Vercel project settings
- `RENDER_DEPLOY_HOOK_URL`: from the Render service deploy hook settings

Required production environment variables:

- Backend:
  - `SECRET_KEY`
  - `DATABASE_URL`
  - `REDIS_URL`
  - `BACKEND_CORS_ORIGINS`
  - `LEGAL_DISCLAIMER_TEXT`
  - `MAP_STYLE_URL`
  - `DEMO_MODE`
- Frontend:
  - `NEXT_PUBLIC_API_BASE_URL`
  - `NEXT_PUBLIC_MAP_STYLE_URL`

## Next steps

- Replace demo connector with official source adapters behind the existing connector interface.
- Add real async import/export workers and binary document storage.
- Expand AOI tools, geospatial overlays, and admin RBAC workflows.
