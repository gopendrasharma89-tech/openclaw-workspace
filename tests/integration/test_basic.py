import os
import json

import jsonschema

def project_root():
    # Walk up from this file to repo root (where 'scripts/' exists)
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

def _load_schema(relpath):
    with open(os.path.join(ROOT, relpath)) as f:
        return json.load(f)

def test_health():
    script = os.path.join(ROOT, "scripts", "healthcheck.sh")
    assert os.path.exists(script), f"missing: {script}"
    rc, out, err = run_cmd(f"bash {script}")
    assert rc == 0, f"healthcheck failed: {err}"

def test_skills_registered():
    d = os.path.join(ROOT, "skills")
    assert os.path.isdir(d), f"missing skills dir: {d}"
    rc, out, err = run_cmd(f"ls -1 {d}")
    assert rc == 0, f"ls failed: {err}"
    assert len([l for l in out.strip().split("\n") if l]) > 0, "no skills"

def test_api_outline_exists():
    api_path = os.path.join(ROOT, "docs", "API.md")
    assert os.path.exists(api_path), f"missing API.md: {api_path}"
    with open(api_path) as f:
        c = f.read().lower()
        assert "get /health" in c or "health" in c
        assert "get /tasks" in c or "task" in c
        assert "post /tasks" in c or "status" in c
        assert "envelope" in c

def test_health_schema():
    schema = _load_schema("schemas/health.json")
    example = {
        "data": {"status": "ok", "uptimeSeconds": 0, "timestamp": "2026-04-16T06:00:00Z"},
        "meta": {"requestId": "test", "timestamp": "2026-04-16T06:00:00Z", "version": "v0"}
    }
    jsonschema.validate(instance=example, schema=schema)

def test_error_schema():
    schema = _load_schema("schemas/error.json")
    example = {
        "error": {"code": "ERR_INVALID_REQUEST", "message": "test"},
        "meta": {"requestId": "test", "timestamp": "2026-04-16T06:00:00Z", "version": "v0"}
    }
    jsonschema.validate(instance=example, schema=schema)