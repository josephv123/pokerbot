"""
Evaluation utilities shared by the different learning approaches.

Two evaluation modes are provided:
1. Fast Gym rollouts for in-training diagnostics.
2. Full engine-based tests against the official opponent set.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Tuple

import numpy as np

from opponents import AllIn, John1, training_opponents
from randomTexas import pokerTest

from .poker_env import RandomTexasEnv


@dataclass
class EvalResult:
    opponent: str
    win_rate: float


def evaluate_in_env(
    policy_fn: Callable[[np.ndarray], int],
    env: RandomTexasEnv,
    episodes: int = 100,
) -> Tuple[float, List[float]]:
    """
    Roll out a policy inside the Gym environment and report mean reward per episode.
    """
    returns: List[float] = []
    obs, _ = env.reset()
    for _ in range(episodes):
        done = False
        total = 0.0
        while not done:
            action = int(policy_fn(obs))
            obs, reward, terminated, truncated, _ = env.step(action)
            total += reward
            done = terminated or truncated
            if done:
                obs, _ = env.reset()
        returns.append(total)
    return float(np.mean(returns)), returns


def _format_result(name: str, win_rate: float) -> str:
    return f"{name:<12s} -> {win_rate * 100:5.1f}%"


def evaluate_against_training_set(
    player_cls,
    ngames: int = 200,
    verbosity: int = 0,
) -> List[EvalResult]:
    """
    Play the provided PokerPlayer class against all published training opponents.
    """
    results: List[EvalResult] = []
    for opponent in training_opponents:
        wr = pokerTest(player_cls, opponent, ngames, verbosity=0)
        if verbosity:
            print(_format_result(opponent.__name__, wr))
        results.append(EvalResult(opponent.__name__, wr))
    return results


def evaluate_baselines(player_cls, ngames: int = 200, verbosity: int = 1) -> List[EvalResult]:
    """
    Convenience wrapper for quick regressions vs AllIn & John1.
    """
    res = []
    for opponent in (AllIn, John1):
        wr = pokerTest(player_cls, opponent, ngames, verbosity=verbosity)
        res.append(EvalResult(opponent.__name__, wr))
    return res

