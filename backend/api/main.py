# This is the main entry point for the FastAPI backend.
# It sets up the FastAPI application, configures CORS to allow requests from
# the frontend, and defines a simple health check endpoint.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Wireless Attack Simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}