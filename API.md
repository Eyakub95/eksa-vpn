# EKSA VPN API

Base URL (local): `http://localhost:8000`

## Admin authentication
`POST /auth/token` with form fields `username` (admin email) and `password`.
Use returned `access_token` as `Authorization: Bearer <token>`.

## Admin endpoints
- `GET /admin/users`
- `POST /admin/users`
  ```json
  {"email":"client@example.com","password":"AtLeast12Chars!","expires_at":"2026-12-01T00:00:00Z","quota_bytes":10737418240}
  ```
- `PATCH /admin/users/{id}`
  ```json
  {"is_active":false,"quota_bytes":5368709120}
  ```
- `GET /admin/servers`
- `POST /admin/servers`
  ```json
  {"name":"EKSA Saudi","country":"Saudi Arabia","region":"Riyadh","hostname":"sa.example.net","port":443,"protocol":"VLESS"}
  ```

## Client endpoints
- `GET /me`
- `GET /client/config`

Node credentials are intentionally not returned by this starter API. A production implementation
should issue short-lived per-user tunnel credentials through a secured provisioning service.
