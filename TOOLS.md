# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Environment

- **Host:** Linux 5.15.178 (arm64)
- **Node:** v24.2.0
- **OpenClaw:** installed via npm
- **CLI tools available:** `clawhub`, `git`, `curl`, `wget`
- **Workspace:** `/root/.openclaw/workspace`
- **Self-improving data:** `~/self-improving/`
- **Proactivity data:** `~/proactivity/`

## ClawHub CLI

```bash
# Search skills
clawhub search "query"

# Install a skill
clawhub install <skill-name>

# Update all skills
clawhub update --all

# List installed skills
clawhub list

# Registry: https://clawhub.com (default)
```

## Installed Skills

| Skill | Source | Location |
|-------|--------|----------|
| clawflow | Built-in | `/usr/local/lib/node_modules/openclaw/skills/clawflow` |
| clawflow-inbox-triage | Built-in | `.../skills/clawflow-inbox-triege` |
| healthcheck | Built-in | `.../skills/healthcheck` |
| node-connect | Built-in | `.../skills/node-connect` |
| skill-creator | Built-in | `.../skills/skill-creator` |
| weather | Built-in | `.../skills/weather` |
| self-improving | ClawHub | `/root/.openclaw/skills/self-improving` |
| proactivity | ClawHub | `/root/.openclaw/skills/proactivity` |

## TTS

- **Available:** `tts` tool (built-in)
- Preferred voice: _(to be discovered)_

## Messaging

- **Current channel:** webchat
- **Planned:** WhatsApp / Telegram (not configured yet)

---

Add whatever helps you do your job. This is your cheat sheet.
