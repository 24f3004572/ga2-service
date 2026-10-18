import time, uuid
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

EMAIL = "24f3004572@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-6gsnud.example.com"

app = FastAPI()

@app.middleware("http")
async def mw(request: Request, call_next):
    t0 = time.perf_counter()
    origin = request.headers.get("origin")

    if request.method == "OPTIONS":
        resp = Response(status_code=204)
    else:
        resp = await call_next(request)

    # CORS: only the assigned origin gets ACAO. Never "*".
    if origin == ALLOWED_ORIGIN:
        resp.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
        resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = (
            request.headers.get("access-control-request-headers") or "*"
        )
        resp.headers["Access-Control-Expose-Headers"] = "X-Request-ID, X-Process-Time"
        resp.headers["Vary"] = "Origin"

    resp.headers["X-Request-ID"] = str(uuid.uuid4())
    resp.headers["X-Process-Time"] = f"{time.perf_counter() - t0:.6f}"
    return resp

@app.get("/stats")
def stats(values: str = ""):
    try:
        nums = [int(x) for x in values.split(",") if x.strip()]
    except ValueError:
        return JSONResponse({"error": "values must be comma-separated integers"}, status_code=422)
    if not nums:
        return JSONResponse({"error": "no values"}, status_code=422)
    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }
