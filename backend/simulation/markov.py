"""Markov chain state modeling for the wireless network simulation.

Models the network as moving through four states:
  NORMAL     — healthy, packets flowing normally
  DEGRADED   — under attack, performance declining
  FAILED     — severely impaired, most traffic blocked
  RECOVERING — countermeasure active, metrics improving

At each tick, transition probabilities are computed from the current network
health score (packet_success_rate * (1 - channel_utilization)).
A high health score makes recovery/normal transitions more likely;
a low health score drives the chain toward FAILED.

A fixed random seed makes results reproducible across identical simulation runs.
"""

import random

STATES = ["NORMAL", "DEGRADED", "FAILED", "RECOVERING"]


def _get_transition_probs(current_state: str, health: float) -> list[float]:
    """Return transition probability vector [P(NORMAL), P(DEGRADED), P(FAILED), P(RECOVERING)].

    health is relative to the tick-0 baseline (1.0 = as healthy as the simulation started,
    0.0 = fully collapsed), so thresholds stay meaningful regardless of node count.
    """
    if current_state == "NORMAL":
        if health >= 0.80:
            return [0.99, 0.01, 0.00, 0.00]  # near-perfect — stay normal
        elif health >= 0.55:
            return [0.93, 0.07, 0.00, 0.00]
        elif health >= 0.25:
            return [0.20, 0.70, 0.10, 0.00]
        else:
            return [0.00, 0.25, 0.75, 0.00]

    elif current_state == "DEGRADED":
        if health >= 0.80:
            return [0.92, 0.08, 0.00, 0.00]  # healthy again — snap back quickly
        elif health >= 0.55:
            return [0.30, 0.55, 0.00, 0.15]
        elif health >= 0.25:
            return [0.00, 0.65, 0.35, 0.00]
        else:
            return [0.00, 0.15, 0.85, 0.00]

    elif current_state == "FAILED":
        if health >= 0.45:
            return [0.00, 0.15, 0.30, 0.55]
        elif health >= 0.15:
            return [0.00, 0.05, 0.65, 0.30]
        else:
            return [0.00, 0.00, 0.95, 0.05]

    else:  # RECOVERING
        if health >= 0.80:
            return [0.95, 0.05, 0.00, 0.00]  # fully recovered — exit to NORMAL
        elif health >= 0.55:
            return [0.65, 0.20, 0.00, 0.15]
        elif health >= 0.25:
            return [0.05, 0.25, 0.05, 0.65]
        else:
            return [0.00, 0.10, 0.45, 0.45]


def compute_state_sequence(metrics: dict) -> list[str]:
    """Derive the Markov state sequence from a completed simulation's metrics."""
    rng = random.Random(42)
    psr_list = metrics["packet_success_rate"]
    cu_list = metrics["channel_utilization"]

    # Anchor health to tick 0 so the chain measures degradation from the actual
    # starting conditions rather than an absolute value. This keeps thresholds
    # meaningful regardless of node count or initial channel utilization.
    baseline_health = max(0.01, psr_list[0] * (1.0 - cu_list[0]))

    current_state = "NORMAL"
    states: list[str] = []

    for psr, cu in zip(psr_list, cu_list):
        health = min(1.0, (psr * (1.0 - cu)) / baseline_health)
        probs = _get_transition_probs(current_state, health)
        current_state = rng.choices(STATES, weights=probs, k=1)[0]
        states.append(current_state)

    return states
