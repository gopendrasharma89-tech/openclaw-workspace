# API — Initial Outline (openclaw-workspace)

## Purpose
Define the initial API surface and contract expectations for the openclaw-workspace so clients, integrations, and tests can interact consistently.

## Audience
- Developers working on integrations (e.g., Slack/Discord bots, CLI wrappers)
- Testers and QA
- Future maintainers

## Core API Contracts (v0)
### 1. Workspace State API
- Endpoint: internal/state
- Purpose: Provide read-only access to critical workspace state (git status, current task, health).
- Request: none (internal use)
- Response fields: commit, branch, dirty, task, last_heartbeat

### 2. Task Queue API (agent-autonomy-kit)
- Purpose: Query and update work queue (ready, in-progress, done).
- Actions:
  - GET /tasks — list tasks with status
  - POST /tasks/{id}/start — mark task in-progress
  - POST /tasks/{id}/done — mark task complete

### 3. Skills Registry API
- Purpose: Enumerate installed skills and metadata.
- GET /skills — list skills with id, source, status
- GET /skills/{id} — detail for a skill

### 4. Health API
- GET /health — return OK if core files present and git ok

## Message/Event Contracts (for internal events)
- task-started: { taskId, workerId, timestamp }
- task-completed: { taskId, result, timestamp }
- heartbeat: { at, status, issues[] }

## API Schemas (v0)
### 1. GET /health
- Request: none
- Response 200:
  ```json
  { "status": "ok", "uptime": 123, "timestamp": "2026-04-16T06:00:00Z" }
  ```

### 2. GET /tasks
- Request: none
- Response 200:
  ```json
  { "tasks": [ { "id": "uuid", "status": "ready|in-progress|done", "title": "string", "createdAt": "ISO8601" } ] }
  ```

### 3. POST /tasks/{id}/start
- Request: none (internal trigger)
- Response 200:
  ```json
  { "taskId": "uuid", "status": "in-progress", "startedAt": "ISO8601" }
  ```

### 4. POST /tasks/{id}/done
- Request: none (internal trigger)
- Response 200:
  ```json
  { "taskId": "uuid", "status": "done", "result": "string|object", "completedAt": "ISO8601" }
  ```

### 5. GET /skills
- Request: none
- Response 200:
  ```json
  { "skills": [ { "id": "string", "source": "clawhub|local", "status": "active|inactive" } ] }
  ```

## Auth & Security Notes
- Initial scope: local/internal usage — no auth required.
- Plan: add API key or token-based auth when external clients are introduced.
- Transport: use HTTP for external clients; stdin/stdout or file events for internal agent communication.

## Error Format (to be adopted)
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