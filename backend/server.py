"""
TeleCareZone - Python to PHP Bridge Server
This server acts as a proxy to forward requests from the Python/FastAPI ecosystem
to the Core PHP backend running on port 8002.
"""
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="TeleCareZone API Bridge")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PHP Backend URL
PHP_BACKEND_URL = "http://localhost:8002"

@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_to_php(path: str, request: Request):
    """
    Forward all /api/* requests to the PHP backend
    """
    try:
        # Get the request body
        body = await request.body()
        
        # Prepare headers (exclude host header)
        headers = dict(request.headers)
        headers.pop('host', None)
        
        # Make request to PHP backend
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=request.method,
                url=f"{PHP_BACKEND_URL}/api/{path}",
                content=body,
                headers=headers,
                params=request.query_params
            )
        
        # Return the PHP response
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    
    except httpx.ConnectError:
        return Response(
            content='{"error": "PHP backend is not running"}',
            status_code=503,
            media_type="application/json"
        )
    except Exception as e:
        return Response(
            content=f'{{"error": "Bridge error: {str(e)}"}}',
            status_code=500,
            media_type="application/json"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{PHP_BACKEND_URL}/api")
            php_status = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        php_status = "unreachable"
    
    return {
        "status": "running",
        "bridge": "operational",
        "php_backend": php_status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
