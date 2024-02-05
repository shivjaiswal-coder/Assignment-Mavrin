import threading
import os
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import router as router_v1

# creating a simple fast api app
app = FastAPI()

# including router file
app.include_router(router_v1.router, prefix="")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")