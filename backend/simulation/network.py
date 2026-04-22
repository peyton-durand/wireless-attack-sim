class WirelessNetwork:
  #represents a wireless network with basic parameters and metrics tracking

    def __init__(self, num_nodes=10, base_throughput=100.0, packet_success_rate=1.0, channel_utilization=0.0):
        self.num_nodes = num_nodes  # Number of devices/nodes in the network
        self.base_throughput = base_throughput  # Packets per tick it can send everything healthy
        self.packet_success_rate = packet_success_rate  # what fraction of packets are successfully delivered
        self.channel_utilization = channel_utilization  # how busy the channel is
        self.metrics = {
            'throughput': [],
            'packet_success_rate': [],
            'channel_utilization': [],
            'dropped_packets': [],
        }

    #resets the network to initial conditions and clears metrics
    def reset(self):
        for key in self.metrics:
            self.metrics[key] = []
        self.packet_success_rate = 1.0
        self.channel_utilization = 0.0

    #records the metrics for the current tick
    def record_metrics(self, throughput, dropped_packets):
        self.metrics['throughput'].append(throughput)
        self.metrics['packet_success_rate'].append(self.packet_success_rate)
        self.metrics['channel_utilization'].append(self.channel_utilization)
        self.metrics['dropped_packets'].append(dropped_packets)

    #return all metrics
    def get_metrics(self):
        return self.metrics