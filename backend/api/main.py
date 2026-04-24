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

COMPARE_ATTACKS = ["jamming", "rach_flood", "carrier_sense"]

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

class BaseSimulationConfig(BaseModel):
    num_nodes: int = Field(default=10, ge=1)
    base_throughput: float = Field(default=300.0, ge=0.0)
    packet_success_rate: float = Field(default=0.98, ge=0.0, le=1.0)
    channel_utilization: float = Field(default=0.15, ge=0.0, le=1.0)
    connection_success_rate: float = Field(default=0.99, ge=0.0, le=1.0)
    offered_load: float = Field(default=0.65, ge=0.0, le=1.0)
    noise_std: float = Field(default=0.01, ge=0.0, le=0.5)
    num_ticks: int = Field(default=100, ge=1)
    countermeasure_start_tick: int = Field(default=50, ge=0)


class SimulationConfig(BaseSimulationConfig):
    attack_type: Literal["none", "jamming", "rach_flood", "carrier_sense"] = "none"


class CompareAllConfig(BaseSimulationConfig):
    pass

ATTACK_MAP = {
    "none": (None, None),
    "jamming": (jamming_attack, frequency_hopping_countermeasure),
    "rach_flood": (rach_flood_attack, rate_limiting_countermeasure),
    "carrier_sense": (carrier_sense_attack, nav_anomaly_countermeasure),
}


def _run_simulation(config: BaseSimulationConfig, attack_type: str):
    attack_fn, countermeasure_fn = ATTACK_MAP[attack_type]

    network = WirelessNetwork(
        num_nodes=config.num_nodes,
        base_throughput=config.base_throughput,
        packet_success_rate=config.packet_success_rate,
        connection_success_rate=config.connection_success_rate,
        offered_load=config.offered_load,
        noise_std=config.noise_std,
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
    return metrics

# The main simulation endpoint, this is what the frontend's Run button calls.
# It receives a config, builds the network and simulation engine, runs it,
# and returns the full time-series metrics as JSON for the frontend to graph.
# Attack and countermeasure functions will be wired in here in later phases
# for now it runs a clean baseline simulation with no attack.

@app.post("/simulate")
def simulate(config: SimulationConfig):
    return {
        "config": config.model_dump(),
        "metrics": _run_simulation(config, config.attack_type),
    }


@app.post("/simulate/compare-all")
def compare_all(config: CompareAllConfig):
    results = {
        attack_type: {
            "metrics": _run_simulation(config, attack_type),
        }
        for attack_type in COMPARE_ATTACKS
    }

    return {
        "config": config.model_dump(),
        "results": results,
    }
