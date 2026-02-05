@echo off
echo Starting MCP Proxy for Continue...
echo ========================================

REM Check if server is running
curl -s http://127.0.0.1:8000/ > nul
if errorlevel 1 (
    echo ERROR: Your MCP server is not running!
    echo Start it with: python mcp_server.py
    pause
    exit /b 1
)

echo Starting mcp-remote proxy...
echo This window must stay open while using Continue.
echo ========================================

REM Find npx path and run it
where npx > nul 2>&1
if errorlevel 1 (
    echo ERROR: npx not found! Install Node.js from https://nodejs.org
    pause
    exit /b 1
)

REM Start mcp-remote with full logging
npx -y mcp-remote@latest http://127.0.0.1:8000/mcp --transport sse-only --verbose

pause