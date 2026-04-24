"""Represents the current state of the simulated wireless network."""
import random

class WirelessNetwork:

    def __init__(
        self,
        num_nodes=10,
        base_throughput=100.0,
        packet_success_rate=1.0,
        channel_utilization=0.0,
        connection_success_rate=1.0,
        offered_load=0.65,
        noise_std=0.01,
    ):
        self.num_nodes = num_nodes # how many devices/nodes that are on the network
        self.base_throughput = base_throughput # maximum packets network can send per tick and be healthy
        self.offered_load = self._clamp(offered_load)
        self.noise_std = noise_std

        # store the original values so reset can restore them
        self.initial_packet_success_rate = self._clamp(packet_success_rate)
        self.initial_channel_utilization = self._clamp(channel_utilization) # needs to be between 0.0 and 1.0
        self.initial_connection_success_rate = self._clamp(connection_success_rate)

        # "live" values that attacks will degrade during simulation 
        self.packet_success_rate = self.initial_packet_success_rate
        self.channel_utilization = self.initial_channel_utilization
        self.connection_success_rate = self.initial_connection_success_rate

        self.metrics = self._empty_metrics() #scoreboard, track how things have changed every tick

    #fresh scoreboard for every metric being tracked 
    def _empty_metrics(self):
        return {
            "ticks": [],
            "throughput": [],
            "packet_success_rate": [],
            "channel_utilization": [],
            "connection_success_rate": [],
            "dropped_packets": [],
        }

    def _clamp(self, value, minimum=0.0, maximum=1.0):
        return max(minimum, min(maximum, value))

    def reset(self):
        self.metrics = self._empty_metrics()
        self.packet_success_rate = self.initial_packet_success_rate
        self.channel_utilization = self.initial_channel_utilization
        self.connection_success_rate = self.initial_connection_success_rate

    def set_packet_success_rate(self, value):
        self.packet_success_rate = self._clamp(value)

    def set_channel_utilization(self, value):
        self.channel_utilization = self._clamp(value)

    def set_connection_success_rate(self, value):
        self.connection_success_rate = self._clamp(value)

    def _contention_factor(self):
        # More nodes create more collisions and retransmissions on a shared medium.
        return min(0.5, max(0.0, (self.num_nodes - 1) * 0.02))

    def calculate_metrics(self):
        offered_traffic = self.base_throughput * self.offered_load
        effective_success = max(0.0, self.packet_success_rate * (1.0 - self._contention_factor()))
        throughput = offered_traffic * effective_success
        dropped_packets = max(0.0, offered_traffic - throughput)
        return {
            "throughput": throughput,
            "packet_success_rate": self.packet_success_rate,
            "channel_utilization": self.channel_utilization,
            "connection_success_rate": self.connection_success_rate,
            "dropped_packets": dropped_packets,
        }

    def record_metrics(self, tick):
        current_metrics = self.calculate_metrics()
        self.metrics["ticks"].append(tick)
        for metric_name, metric_value in current_metrics.items():
            self.metrics[metric_name].append(metric_value)

    def apply_noise(self, rng: random.Random):
        if self.noise_std <= 0.0:
            return
        self.set_packet_success_rate(self.packet_success_rate + rng.gauss(0, self.noise_std))
        self.set_channel_utilization(self.channel_utilization + rng.gauss(0, self.noise_std))
        self.set_connection_success_rate(self.connection_success_rate + rng.gauss(0, self.noise_std))

    def get_metrics(self):
        return self.metrics
