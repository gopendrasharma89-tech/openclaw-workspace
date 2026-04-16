import os, sys

def project_root():
    # Walk up from this file until we find the 'scripts' directory
    path = os.path.abspath(__file__)
    while True:
        parent = os.path.dirname(path)
        if os.path.exists(os.path.join(parent, "scripts")) or parent == path:
            return parent
        path = parent

ROOT = project_root()

def run_cmd(cmd):
    import subprocess
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

def test_health():
    p = os.path.join(ROOT, "scripts", "healthcheck.sh")
    assert os.path.exists(p), f"missing: {p}"
    rc, out, err = run_cmd(f"bash {p}")
    assert rc == 0, f"healthcheck failed: {err}"

def test_skills_registered():
    d = os.path.join(ROOT, "skills")
    assert os.path.isdir(d), f"missing skills dir: {d}"
    rc, out, err = run_cmd(f"ls -1 {d}")
    assert rc == 0, f"ls failed: {err}"
    assert len([l for l in out.strip().split("\n") if l]) > 0, "no skills"

def test_api_outline_exists():
    p = os.path.join(ROOT, "docs", "API.md")
    assert os.path.exists(p), f"missing API.md: {p}"
    with open(p) as f:
        c = f.read().lower()
        assert "get /health" in c or "health" in c
        assert "get /tasks" in c or "task" in c
        assert "post /tasks" in c or "status" in c
        assert "envelope" in c

for name in [test_health, test_skills_registered, test_api_outline_exists]:
    try:
        name()
        print(f"PASS: {name.__name__}")
    except AssertionError as e:
        print(f"FAIL: {name.__name__} — {e}")
        sys.exit(1)
print("All checks passed.")
