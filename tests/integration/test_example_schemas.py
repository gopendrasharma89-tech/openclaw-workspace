import os
import json

import jsonschema

def project_root():
    path = os.path.abspath(__file__)
    while True:
        parent = os.path.dirname(path)
        if os.path.exists(os.path.join(parent, "scripts")) or parent == path:
            return parent
        path = parent

ROOT = project_root()

def load_json(relpath):
    with open(os.path.join(ROOT, relpath)) as f:
        return json.load(f)

def test_generated_examples_against_schemas():
    examples_dir = os.path.join(ROOT, "docs", "examples")
    for fname in os.listdir(examples_dir):
        if not fname.endswith(".json"):
            continue
        example = load_json(os.path.join("docs", "examples", fname))
        assert "operationId" in example, f"{fname} missing operationId"
        assert "responseExamples" in example, f"{fname} missing responseExamples"
        op_id = example["operationId"]
        for code, payload in example.get("responseExamples", {}).items():
            if isinstance(payload, dict) and payload.get("_ref"):
                continue  # skip placeholder refs
            if op_id == "healthCheck":
                schema = load_json("schemas/health.json")
                jsonschema.validate(instance=payload, schema=schema)
            elif op_id == "listTasks":
                # validate envelope wrapper
                assert "data" in payload and "meta" in payload
                assert "tasks" in payload["data"]
                tasks = payload["data"]["tasks"]
                for task in tasks:
                    assert "id" in task and isinstance(task["id"], str)
                    assert "status" in task and task["status"] in ("ready", "in-progress", "done")
                    assert "title" in task and isinstance(task["title"], str)

def test_generated_schemas_are_reachable():
    schemas = ["schemas/health.json", "schemas/error.json"]
    for s in schemas:
        assert os.path.exists(os.path.join(ROOT, s)), f"schema missing: {s}"