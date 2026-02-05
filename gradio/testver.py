# verify_mcp.py
import requests
import json

def verify_server():
    base_url = "http://127.0.0.1:7860"
    
    print("🔍 Verifying MCP Server Setup")
    print("=" * 50)
    
    # 1. Check if server is running
    try:
        response = requests.get(base_url, timeout=5)
        print(f"✅ Server is running at {base_url}")
    except:
        print(f"❌ Server not running at {base_url}")
        return
    
    # 2. Check Gradio API
    try:
        response = requests.get(f"{base_url}/config", timeout=5)
        if response.status_code == 200:
            print("✅ Gradio API is accessible")
        else:
            print(f"❌ Gradio API error: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot access Gradio API: {e}")
    
    # 3. Check MCP endpoint
    try:
        response = requests.get(
            f"{base_url}/gradio_api/mcp",
            headers={"Accept": "text/event-stream"},
            timeout=3
        )
        print(f"✅ MCP endpoint responds (SSE): {response.status_code}")
    except requests.exceptions.Timeout:
        print("✅ MCP endpoint accepts SSE connections (timeout expected)")
    except Exception as e:
        print(f"❌ MCP endpoint error: {e}")
    
    # 4. Test sentiment analysis
    try:
        response = requests.post(
            f"{base_url}/api/predict/",
            json={"data": ["Test sentence for sentiment analysis."]},
            timeout=5
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Sentiment analysis works!")
            print(f"   Result: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Sentiment analysis failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot test sentiment analysis: {e}")
    
    print("=" * 50)
    print("📋 Summary:")
    print("- Your server needs to expose tools via MCP protocol")
    print("- Gradio's mcp_server=True should create /gradio_api/mcp endpoint")
    print("- Continue looks for tools via this SSE endpoint")

if __name__ == "__main__":
    verify_server()