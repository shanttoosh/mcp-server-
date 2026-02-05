# test_protocol.py
import requests
import json
import sys

print("🧪 Testing MCP Server Protocol Handshake...")
print("="*50)

# 1. Test SSE initialization (what mcp-remote expects first)
print("1. Testing SSE endpoint...")
try:
    response = requests.get("http://127.0.0.1:8000/mcp", 
                          headers={"Accept": "text/event-stream"}, 
                          stream=True, 
                          timeout=2)
    
    # Read the first event
    for line in response.iter_lines():
        if line:
            decoded = line.decode('utf-8')
            if decoded.startswith('data:'):
                data = json.loads(decoded[5:].strip())
                print(f"✅ First SSE event received:")
                print(f"   Protocol: {data.get('result', {}).get('protocolVersion', 'NOT FOUND')}")
                print(f"   Server: {data.get('result', {}).get('serverInfo', {})}")
                break
except Exception as e:
    print(f"❌ SSE test failed: {e}")

print("\n" + "="*50)

# 2. Test JSON-RPC initialization directly
print("2. Testing direct JSON-RPC initialization...")
init_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",  # Try this version
        "capabilities": {},
        "clientInfo": {
            "name": "Test Client",
            "version": "1.0.0"
        }
    }
}

try:
    response = requests.post("http://127.0.0.1:8000/mcp", 
                           json=init_request,
                           timeout=5)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Initialization response: {json.dumps(result, indent=2)}")
    else:
        print(f"❌ Initialization failed: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ Request failed: {e}")

print("="*50)