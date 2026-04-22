"""Represents the current state of the simulated wireless network."""

class WirelessNetwork:

    def __init__(
        self,
        num_nodes=10,
        base_throughput=100.0,
        packet_success_rate=1.0,
        channel_utilization=0.0,
    ):
        self.num_nodes = num_nodes # how many devices/nodes that are on the network
        self.base_throughput = base_throughput # maximum packets network can send per tick and be healthy

        # store the original values so reset can restore them
        self.initial_packet_success_rate = self._clamp(packet_success_rate)
        self.initial_channel_utilization = self._clamp(channel_utilization) # needs to be between 0.0 and 1.0

        # "live" values that attacks will degrade during simulation 
        self.packet_success_rate = self.initial_packet_success_rate
        self.channel_utilization = self.initial_channel_utilization

        self.metrics = self._empty_metrics() #scoreboard, track how things have changed every tick

    #fresh scoreboard for every metric being tracked 
    def _empty_metrics(self):
        return {
            "ticks": [],
            "throughput": [],
            "packet_success_rate": [],
            "channel_utilization": [],
            "dropped_packets": [],
        }

    def _clamp(self, value, minimum=0.0, maximum=1.0):
        return max(minimum, min(maximum, value))

    def reset(self):
        self.metrics = self._empty_metrics()
        self.packet_success_rate = self.initial_packet_success_rate
        self.channel_utilization = self.initial_channel_utilization

    def set_packet_success_rate(self, value):
        self.packet_success_rate = self._clamp(value)

    def set_channel_utilization(self, value):
        self.channel_utilization = self._clamp(value)

    def calculate_metrics(self):
        throughput = self.base_throughput * self.packet_success_rate
        dropped_packets = max(0.0, self.base_throughput - throughput)
        return {
            "throughput": throughput,
            "packet_success_rate": self.packet_success_rate,
            "channel_utilization": self.channel_utilization,
            "dropped_packets": dropped_packets,
        }

    def record_metrics(self, tick):
        current_metrics = self.calculate_metrics()
        self.metrics["ticks"].append(tick)
        for metric_name, metric_value in current_metrics.items():
            self.metrics[metric_name].append(metric_value)

    def get_metrics(self):
        return self.metrics
