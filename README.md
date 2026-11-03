# EKSA VPN — starter project

A low-cost, lawful VPN service starter with:
- FastAPI backend + PostgreSQL
- Admin API for users, servers and subscriptions
- Minimal bilingual-ready admin web UI (English/Bangla labels)
- Android Kotlin VPN app shell using Android `VpnService`
- Docker Compose for local backend/database development

## Important scope
This starter does **not** include a working V2Ray/Xray tunnel engine, production payment processing,
or carrier-billing bypass. The Android app currently requests Android VPN permission and provides
the integration point for a properly licensed V2Ray/Xray client core. A real VPN connection requires
integrating and testing that core, configuring lawful VPS nodes, TLS, routing, DNS, monitoring and
abuse controls. Use only networks and data plans you are authorized to use.

## 1) Run backend locally

Requirements: Docker + Docker Compose.

```bash
cp .env.example .env
# Change SECRET_KEY before any non-local use.
docker compose up --build
```

API docs: http://localhost:8000/docs
Health: http://localhost:8000/health

Create the first admin from inside the API container:

```bash
docker compose exec api python -m app.create_admin
```

Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `.env` first. The command refuses to create a
duplicate account.

## 2) API overview

- `POST /auth/token` — admin login; returns bearer token
- `GET /admin/users` — list users
- `POST /admin/users` — create user
- `PATCH /admin/users/{id}` — update active state, expiry and traffic quota
- `GET /admin/servers` — list VPN nodes
- `POST /admin/servers` — add a node
- `GET /client/config` — authenticated user's enabled server catalogue

All admin routes require an admin bearer token. Client routes require a user bearer token.
The demo admin interface is intentionally minimal; use `/docs` to exercise APIs.

## 3) Database
Tables:
- `accounts`: login identity, role, active status
- `vpn_servers`: node metadata (never store private keys in this table)
- `subscriptions`: expiry and quota per account
- `usage_records`: usage counters reported by trusted node agents

For a real deployment, usage must be reported by trusted server-side node agents, not accepted
as arbitrary client-supplied values.

## 4) Android app
Open `android/` in Android Studio. It contains:
- VPN permission flow
- foreground VPN service skeleton
- server list model / API integration TODO

The service deliberately does not claim "connected" until a tunnel engine is integrated.
Implement the Xray/V2Ray core adapter using the core project's documented Android integration
and licensing terms. Keep server credentials short-lived and fetch them over HTTPS after login.

## 5) Deployment checklist
- Use a supported Ubuntu LTS VPS in Saudi Arabia and Europe, subject to provider availability.
- Use unique SSH keys; disable password SSH after confirming key access.
- Restrict admin panel/API access; enable HTTPS and firewall rules.
- Keep node management ports private; do not expose panel ports publicly.
- Rotate secrets; back up PostgreSQL; monitor bandwidth, CPU, abuse and logs.
- Publish clear acceptable-use, privacy and refund policies.
- Confirm VPS provider and local legal requirements before offering paid service.
