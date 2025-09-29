#!/usr/bin/env python3
"""
Serve Villager FastAPI and expose MCP stdio tools in one process.
"""

import asyncio
import uvicorn
import logging
from importlib import import_module
import os
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure project root and this directory are importable
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(THIS_DIR, ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)


async def start_fastapi() -> None:
    app = import_module('villager_server').app
    config = uvicorn.Config(app=app, host='0.0.0.0', port=37695, log_level='info')
    server = uvicorn.Server(config)
    try:
        from villager_visuals import create_banner
        print(create_banner())
    except Exception:
        pass
    logger.info('🚀 Starting Villager FastAPI server on 0.0.0.0:37695')
    await server.serve()


async def start_mcp() -> None:
    # Import without relative path issues
    try:
        from villager_http_mcp import run as run_mcp
    except Exception:
        # Fallback: load by file location
        import importlib.util
        spec = importlib.util.spec_from_file_location('villager_http_mcp', os.path.join(THIS_DIR, 'villager_http_mcp.py'))
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        run_mcp = mod.run
    import sys
    sys.argv = ['villager_http_mcp', '--server', 'http://127.0.0.1:37695']
    logger.info('🤖 Starting MCP stdio server targeting http://127.0.0.1:37695')
    await run_mcp()


async def main() -> None:
    await asyncio.gather(
        start_fastapi(),
        start_mcp(),
    )


if __name__ == '__main__':
    asyncio.run(main())
