# Portable workspace health check script
# Usage: bash scripts/healthcheck.sh

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "⚡ Kavi Workspace Health Check"
echo "=============================="
echo ""

# Git
cd "$ROOT"
echo "📦 Git Status:"
git status --short 2>/dev/null || echo "  (not a git repo or no git)"
echo "  Last commit: $(git log --oneline -1 2>/dev/null || echo 'none')"
echo ""

# Core Files
cd "$ROOT"
echo "📄 Core Files:"
for f in AGENTS.md SOUL.md IDENTITY.md USER.md MEMORY.md TOOLS.md SKILLS.md README.md HEARTBEAT.md; do
  if [ -f "$ROOT/$f" ]; then
    echo "  ✅ $f ($(wc -l < "$ROOT/$f") lines)"
  else
    echo "  ❌ $f MISSING"
  fi
done
echo ""

# Directories
cd "$ROOT"
echo "📁 Directories:"
for d in memory projects scripts; do
  count=$(find "$ROOT/$d" -maxdepth 1 -type f 2>/dev/null | wc -l)
  echo "  ✅ $d/ ($count files)"
done
echo ""

# Self-improving
cd "$ROOT"
echo "🧠 Self-improving:"
if [ -d "$ROOT/self-improving" ]; then
  for md in "$ROOT/self-improving"/*.md; do
    [ -f "$md" ] && echo "  ✅ $(basename "$md") ($(wc -l < "$md") lines)"
  done
else
  echo "  (no self-improving directory)"
fi
echo ""

# Proactivity
cd "$ROOT"
echo "⚡ Proactivity:"
if [ -d "$ROOT/proactivity" ]; then
  for md in "$ROOT/proactivity"/*.md; do
    [ -f "$md" ] && echo "  ✅ $(basename "$md") ($(wc -l < "$md") lines)"
  done
else
  echo "  (no proactivity directory)"
fi
echo ""

# Skills
cd "$ROOT"
SKILL_COUNT=$(find "$ROOT/skills" -name 'SKILL.md' 2>/dev/null | wc -l)
echo "🔧 Skills: $SKILL_COUNT installed at skills/"
echo ""

echo "✅ Health check done."