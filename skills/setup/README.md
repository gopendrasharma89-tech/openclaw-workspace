# Setup Guide for Skills Requiring Credentials

## Email (email-management / porteden-email)
1. For Gmail: Get App Password → `email-management` needs `~/email-management/` config
2. For Porteden: `porteden auth login` (browser) or set `PE_API_KEY` env var

## Notion (notion)
1. Create Integration at notion.so/my-integrations
2. Share database with integration
3. `export NOTION_KEY="ntn_xxx"`

## Trello (trello)
1. Get API Key: trello.com/power-ups/admin
2. Get Token: trello.com/1/appKey/generate
3. `export TRELLO_API_KEY="xxx"`
4. `export TRELLO_TOKEN="xxx"`

## Spotify (spotify-player)
1. Need Spotify Premium account
2. Create app at developer.spotify.com/dashboard
3. Install spogo for terminal control
4. Authorize with OAuth flow

## Todoist (todoist-rs)
1. Get API token: todoist.com/prefs/integrations
2. Install `td` CLI: `cargo install todoist-cli`
3. `export TODOIST_API_TOKEN="xxx"`

## Social Intelligence (social-intelligence)
1. Create account at xpoz.ai (free tier)
2. Install mcporter: `npm i -g mcporter`
3. Run `xpoz-setup` skill for auth

## Obsidian (obsidian)
1. Install Obsidian desktop app
2. Install obsidian-cli: `brew install yakitrak/yakitrak/obsidian-cli`
3. Ensure URI handler works (`obsidian://open`)

## Local Whisper (local-whisper)
1. Install pip: `pip3 install openai-whisper`
2. Model auto-downloads on first use
3. Requires ffmpeg (already installed ✅)
