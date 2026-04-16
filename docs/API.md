# API — Initial Outline (openclaw-workspace)

## Purpose
Define the initial API surface and contract expectations for the openclaw-workspace so clients, integrations, and tests can interact consistently.

## Audience
- Developers working on integrations (e.g., Slack/Discord bots, CLI wrappers)
- Testers and QA
- Future maintainers

## Core API Contracts (v0)

### Common envelope
All successful responses include:
```json
{ "data": { ... }, "meta": { "requestId": "uuid", "timestamp": "2026-04-16T06:00:00Z", "version": "v0" } }
```
Schema: `schemas/health.json`

### Error envelope
```json
{
  "error": {
    "code": "ERR_INVALID_REQUEST | ERR_NOT_FOUND | ERR_INTERNAL",
    "message": "human-readable description",
    "details": { /* optional structured details */ }
  },
  "meta": { "requestId": "uuid", "timestamp": "...", "version": "v0" }
}
```
Schema: `schemas/error.json`
HTTP status codes: 200 OK, 400 Bad Request, 404 Not Found, 500 Internal Server Error.

### 1. GET /health
- Request: none
- Response 200:
  ```json
  { "data": { "status": "ok", "uptimeSeconds": 123, "timestamp": "2026-04-16T06:00:00Z" }, "meta": { ... } }
  ```

### 2. GET /tasks
- Request: none
- Response 200:
  ```json
  { "data": { "tasks": [ {
    "id": "uuid",
    "status": "ready | in-progress | done",
    "title": "string",
    "description": "string",
    "createdAt": "2026-04-16T06:00:00Z",
    "updatedAt": "2026-04-16T06:00:00Z"
  } ] }, "meta": { ... } }
  ```

### 3. POST /tasks/{id}/start
- Request body: none (internal trigger)
- Response 200:
  ```json
  { "data": {
    "taskId": "uuid",
    "status": "in-progress",
    "startedAt": "2026-04-16T06:00:00Z",
    "message": "string"
  }, "meta": { ... } }
  ```

### 4. POST /tasks/{id}/done
- Request body: none (internal trigger)
- Response 200:
  ```json
  { "data": {
    "taskId": "uuid",
    "status": "done",
    "result": "string | object",
    "completedAt": "2026-04-16T06:00:00Z"
  }, "meta": { ... } }
  ```

### 5. GET /skills
- Request: none
- Response 200:
  ```json
  { "data": { "skills": [ {
    "id": "string",
    "source": "clawhub | local",
    "status": "active | inactive",
    "name": "string",
    "version": "string"
  } ] }, "meta": { ... } }
  ```

## Auth & Security Notes
- Initial scope: local/internal usage — no auth required.
- Plan: add API key or token-based auth when external clients are introduced.
- Transport: use HTTP for external clients; stdin/stdout or file events for internal agent communication.

## Error Format
- Standard error response:
  ```json
  { "error": { "code": "ERR_INVALID_REQUEST", "message": "human-readable description" } }
  ```

## Minimal Integration Test Skeleton
- Verify /health returns OK and schema shape.
- Verify /skills returns non-empty list.
- Verify /tasks returns an array (possibly empty) and conforms to schema.

## Versioning & Change Policy
- v0: Initial outline — subject to change.
- Semantic versioning will be adopted once public clients exist.

## Notes & Open Questions
- Transport/protocol: decide between HTTP, stdin/stdout messages, or file-based events.
- Error format: adopt consistent error codes/messages as above.
- Expand concrete schemas and add validation on server side.