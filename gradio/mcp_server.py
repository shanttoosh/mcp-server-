# mcp_server.py - SIMPLE WORKING MCP SERVER
import json
from textblob import TextBlob
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from sse_starlette.sse import EventSourceResponse
import uvicorn
import asyncio
from fastapi import Header

app = FastAPI(title="Sentiment Analysis MCP Server")

def analyze_sentiment(text: str) -> dict:
    """Analyze text sentiment."""
    blob = TextBlob(text)
    sentiment = blob.sentiment
    
    return {
        "polarity": round(sentiment.polarity, 2),
        "subjectivity": round(sentiment.subjectivity, 2),
        "assessment": "positive" if sentiment.polarity > 0 else "negative" if sentiment.polarity < 0 else "neutral"
    }

# MCP SSE endpoint
@app.get("/mcp")
async def mcp_sse(accept: str = Header(None)):
    if "text/event-stream" not in (accept or ""):
        return JSONResponse(
            status_code=406,
            content={"error": "Client must accept text/event-stream"}
        )
    async def event_generator():
        # Send initialization
        while True:
            await asyncio.sleep(30)
            yield {"event": "ping", "data": ""}
    
    return EventSourceResponse(event_generator())

# JSON-RPC endpoint
# IN YOUR mcp_server.py, update the handle_mcp function:
# In mcp_server.py, replace the entire handle_mcp function with this:

@app.post("/mcp")
async def handle_mcp(request: Request):
    data = await request.json()
    method = data.get("method")
    request_id = data.get("id")
    params = data.get("params", {})
    
    print(f"📨 Received {method} request (ID: {request_id})")
    
    if method == "initialize":
        # MCP INITIALIZATION HANDLER - CRITICAL!
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "logging": {},
                    "experimental": {}
                },
                "serverInfo": {
                    "name": "sentiment-analysis",
                    "version": "1.0.0"
                }
            }
        })
    
    elif method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "sentiment_analysis",
                        "description": "Analyze the sentiment of text",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string", "description": "The text to analyze"}
                            },
                            "required": ["text"]
                        }
                    }
                ]
            }
        })
    
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "sentiment_analysis":
            text = arguments.get("text", "")
            result = analyze_sentiment(text)
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }
                    ]
                }
            })
    
    return JSONResponse({
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"}
    })
# Test endpoint
@app.get("/analyze")
async def analyze_text(text: str = "I love this!"):
    return analyze_sentiment(text)

@app.get("/")
async def root():
    return {
        "name": "Sentiment Analysis MCP Server",
        "endpoints": {
            "mcp_sse": "GET /mcp",
            "mcp_jsonrpc": "POST /mcp",
            "analyze": "GET /analyze?text=Your+text"
        }
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 SENTIMENT ANALYSIS MCP SERVER")
    print("=" * 60)
    print("📡 Server: http://127.0.0.1:8000")
    print("🔧 MCP Endpoint: http://127.0.0.1:8000/mcp")
    print("📊 Test: http://127.0.0.1:8000/analyze?text=I+love+this")
    print("=" * 60)
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")