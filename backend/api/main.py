# This is the main entry point for the FastAPI backend.
# It sets up the FastAPI application, configures CORS to allow requests from
# the frontend, and defines a simple health check endpoint.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal

from simulation.engine import Simulation
from simulation.network import WirelessNetwork
from simulation.attacks.jamming import jamming_attack, frequency_hopping_countermeasure
from simulation.attacks.rach_flood import (
    rach_flood_attack,
    rate_limiting_countermeasure,
)
from simulation.attacks.carrier_sense import carrier_sense_attack, nav_anomaly_countermeasure
from simulation.markov import compute_state_sequence

app = FastAPI(title="Wireless Attack Simulator")

RACH_BASELINE_CHANNEL_UTILIZATION = 0.20

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Defines what the frontend needs to send when requesting a simulation.
# FastAPI automatically validates all these values before they reach our code
# so if the frontend sends something invalid (like num_ticks: -1), it gets
# rejected with an error before the simulation even runs.

class SimulationConfig(BaseModel):
    attack_type: Literal["none", "jamming", "rach_flood", "carrier_sense"] = "none"
    num_nodes: int = Field(default=10, ge=1)
    base_throughput: float = Field(default=100.0, ge=0.0)
    packet_success_rate: float = Field(default=1.0, ge=0.0, le=1.0)
    channel_utilization: float = Field(default=0.0, ge=0.0, le=1.0)
    connection_success_rate: float = Field(default=1.0, ge=0.0, le=1.0)
    num_ticks: int = Field(default=100, ge=1)
    countermeasure_start_tick: int = Field(default=50, ge=0)

ATTACK_MAP = {
    "none": (None, None),
    "jamming": (jamming_attack, frequency_hopping_countermeasure),
    "rach_flood": (rach_flood_attack, rate_limiting_countermeasure),
    "carrier_sense": (carrier_sense_attack, nav_anomaly_countermeasure),
}

# The main simulation endpoint, this is what the frontend's Run button calls.
# It receives a config, builds the network and simulation engine, runs it,
# and returns the full time-series metrics as JSON for the frontend to graph.
# Attack and countermeasure functions will be wired in here in later phases
# for now it runs a clean baseline simulation with no attack.

@app.post("/simulate")
def simulate(config: SimulationConfig):
    attack_fn, countermeasure_fn = ATTACK_MAP[config.attack_type]
    channel_utilization = config.channel_utilization

    if config.attack_type == "rach_flood" and channel_utilization == 0.0:
        channel_utilization = RACH_BASELINE_CHANNEL_UTILIZATION

    network = WirelessNetwork(
        num_nodes=config.num_nodes,
        base_throughput=config.base_throughput,
        packet_success_rate=config.packet_success_rate,
        channel_utilization=channel_utilization,
        connection_success_rate=config.connection_success_rate,
    )
    simulation = Simulation(
        network=network,
        num_ticks=config.num_ticks,
        attack_fn=attack_fn,
        countermeasure_fn=countermeasure_fn,
        countermeasure_start_tick=config.countermeasure_start_tick,
    )

    metrics = simulation.run()
    metrics["state_sequence"] = compute_state_sequence(metrics)

    return {
        "config": config.model_dump(),
        "metrics": metrics,
    }
