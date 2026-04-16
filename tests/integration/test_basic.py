# Minimal integration test skeleton for openclaw-workspace
import json
import os
import subprocess
import sys

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def test_health():
    # Placeholder: implement actual health check endpoint or script
    assert os.path.exists("/root/.openclaw/workspace/docs/API.md")
    assert os.path.exists("/root/.openclaw/workspace/docs/SCOPE.md")
    rc, out, err = run_cmd("bash /root/.openclaw/workspace/scripts/healthcheck.sh")
    # Currently healthcheck outputs to terminal; ensure it runs without error
    assert rc == 0, f"healthcheck failed: {err}"

def test_skills_registered():
    skills_dir = "/root/.openclaw/workspace/skills"
    assert os.path.isdir(skills_dir), "skills directory missing"
    # At minimum, skills directory should contain known skill entries
    rc, out, err = run_cmd("ls -1 /root/.openclaw/workspace/skills/")
    assert rc == 0, f"cannot list skills: {err}"
    # Expect several skills present (non-zero count)
    lines = [l for l in out.strip().split("\n") if l]
    assert len(lines) > 0, "no skills found"

def test_api_outline_exists():
    assert os.path.exists("/root/.openclaw/workspace/docs/API.md"), "API outline missing"
    with open("/root/.openclaw/workspace/docs/API.md") as f:
        content = f.read()
        assert "Health API" in content or "health" in content.lower()
        assert "Task Queue API" in content or "Task" in content

if __name__ == "__main__":
    # Basic runner for manual execution
    for name in [test_health, test_skills_registered, test_api_outline_exists]:
        try:
            name()
            print(f"PASS: {name.__name__}")
        except AssertionError as e:
            print(f"FAIL: {name.__name__} — {e}")
            sys.exit(1)
    print("All basic integration checks passed.")