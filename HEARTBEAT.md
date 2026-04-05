# HEARTBEAT.md

## Self-Improving Check

- Read `./skills/self-improving/heartbeat-rules.md`
- Use `~/self-improving/heartbeat-state.md` for last-run markers and action notes
- If no file inside `~/self-improving/` changed since the last reviewed change, return `HEARTBEAT_OK`

## Proactivity Check

- Read ~/proactivity/heartbeat.md
- Re-check active blockers, promised follow-ups, stale work, and missing decisions
- Ask what useful check-in or next move would help right now
- Message the user only when something changed or needs a decision
- Update ~/proactivity/session-state.md after meaningful follow-through

## Task Queue Integration (agent-autonomy-kit)

- Check `tasks/QUEUE.md` for work items
- Always pick a "Ready" task when idle
- Mark "Done" items when completed
- Never skip the queue for new work without asking

## Daily Routines

### Morning (when heartbeat after 04:00 UTC / 09:30 IST)
- Run morning-routine skill
- Review tasks/QUEUE.md
- Check calendar/weather if relevant
- Plan top 3 priorities for the day

### Evening (when heartbeat after 17:00 UTC / 22:30 IST)
- Run daily-review-ritual skill
- Update journal with reflections
- Archive completed tasks
- Prepare tomorrow's priorities

### Night (when heartbeat after 20:00 UTC / 01:30 IST)
- Run night-routine skill
- Ensure nothing critical is left open
- Update session-state for next morning
