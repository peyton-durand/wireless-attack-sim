"""
Jamming attack: jammer broadcasts noise on the same frequency, increasing
packet failure rate over time. Countermeasure: frequency hopping (FHSS)
switches channels, gradually restoring packet success rate.
"""

from simulation.network import WirelessNetwork

JAMMER_INTENSITY = 0.04   # how much packet success rate drops per tick (5 GHz jamming is effective on-channel)
RECOVERY_RATE = 0.06      # how fast frequency hopping recovers per tick (802.11ac has 25 non-overlapping 5 GHz channels)


def jamming_attack(network: WirelessNetwork, tick: int) -> None:
    new_rate = network.packet_success_rate - JAMMER_INTENSITY
    network.set_packet_success_rate(new_rate)

    # channel fills up as jammer occupies it
    new_utilization = network.channel_utilization + JAMMER_INTENSITY
    network.set_channel_utilization(new_utilization)


def frequency_hopping_countermeasure(network: WirelessNetwork, tick: int) -> None:
    new_rate = network.packet_success_rate + RECOVERY_RATE
    network.set_packet_success_rate(new_rate)

    new_utilization = network.channel_utilization - RECOVERY_RATE
    network.set_channel_utilization(new_utilization)