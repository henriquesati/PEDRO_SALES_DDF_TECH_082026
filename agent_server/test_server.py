"""Automated test suite for Agent Server discovery, configuration, and endpoints."""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from fastapi.testclient import TestClient
from agent_server.discovery import scan_all_agents, scan_all_skills, get_skills_paths
from agent_server.server import app


def test_discovery_pure_functions():
    """Validates pure discovery functions for agents and skills."""
    print("Testing pure discovery functions...")
    agents = scan_all_agents()
    skills = scan_all_skills()
    skills_paths = get_skills_paths()

    assert len(agents) > 0, "No agents found in .agents/agents!"
    assert len(skills) > 0, "No skills found in .agents/skills!"
    assert len(skills_paths) == 1, "Skills path not resolved correctly!"

    agent_names = [a.name for a in agents]
    print(f"[OK] Discovered {len(agents)} agents: {agent_names}")

    skill_names = [s.name for s in skills]
    print(f"[OK] Discovered {len(skills)} skills: {skill_names[:5]}... (total {len(skills)})")


def test_fastapi_endpoints():
    """Validates FastAPI routes using TestClient."""
    print("\nTesting FastAPI HTTP endpoints...")
    client = TestClient(app)

    # 1. Healthcheck
    health_resp = client.get("/health")
    assert health_resp.status_code == 200, f"Healthcheck failed: {health_resp.text}"
    health_data = health_resp.json()
    assert health_data["status"] == "healthy"
    assert health_data["agents_count"] > 0
    assert health_data["skills_count"] > 0
    print(f"[OK] GET /health -> 200 OK | Agents: {health_data['agents_count']}, Skills: {health_data['skills_count']}")

    # 2. Agents list
    agents_resp = client.get("/agents")
    assert agents_resp.status_code == 200
    agents_list = agents_resp.json()
    assert len(agents_list) == health_data["agents_count"]
    print(f"[OK] GET /agents -> 200 OK | Count: {len(agents_list)}")

    # 3. Skills list
    skills_resp = client.get("/skills")
    assert skills_resp.status_code == 200
    skills_list = skills_resp.json()
    assert len(skills_list) == health_data["skills_count"]
    print(f"[OK] GET /skills -> 200 OK | Count: {len(skills_list)}")

def test_openapi_specification():
    """Validates OpenAPI 3.1.0 schema generation, tags, contact info, and interactive docs."""
    print("\nTesting OpenAPI 3.1.0 documentation & schema contracts...")
    client = TestClient(app)

    # 1. OpenAPI JSON spec
    openapi_resp = client.get("/openapi.json")
    assert openapi_resp.status_code == 200, f"OpenAPI spec failed: {openapi_resp.text}"
    schema = openapi_resp.json()

    assert schema["info"]["title"] == "Antigravity Agent Server"
    assert schema["info"]["version"] == "1.0.0"
    assert "contact" in schema["info"]
    assert "license" in schema["info"]
    assert "paths" in schema
    assert "/health" in schema["paths"]
    assert "/agents" in schema["paths"]
    assert "/skills" in schema["paths"]
    assert "/chat" in schema["paths"]
    assert "/stream" in schema["paths"]

    # Verify tags presence
    tags = [t["name"] for t in schema.get("tags", [])]
    assert "Health" in tags
    assert "Discovery" in tags
    assert "Inference" in tags
    print(f"[OK] GET /openapi.json -> 200 OK | Title: {schema['info']['title']} v{schema['info']['version']} | Tags: {tags}")

    # 2. Interactive Swagger UI
    docs_resp = client.get("/docs")
    assert docs_resp.status_code == 200
    assert "swagger" in docs_resp.text.lower() or "openapi" in docs_resp.text.lower()
    print("[OK] GET /docs -> 200 OK (Swagger UI)")

    # 3. Interactive ReDoc
    redoc_resp = client.get("/redoc")
    assert redoc_resp.status_code == 200
    assert "redoc" in redoc_resp.text.lower()
    print("[OK] GET /redoc -> 200 OK (ReDoc)")


if __name__ == "__main__":
    test_discovery_pure_functions()
    test_fastapi_endpoints()
    test_openapi_specification()
    print("\n*** ALL BACKEND & OPENAPI TESTS PASSED SUCCESSFULLY! ***")
