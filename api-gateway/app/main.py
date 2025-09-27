from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI(title="API Gateway")

services = {
    "auth": "http://auth-service:8000",
    "accounts": "http://account-service:8000",
    "transactions": "http://transaction-service:8000",
    "risk": "http://risk-service:8000",
}

client = httpx.AsyncClient()

@app.api_route("/{service}/{path:path}")
async def reverse_proxy(request: Request, service: str, path: str):
    """
    A simple reverse proxy that forwards requests to the appropriate service.
    """
    base_url = services.get(service)
    if not base_url:
        return Response(content="Service not found", status_code=404)

    url = f"{base_url}/{path}"

    # Recreate the request to the downstream service
    request_body = await request.body()
    headers = dict(request.headers)
    # Host header needs to be updated for the downstream service
    headers["host"] = base_url.split("://")[1].split(":")[0]

    r = await client.request(
        method=request.method,
        url=url,
        headers=headers,
        params=request.query_params,
        content=request_body,
    )

    # Copy the response from the downstream service to the client
    return Response(content=r.content, status_code=r.status_code, headers=dict(r.headers))

@app.get("/health")
async def health_check():
    return {"status": "ok", "gateway": True}