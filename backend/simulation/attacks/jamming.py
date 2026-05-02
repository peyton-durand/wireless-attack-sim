"""
Jamming attack: jammer broadcasts noise on the same frequency, raising
interference and dropping the link SINR. Packet success rate is derived from
a sigmoid of SINR rather than a flat delta — this produces the S-curve seen
in real 802.11 link-quality vs. interference measurements: small SINR drops
hurt little, but once SINR crosses the demodulation threshold the link
collapses rapidly. Countermeasure: FHSS hops to a clean channel, bleeding
the accumulated interference back down faster than the jammer can rebuild it.
"""

import math
from simulation.network import WirelessNetwork

# --- physical link constants ---
SINR_CLEAN_dB     = 25.0   # healthy link SINR before any jamming (dB) — typical 802.11ac at ~10 m
SINR_THRESHOLD_dB = 10.0   # inflection point: PSR = 50% at this SINR (802.11ac BPSK 1/2 sensitivity)
SINR_STEEPNESS    = 0.27   # sigmoid slope — calibrated so PSR ≈ 98% at 25 dB, ≈ 21% at 5 dB

# --- jammer buildup ---
JAMMER_RAMP_dB_PER_TICK = 1.0   # interference grows 1 dB/tick as jammer locks on
JAMMER_MAX_dB           = 25.0  # ceiling: fully on-channel jammer saturates the receiver

# --- FHSS countermeasure ---
# FHSS bleeds interference 1.5 dB/tick; attack still adds 1.0 dB/tick while active,
# so the net is -0.5 dB/tick — full recovery in ~40 ticks, matching the linear model's pace.
FHSS_RELIEF_dB_PER_TICK = 1.5

# --- channel utilization (jammer occupies spectrum regardless of SINR) ---
CU_RAMP_PER_TICK        = 0.04
FHSS_CU_RELIEF_PER_TICK = 0.06


def _sinr_to_psr(sinr_db: float) -> float:
    """Sigmoid mapping from SINR (dB) to packet success rate.

    Models the BER-vs-SNR curve of 802.11ac OFDM: near-perfect delivery at
    high SINR, catastrophic failure below the demodulation threshold.
    """
    return 1.0 / (1.0 + math.exp(-SINR_STEEPNESS * (sinr_db - SINR_THRESHOLD_dB)))


def jamming_attack(network: WirelessNetwork, tick: int) -> None:
    # Jammer ramps up interference each tick until it saturates the channel.
    network.jammer_interference_dB = min(
        JAMMER_MAX_dB,
        network.jammer_interference_dB + JAMMER_RAMP_dB_PER_TICK,
    )

    sinr_db = SINR_CLEAN_dB - network.jammer_interference_dB
    network.set_packet_success_rate(_sinr_to_psr(sinr_db))

    network.set_channel_utilization(network.channel_utilization + CU_RAMP_PER_TICK)


def frequency_hopping_countermeasure(network: WirelessNetwork, tick: int) -> None:
    # FHSS hops to a clean channel faster than the jammer can pursue —
    # net effect is interference drains while the attack is still running.
    network.jammer_interference_dB = max(
        0.0,
        network.jammer_interference_dB - FHSS_RELIEF_dB_PER_TICK,
    )

    sinr_db = SINR_CLEAN_dB - network.jammer_interference_dB
    network.set_packet_success_rate(_sinr_to_psr(sinr_db))

    network.set_channel_utilization(network.channel_utilization - FHSS_CU_RELIEF_PER_TICK)
