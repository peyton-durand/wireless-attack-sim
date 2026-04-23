"""Carrier sense exploit attack and NAV anomaly countermeasure.

In 802.11 CSMA/CA, devices check if the channel is idle before transmitting.
The NAV (Network Allocation Vector) is a virtual carrier sense timer: RTS/CTS frames
announce how long a transmission will take, so all nearby devices defer for that duration.

The attacker floods fake RTS frames with exaggerated NAV durations, causing every
legitimate device to hold off indefinitely. Channel utilization climbs to near 100%
while real throughput collapses.

Countermeasure: anomalous NAV detection — devices track NAV durations and ignore
reservations that exceed a plausible maximum (timeout threshold). This lets
legitimate devices reclaim channel access.
"""

CS_NAV_PRESSURE = 0.05        # channel utilization increase per tick (fake RTS frames)
CS_PACKET_PRESSURE = 0.03     # packet success rate drop per tick base
CS_CHANNEL_CEILING = 0.97     # attacker saturates channel but can't quite hit 100%

CS_NAV_RELIEF = 0.07          # channel utilization cleared per tick after detection
CS_PACKET_RECOVERY = 0.05     # packet success rate recovered per tick
CS_HEALTHY_CHANNEL_BASELINE = 0.05  # resting channel utilization after recovery


def carrier_sense_attack(network, tick: int) -> None:
    congestion_factor = 1.0 + network.channel_utilization
    new_cu = min(network.channel_utilization + CS_NAV_PRESSURE, CS_CHANNEL_CEILING)
    new_psr = max(network.packet_success_rate - CS_PACKET_PRESSURE * congestion_factor, 0.0)
    network.set_channel_utilization(new_cu)
    network.set_packet_success_rate(new_psr)


def nav_anomaly_countermeasure(network, tick: int) -> None:
    new_cu = max(network.channel_utilization - CS_NAV_RELIEF, CS_HEALTHY_CHANNEL_BASELINE)
    new_psr = min(network.packet_success_rate + CS_PACKET_RECOVERY, 1.0)
    network.set_channel_utilization(new_cu)
    network.set_packet_success_rate(new_psr)
