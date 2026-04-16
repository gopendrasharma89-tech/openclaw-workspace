#!/usr/bin/env python3
"""
Generate concrete example payloads from openapi.yaml for known endpoints.
"""
import yaml, json, os

SPEC_PATH = "openapi.yaml"
OUT_DIR = "docs/examples"
os.makedirs(OUT_DIR, exist_ok=True)

with open(SPEC_PATH) as f:
    spec = yaml.safe_load(f)

paths = spec.get("paths", {})
components = spec.get("components", {})
schemas = components.get("schemas", {})

def resolve_ref(ref):
    if not ref or not ref.startswith("#/"):
        return None
    parts = ref[2:].split("/")
    cur = components
    for p in parts:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return None
    return cur

def make_example(schema):
    if not schema:
        return None
    if "$ref" in schema:
        resolved = resolve_ref(schema["$ref"])
        if resolved:
            return make_example(resolved)
        return {"_ref": schema["$ref"]}
    typ = schema.get("type")
    if typ == "object":
        obj = {}
        for k, v in schema.get("properties", {}).items():
            if "enum" in v:
                obj[k] = v["enum"][0]
            elif v.get("type") == "string":
                obj[k] = "example"
            elif v.get("type") == "integer":
                obj[k] = 0
            elif v.get("type") == "boolean":
                obj[k] = False
            elif v.get("type") == "array":
                items = v.get("items", {})
                if "enum" in items:
                    obj[k] = items["enum"]
                else:
                    obj[k] = [make_example(items)]
            else:
                val = make_example(v)
                obj[k] = val if val not in ({}, None) else "example"
        return obj
    if typ == "array":
        items = schema.get("items", {})
        if "enum" in items:
            return items["enum"]
        return [make_example(items)]
    if "enum" in schema:
        return schema["enum"][0]
    if typ == "string":
        return "example"
    if typ == "integer":
        return 0
    return {}

# Override: provide concrete examples per operationId
def concrete_example(oid):
    examples = {
        "healthCheck": {
            "path": "/health",
            "method": "GET",
            "operationId": "healthCheck",
            "requestExamples": {},
            "responseExamples": {
                "200": {
                    "status": "ok",
                    "uptimeSeconds": 123,
                    "timestamp": "2026-04-16T06:00:00Z",
                    "_note": "matches HealthResponse schema"
                }
            }
        },
        "listTasks": {
            "path": "/tasks",
            "method": "GET",
            "operationId": "listTasks",
            "requestExamples": {},
            "responseExamples": {
                "200": {
                    "tasks": [
                        {
                            "id": "task-uuid-1",
                            "status": "ready",
                            "title": "Example task",
                            "description": "An example task description.",
                            "createdAt": "2026-04-16T06:00:00Z",
                            "updatedAt": "2026-04-16T06:00:00Z"
                        }
                    ],
                    "_note": "matches TaskList schema"
                }
            }
        }
    }
    return examples.get(oid)

for path_str, methods in paths.items():
    for method, spec in methods.items():
        if not isinstance(spec, dict):
            continue
        operation_id = spec.get("operationId")
        if not operation_id:
            continue
        # Use concrete example if available, otherwise generate
        out = concrete_example(operation_id)
        if out:
            outfile = os.path.join(OUT_DIR, f"{operation_id}.json")
            with open(outfile, "w") as f:
                json.dump(out, f, indent=2)
            print(f"Generated {outfile}")
        else:
            # fallback to generic generation
            request_examples = {}
            response_examples = {}
            if "requestBody" in spec:
                content = spec["requestBody"].get("content", {})
                for mime, body in content.items():
                    if "schema" in body:
                        request_examples[mime] = make_example(body["schema"])
            responses = spec.get("responses", {})
            for code, resp in responses.items():
                content = resp.get("content", {})
                for mime, body in content.items():
                    if "schema" in body:
                        example = make_example(body["schema"])
                        if example == {} and "$ref" in body["schema"]:
                            example = {"_ref": body["schema"]["$ref"]}
                        response_examples[code] = example
            if request_examples or response_examples:
                out = {
                    "path": path_str,
                    "method": method.upper(),
                    "operationId": operation_id,
                    "requestExamples": request_examples,
                    "responseExamples": response_examples,
                }
                outfile = os.path.join(OUT_DIR, f"{operation_id}.json")
                with open(outfile, "w") as f:
                    json.dump(out, f, indent=2)
                print(f"Generated {outfile}")

print("Example generation complete.")