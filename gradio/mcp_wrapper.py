# mcp_wrapper.py - Python wrapper that ensures proxy is ready
import subprocess
import time
import sys
import signal
import os

def signal_handler(sig, frame):
    print("\nShutting down MCP proxy...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("🚀 Starting MCP proxy wrapper...")
print(f"Connecting to: http://127.0.0.1:8000/mcp")
print("-" * 50)

# Start mcp-remote
proc = subprocess.Popen(
    [
        "npx", "-y", "mcp-remote@latest",
        "http://127.0.0.1:8000/mcp",
        "--transport", "sse-only"
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    universal_newlines=True
)

# Wait for "Proxy established successfully" message
print("Waiting for proxy to be ready...")
ready = False
for line in iter(proc.stdout.readline, ''):
    print(line.strip())
    if "Proxy established successfully" in line:
        print("✅ Proxy is ready!")
        ready = True
        break
    elif "error" in line.lower() or "failed" in line.lower():
        print("❌ Proxy failed to start")
        proc.terminate()
        sys.exit(1)

# If we got here, proxy is ready
if ready:
    print("\n🎯 MCP Proxy is running and ready for Continue")
    print("   Keep this window open while using Continue")
    print("-" * 50)
    
    # Keep the process alive
    try:
        for line in iter(proc.stdout.readline, ''):
            print(line.strip())
    except KeyboardInterrupt:
        print("\nShutting down...")
        proc.terminate()

proc.wait()