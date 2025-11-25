"""
Counterfactual Regret Minimization (CFR) for Random Number Texas Hold'Em.

The implementation follows a coarse abstraction:
- Card space discretized into 20 equal buckets
- Information set defined by (card_bucket, position, pot_size_state)
- Actions: fold, call, raise (single raise size per node)

We use External Sampling Monte Carlo CFR which scales to large trees by
sampling a single opponent action trajectory per iteration.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


NUM_BUCKETS = 20
ACTION_LIST = ["fold", "call", "raise"]


def bucketize(card_value: float) -> int:
    bucket = min(int(card_value * NUM_BUCKETS), NUM_BUCKETS - 1)
    return bucket


@dataclass
class CFRNode:
    info_set: str
    regret_sum: List[float] = field(default_factory=lambda: [0.0] * len(ACTION_LIST))
    strategy_sum: List[float] = field(default_factory=lambda: [0.0] * len(ACTION_LIST))

    def get_strategy(self, realization_weight: float) -> List[float]:
        positive_regrets = [max(r, 0.0) for r in self.regret_sum]
        normalizing_sum = sum(positive_regrets)
        if normalizing_sum > 0:
            strategy = [r / normalizing_sum for r in positive_regrets]
        else:
            strategy = [1.0 / len(ACTION_LIST)] * len(ACTION_LIST)
        for i, prob in enumerate(strategy):
            self.strategy_sum[i] += realization_weight * prob
        return strategy

    def get_average_strategy(self) -> List[float]:
        normalizing_sum = sum(self.strategy_sum)
        if normalizing_sum > 0:
            return [s / normalizing_sum for s in self.strategy_sum]
        return [1.0 / len(ACTION_LIST)] * len(ACTION_LIST)


class CFRTrainer:
    def __init__(self, rng_seed: int | None = None):
        self.nodes: Dict[str, CFRNode] = {}
        self.rng = random.Random(rng_seed)

    def train(self, iterations: int = 1_000_000):
        util = 0.0
        for i in range(1, iterations + 1):
            card_my = self.rng.random()
            card_opp = self.rng.random()
            util += self.cfr(card_my, card_opp, "", 1.0, 1.0)
            if i % 10000 == 0:
                avg = util / i
                print(f"[CFR] iter={i:,} avg_util={avg:+.4f}")

    def cfr(
        self,
        my_card: float,
        opp_card: float,
        history: str,
        prob_my: float,
        prob_opp: float,
        pot: float = 3.0,
        minbet: float = 1.0,
    ) -> float:
        terminal, payoff = self._is_terminal(history, my_card, opp_card, pot, minbet)
        if terminal:
            return payoff

        player = len(history) % 2
        info_set = self._get_info_set(player, my_card, history, pot, minbet)
        node = self.nodes.get(info_set)
        if node is None:
            node = CFRNode(info_set=info_set)
            self.nodes[info_set] = node

        strategy = node.get_strategy(prob_my if player == 0 else prob_opp)
        util = [0.0] * len(ACTION_LIST)
        node_util = 0.0

        for idx, action in enumerate(ACTION_LIST):
            next_history, next_pot = self._next_state(history, action, pot, minbet)
            if player == 0:
                util[idx] = self.cfr(
                    my_card, opp_card, next_history, prob_my * strategy[idx], prob_opp, next_pot, minbet
                )
            else:
                util[idx] = self.cfr(
                    my_card, opp_card, next_history, prob_my, prob_opp * strategy[idx], next_pot, minbet
                )
            node_util += strategy[idx] * util[idx]

        for idx in range(len(ACTION_LIST)):
            regret = util[idx] - node_util
            if player == 0:
                node.regret_sum[idx] += prob_opp * regret
            else:
                node.regret_sum[idx] -= prob_my * regret

        return node_util

    def _get_info_set(self, player: int, card_value: float, history: str, pot: float, minbet: float) -> str:
        bucket = bucketize(card_value)
        role = "B" if player == 0 else "O"
        pot_state = int(math.log2(max(pot, 1)))
        return f"{role}|b{bucket}|p{pot_state}|h{history}"

    def _next_state(self, history: str, action: str, pot: float, minbet: float) -> Tuple[str, float]:
        if action == "fold":
            return history + "f", pot
        if action == "call":
            return history + "c", pot
        if action == "raise":
            return history + "r", pot + minbet
        raise ValueError(action)

    def _is_terminal(
        self,
        history: str,
        my_card: float,
        opp_card: float,
        pot: float,
        minbet: float,
    ) -> Tuple[bool, float]:
        if history.endswith("f"):
            if len(history) % 2 == 1:  # last action by player 0
                return True, 0.0
            else:
                return True, pot
        if history.endswith("cc") or history.endswith("rc") or history.endswith("cr"):
            return True, pot if my_card > opp_card else -pot
        return False, 0.0

    def export_strategy(self) -> Dict[str, List[float]]:
        return {info_set: node.get_average_strategy() for info_set, node in self.nodes.items()}

