# 🐙 Workspace Health Check Script
# Usage: Run this to quickly check workspace status
# bash ~/.openclaw/workspace/scripts/healthcheck.sh

set -e

WS="/root/.openclaw/workspace"

echo "⚡ Kavi Workspace Health Check"
echo "=============================="
echo ""

# Git
echo "📦 Git Status:"
cd "$WS"
git status --short 2>/dev/null || echo "  ❌ Not a git repo"
echo "  Last commit: $(git log --oneline -1 2>/dev/null || echo 'none')"
echo ""

# Core Files
echo "📄 Core Files:"
for f in AGENTS.md SOUL.md IDENTITY.md USER.md MEMORY.md TOOLS.md SKILLS.md README.md HEARTBEAT.md; do
  if [ -f "$WS/$f" ]; then
    echo "  ✅ $f ($(wc -l < "$WS/$f") lines)"
  else
    echo "  ❌ $f MISSING"
  fi
done
echo ""

# Directories
echo "📁 Directories:"
for d in memory projects scripts; do
  count=$(find "$WS/$d" -type f 2>/dev/null | wc -l)
  echo "  ✅ $d/ ($count files)"
done
echo ""

# External
echo "🧠 Self-improving:"
ls -1 /root/self-improving/*.md 2>/dev/null | while read f; do
  echo "  ✅ $(basename $f) ($(wc -l < "$f") lines)"
done
echo ""
echo "⚡ Proactivity:"
ls -1 /root/proactivity/*.md 2>/dev/null | while read f; do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 0 ]; then
    echo "  ✅ $(basename $f) ($lines lines)"
  else
    echo "  ⚠️ $(basename $f) (empty)"
  fi
done
echo ""

# Skills
SKILL_COUNT=$(find /root/.openclaw/skills -name 'SKILL.md' | wc -l)
echo "🔧 Skills: $SKILL_COUNT installed at ~/.openclaw/skills/"
echo ""
echo "Done."
