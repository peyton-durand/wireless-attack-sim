# This is the main entry point for the FastAPI backend.
# It sets up the FastAPI application, configures CORS to allow requests from
# the frontend, and defines a simple health check endpoint.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from simulation.engine import Simulation
from simulation.network import WirelessNetwork

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


class SimulationConfig(BaseModel):
    num_nodes: int = Field(default=10, ge=1)
    base_throughput: float = Field(default=100.0, ge=0.0)
    packet_success_rate: float = Field(default=1.0, ge=0.0, le=1.0)
    channel_utilization: float = Field(default=0.0, ge=0.0, le=1.0)
    num_ticks: int = Field(default=100, ge=1)
    countermeasure_start_tick: int = Field(default=50, ge=0)


@app.post("/simulate")
def simulate(config: SimulationConfig):
    network = WirelessNetwork(
        num_nodes=config.num_nodes,
        base_throughput=config.base_throughput,
        packet_success_rate=config.packet_success_rate,
        channel_utilization=config.channel_utilization,
    )
    simulation = Simulation(
        network=network,
        num_ticks=config.num_ticks,
        countermeasure_start_tick=config.countermeasure_start_tick,
    )

    return {
        "config": config.model_dump(),
        "metrics": simulation.run(),
    }
