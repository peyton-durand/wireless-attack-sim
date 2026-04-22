from .network import WirelessNetwork
from typing import Callable, Optional

#runs a time-stepped simulation on the wireless network
class Simulation:
    def __init__(self, 
                 network: WirelessNetwork, 
                 num_ticks: int = 100, 
                 attack_fn: Optional[Callable[[WirelessNetwork, int], None]] = None,
                 countermeasure_fn: Optional[Callable[[WirelessNetwork, int], None]] = None,
                 countermeasure_start_tick: int = 50):
        self.network = network
        self.num_ticks = num_ticks
        self.attack_fn = attack_fn
        self.countermeasure_fn = countermeasure_fn
        self.countermeasure_start_tick = countermeasure_start_tick

    def run(self):
        self.network.reset()
        for tick in range(self.num_ticks):
            # Apply attack if provided
            if self.attack_fn: # call attack, it reaches the network and makes things worse
                self.attack_fn(self.network, tick)
            # Apply countermeasure only after the specified start tick
            if self.countermeasure_fn and tick >= self.countermeasure_start_tick:
                self.countermeasure_fn(self.network, tick)
            # Simulate normal operation
            throughput = self.network.base_throughput * self.network.packet_success_rate
            dropped_packets = self.network.base_throughput - throughput
            # Optionally update channel utilization here if needed
            self.network.record_metrics(throughput, dropped_packets)
        return self.network.get_metrics()