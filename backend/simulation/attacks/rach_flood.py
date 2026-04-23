"""
RACH flooding attack: spoofed devices overwhelm the base station with fake
access requests, making it harder for legitimate users to connect.
Countermeasure: rate limiting and backoff gradually restore connection success.
"""

from simulation.network import WirelessNetwork

RACH_FLOOD_INTENSITY = 0.04
RACH_CHANNEL_PRESSURE = 0.02
RACH_PACKET_PRESSURE = 0.01
RACH_RECOVERY_RATE = 0.08
RACH_CHANNEL_RELIEF = 0.04
RACH_PACKET_RECOVERY = 0.03
RACH_MIN_CONNECTION_SUCCESS = 0.25
RACH_HEALTHY_CHANNEL_BASELINE = 0.20


def rach_flood_attack(network: WirelessNetwork, tick: int) -> None:
    new_connection_rate = max(
        RACH_MIN_CONNECTION_SUCCESS,
        network.connection_success_rate - RACH_FLOOD_INTENSITY,
    )
    network.set_connection_success_rate(new_connection_rate)

    new_channel_utilization = network.channel_utilization + RACH_CHANNEL_PRESSURE
    network.set_channel_utilization(new_channel_utilization)

    new_packet_success_rate = network.packet_success_rate - RACH_PACKET_PRESSURE
    network.set_packet_success_rate(new_packet_success_rate)


def rate_limiting_countermeasure(network: WirelessNetwork, tick: int) -> None:
    new_connection_rate = network.connection_success_rate + RACH_RECOVERY_RATE
    network.set_connection_success_rate(new_connection_rate)

    new_channel_utilization = max(
        RACH_HEALTHY_CHANNEL_BASELINE,
        network.channel_utilization - RACH_CHANNEL_RELIEF,
    )
    network.set_channel_utilization(new_channel_utilization)

    new_packet_success_rate = network.packet_success_rate + RACH_PACKET_RECOVERY
    network.set_packet_success_rate(new_packet_success_rate)
