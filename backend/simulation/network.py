"""Represents the current state of the simulated wireless network."""

class WirelessNetwork:

    def __init__(
        self,
        num_nodes=10,
        base_throughput=300.0,
        packet_success_rate=0.98,
        connection_success_rate=0.99,
        offered_load=0.65,
        noise_std=0.02,
    ):
        self.num_nodes = num_nodes # how many devices/nodes that are on the network
        self.base_throughput = base_throughput # maximum packets network can send per tick and be healthy
        self.offered_load = self._clamp(offered_load)
        self.noise_std = noise_std

        # store the original values so reset can restore them
        self.initial_packet_success_rate = self._clamp(packet_success_rate)
        # CU is derived from both node count and offered load: more devices and
        # more attempted traffic create a busier shared medium before attacks start.
        self.initial_channel_utilization = self._baseline_channel_utilization()
        self.initial_connection_success_rate = self._clamp(connection_success_rate)

        # "live" values that attacks will degrade during simulation
        self.packet_success_rate = self.initial_packet_success_rate
        self.channel_utilization = self.initial_channel_utilization
        self.connection_success_rate = self.initial_connection_success_rate

        # jammer interference accumulator used by jamming.py (dB above noise floor)
        self.jammer_interference_dB = 0.0

        self.metrics = self._empty_metrics() #scoreboard, track how things have changed every tick

    #fresh scoreboard for every metric being tracked 
    def _empty_metrics(self):
        return {
            "ticks": [],
            "throughput": [],
            "latency_ms": [],
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
        self.jammer_interference_dB = 0.0

    def set_packet_success_rate(self, value):
        self.packet_success_rate = self._clamp(value)

    def set_channel_utilization(self, value):
        self.channel_utilization = self._clamp(value)

    def set_connection_success_rate(self, value):
        self.connection_success_rate = self._clamp(value)

    def _node_channel_utilization(self):
        # Power curve fits the 802.11ac home network table:
        # 3 nodes: ~17%, 8 nodes: ~42%, 12 nodes: ~58%, 15 nodes: ~69%
        return min(0.85, 0.08 * self.num_nodes ** 0.7)

    def _baseline_channel_utilization(self):
        node_contention = self._node_channel_utilization()
        load_pressure = self.offered_load * 0.18
        return self._clamp(node_contention + load_pressure, maximum=0.95)

    def _contention_factor(self):
        # Collision overhead scales with node count; 0.002 per extra node gives
        # a visible drop-rate increase while staying modest at low node counts.
        return min(0.5, max(0.0, (self.num_nodes - 1) * 0.002))

    def _latency_ms(self, effective_success):
        # Latency rises as the shared medium gets busier and packet delivery becomes less reliable.
        base_latency = 12.0
        queue_delay = self.channel_utilization * 80.0
        retry_delay = (1.0 - effective_success) * 120.0
        load_delay = self.offered_load * 25.0
        return base_latency + queue_delay + retry_delay + load_delay

    def calculate_metrics(self):
        offered_traffic = self.base_throughput * self.offered_load
        effective_success = max(0.0, self.packet_success_rate * (1.0 - self._contention_factor()))
        throughput = offered_traffic * effective_success
        dropped_packets = max(0.0, offered_traffic - throughput)
        latency_ms = self._latency_ms(effective_success)
        return {
            "throughput": throughput,
            "latency_ms": latency_ms,
            "packet_success_rate": self.packet_success_rate,
            "channel_utilization": self.channel_utilization,
            "connection_success_rate": self.connection_success_rate,
            "dropped_packets": dropped_packets,
        }

    def record_metrics(self, tick, rng=None):
        current_metrics = self.calculate_metrics()
        if rng is not None and self.noise_std > 0.0:
            noisy_psr = self._clamp(current_metrics["packet_success_rate"] + rng.gauss(0, self.noise_std))
            noisy_cu  = self._clamp(current_metrics["channel_utilization"]  + rng.gauss(0, self.noise_std))
            noisy_csr = self._clamp(current_metrics["connection_success_rate"] + rng.gauss(0, self.noise_std))
            offered   = self.base_throughput * self.offered_load
            noisy_tp  = offered * max(0.0, noisy_psr * (1.0 - self._contention_factor()))
            noisy_latency = self._latency_ms(max(0.0, noisy_psr * (1.0 - self._contention_factor())))
            current_metrics.update({
                "packet_success_rate":    noisy_psr,
                "channel_utilization":    noisy_cu,
                "connection_success_rate": noisy_csr,
                "throughput":             noisy_tp,
                "latency_ms":            noisy_latency,
                "dropped_packets":        max(0.0, offered - noisy_tp),
            })
        self.metrics["ticks"].append(tick)
        for metric_name, metric_value in current_metrics.items():
            self.metrics[metric_name].append(metric_value)

    def get_metrics(self):
        return self.metrics
