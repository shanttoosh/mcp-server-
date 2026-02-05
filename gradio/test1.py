# Save as test_tool.py and run: python test_tool.py
import requests
import json

response = requests.post(
    "http://127.0.0.1:8000/mcp",
    json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "sentiment_analysis",
            "arguments": {
                "text": "The service was excellent and very helpful!"
            }
        }
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")