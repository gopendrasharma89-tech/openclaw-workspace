# TOOLS.md - Environment & Tooling Reference

## Environment

- **Host:** Linux 5.15.178 (arm64)
- **Node:** v24.2.0
- **OpenClaw:** installed via npm
- **Workspace:** `/root/.openclaw/workspace`
- **Self-improving data:** `~/self-improving/`
- **Proactivity data:** `~/proactivity/`

## CLI Tools Available

| Tool | Purpose |
|------|---------|
| `clawhub` | Skill marketplace CLI |
| `git` | Version control |
| `curl` | HTTP requests |
| `wget` | Downloads |

## ClawHub CLI

```bash
clawhub search "topic"     # Find skills
clawhub install <skill>    # Install
clawhub update --all       # Update all
clawhub list               # ⚠️ Reports 0 (CLI bug — see SKILLS.md)
```

For full skills inventory: **see [SKILLS.md](./SKILLS.md)**

## TTS

- **Available:** `tts` tool (built-in)
- Preferred voice: _(to be discovered)_

## Messaging

- **Current channel:** webchat
- **Planned:** WhatsApp / Telegram (not configured yet)

---

Add whatever helps you do your job. This is your cheat sheet.
