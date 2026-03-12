#!/usr/bin/env python3
"""Quick smoke test for the three changed files."""

import sys
import os

# Extend path — always relative to *project root*, not CWD
# This file lives at <project>/tests/smoke_test.py
ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC      = os.path.join(ROOT, "src")
VAAI     = os.path.join(SRC, "villager_ai")
VAAI_MCP = os.path.join(VAAI, "mcp")  # flat import of villager_proper_mcp
# Note: put VAAI_MCP FIRST so `import villager_proper_mcp` resolves before
# Python tries to use the local mcp/ package (which only has __init__.py)
for p in [VAAI_MCP, VAAI, SRC]:
    if p not in sys.path:
        sys.path.insert(0, p)


PASS = []
FAIL = []


def check(label, fn):
    try:
        fn()
        PASS.append(label)
        print(f"  ✅  {label}")
    except Exception as e:
        FAIL.append(label)
        print(f"  ❌  {label}: {e}")


# ── 1. task_store ─────────────────────────────────────────────────────────────
print("\n=== task_store.py ===")

def test_task_store():
    from task_store import init_db, upsert_task, get_task, list_tasks, delete_task
    init_db()
    upsert_task("smoke-1", status="pending", abstract="Smoke test", description="Test", source="ci")
    upsert_task("smoke-1", status="completed", result="ok")
    row = get_task("smoke-1")
    assert row is not None, "get_task returned None"
    assert row["status"] == "completed", f"expected completed, got {row['status']}"
    assert row["result"] == "ok", f"expected ok, got {row['result']}"
    tasks = list_tasks(source="ci")
    assert any(t["task_id"] == "smoke-1" for t in tasks), "task not in list"
    delete_task("smoke-1")
    assert get_task("smoke-1") is None, "task should be deleted"

check("task_store CRUD + delete", test_task_store)


# ── 2. config ─────────────────────────────────────────────────────────────────
print("\n=== config.py ===")

def test_config_import_no_raise():
    """Import must not raise even without API keys."""
    # Temporarily clear keys
    old_key = os.environ.pop("ZAI_API_KEY", None)
    old_prov = os.environ.get("LLM_PROVIDER", "zai")
    os.environ["LLM_PROVIDER"] = "zai"
    try:
        # Re-import config fresh
        if "config" in sys.modules:
            del sys.modules["config"]
        import config  # noqa: F401 — must not raise
    finally:
        if old_key:
            os.environ["ZAI_API_KEY"] = old_key
        os.environ["LLM_PROVIDER"] = old_prov

check("config imports without API keys", test_config_import_no_raise)


def test_config_hexstrike_url():
    if "config" in sys.modules:
        del sys.modules["config"]
    os.environ.setdefault("ZAI_API_KEY", "test")
    import config
    assert hasattr(config, "HEXSTRIKE_MCP_URL"), "HEXSTRIKE_MCP_URL missing"
    assert hasattr(config, "validate_config"), "validate_config() missing"
    assert "hexstrike" in config.MCP.server.get("mcp_servers", {}), "hexstrike not in mcp_servers"

check("config HEXSTRIKE_MCP_URL + mcp_servers", test_config_hexstrike_url)


# ── 3. villager_proper_mcp — syntax check ─────────────────────────────────────
print("\n=== villager_proper_mcp.py (syntax) ===")

def test_syntax():
    import py_compile
    target = os.path.join(ROOT, "src", "villager_ai", "mcp", "villager_proper_mcp.py")
    assert os.path.exists(target), f"File not found: {target}"
    py_compile.compile(target, doraise=True)

check("villager_proper_mcp.py compiles cleanly", test_syntax)


# ── 4. MCP file imports (without Villager framework) ─────────────────────────
print("\n=== villager_proper_mcp.py (runtime import) ===")

def test_mcp_import():
    """Import the MCP module — Villager framework is absent so
    VILLAGER_AVAILABLE=False, but everything else must work."""
    os.environ.setdefault("ZAI_API_KEY", "test")
    # Direct import works now that VAAI_MCP is on sys.path
    import villager_proper_mcp as vpm
    print(f"      VILLAGER_AVAILABLE={vpm.VILLAGER_AVAILABLE}, "
          f"TASK_STORE_AVAILABLE={vpm.TASK_STORE_AVAILABLE}")
    v = vpm.VillagerProperMCP()
    status = v.get_system_status()
    assert status["task_store"] in ("sqlite", "memory"), status["task_store"]
    assert "hexstrike_url" in status

check("VillagerProperMCP instantiates", test_mcp_import)


def test_create_task_returns_id():
    import villager_proper_mcp as vpm
    v = vpm.VillagerProperMCP()
    tid = v.create_task("Smoke", "Smoke test task", source="ci-smoke")
    assert len(tid) == 36, f"expected UUID, got: {tid}"

check("create_task returns UUID", test_create_task_returns_id)


def test_create_mission_returns_id():
    import time
    import villager_proper_mcp as vpm
    v = vpm.VillagerProperMCP()
    tid = v.create_mission(
        mission="Recon test target",
        target_scope="10.0.0.1",
        constraints=["no exploitation"],
    )
    assert len(tid) == 36
    time.sleep(0.4)
    s = v.get_task_status(tid)
    assert s.get("source") == "hexclaw", f"expected hexclaw, got: {s.get('source')}"

check("create_mission sets source=hexclaw", test_create_mission_returns_id)


# ── Summary ───────────────────────────────────────────────────────────────────
print()
print("=" * 50)
print(f"PASSED: {len(PASS)}/{len(PASS) + len(FAIL)}")
if FAIL:
    print(f"FAILED: {FAIL}")
    sys.exit(1)
else:
    print("ALL TESTS PASSED")
