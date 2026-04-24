import random
from typing import Callable, Optional

from .network import WirelessNetwork

"""Runs a time-stepped simulation over a wireless network model."""

class Simulation:

    def __init__(
        self,
        network: WirelessNetwork,
        num_ticks: int = 100,
        attack_fn: Optional[Callable[[WirelessNetwork, int], None]] = None,
        countermeasure_fn: Optional[Callable[[WirelessNetwork, int], None]] = None,
        countermeasure_start_tick: int = 50,
        seed: int = 42,
    ):
        self.network = network
        self.num_ticks = num_ticks
        self.attack_fn = attack_fn
        self.countermeasure_fn = countermeasure_fn
        self.countermeasure_start_tick = countermeasure_start_tick
        self._rng = random.Random(seed)

    def _apply_attack(self, tick: int):
        if self.attack_fn is not None:
            self.attack_fn(self.network, tick)

    def _apply_countermeasure(self, tick: int):
        if self.countermeasure_fn is not None and tick >= self.countermeasure_start_tick:
            self.countermeasure_fn(self.network, tick)

    def _run_tick(self, tick: int):
        self._apply_attack(tick)
        self._apply_countermeasure(tick)
        self.network.apply_noise(self._rng)
        self.network.record_metrics(tick)

    def run(self):
        self.network.reset()
        for tick in range(self.num_ticks):
            self._run_tick(tick)
        return self.network.get_metrics()
