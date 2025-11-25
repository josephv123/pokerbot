"""
Utility helpers for RL training infrastructure.

Responsibilities:
- Encode low-level game state into the fixed 10D observation vector
  expected by the RL agents.
- Decode discrete policy outputs into legal betting amounts that can be
  forwarded to the Random Number Texas Hold'Em engine.
- Track simple opponent statistics so agents can condition their policy
  on population behavior during training.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, Optional

import numpy as np

MAX_SCORE = 200.0  # Both players start with 100 points => max stack swing 200
EPSILON = 1e-9


def _safe_div(numerator: float, denominator: float) -> float:
    if abs(denominator) < EPSILON:
        return 0.0
    return float(numerator) / float(denominator)


def normalize_card(card: float) -> float:
    """Cards are already in [0, 1], but coerce to float for consistency."""
    return float(np.clip(card, 0.0, 1.0))


def normalize_score(score: float) -> float:
    """Normalize chips with respect to max total chips (200)."""
    return np.clip(_safe_div(score, MAX_SCORE), 0.0, 1.0)


def normalize_pot(pot: float, myscore: float, oppscore: float) -> float:
    """Divide pot by current max stack (min of the two stacks)."""
    max_possible = max(min(myscore, oppscore), 1.0)
    return np.clip(_safe_div(pot, max_possible), 0.0, 1.0)


def encode_minbet(minbet: float) -> float:
    """Log-scale so doubling blinds creates roughly linear changes."""
    return np.clip(_safe_div(math.log1p(minbet), math.log1p(MAX_SCORE)), 0.0, 1.0)


def encode_role(is_big_blind: bool) -> float:
    return 1.0 if is_big_blind else 0.0


def encode_bet_round(round_idx: int, max_rounds: int = 4) -> float:
    """Map bet round (0,1,2,...) to [0,1] with configurable cap."""
    capped = min(max(round_idx, 0), max_rounds)
    return float(capped) / float(max_rounds)


@dataclass
class OpponentStats:
    """
    Track aggregate opponent tendencies seen by the environment.

    fold / call / raise counters are normalized into frequencies while the
    aggression metric approximates AF = (raises) / max(calls, 1).
    """

    folds: int = 0
    calls: int = 0
    raises: int = 0

    def reset(self) -> None:
        self.folds = self.calls = self.raises = 0

    def update(self, action: str) -> None:
        action = action.lower()
        if action == "fold":
            self.folds += 1
        elif action == "call":
            self.calls += 1
        elif action == "raise":
            self.raises += 1

    def as_features(self) -> np.ndarray:
        total = max(self.folds + self.calls + self.raises, 1)
        fold_rate = self.folds / total
        call_rate = self.calls / total
        raise_rate = self.raises / total
        aggression = self.raises / max(self.calls, 1)
        return np.array([fold_rate, call_rate, raise_rate, aggression], dtype=np.float32)


def encode_state(
    *,
    card: float,
    pot: float,
    myscore: float,
    oppscore: float,
    minbet: float,
    is_big_blind: bool,
    bet_round: int,
    opponent_stats: Optional[OpponentStats] = None,
) -> np.ndarray:
    """
    Assemble the 10D observation vector defined in the project plan.
    """

    opp_features = (
        opponent_stats.as_features()
        if opponent_stats is not None
        else np.zeros(4, dtype=np.float32)
    )

    obs = np.array(
        [
            normalize_card(card),
            normalize_pot(pot, myscore, oppscore),
            normalize_score(myscore),
            normalize_score(oppscore),
            encode_minbet(minbet),
            encode_role(is_big_blind),
            encode_bet_round(bet_round),
            *opp_features,
        ],
        dtype=np.float32,
    )
    assert obs.shape == (10,), f"Observation must be 10-D, got {obs.shape}"
    return obs


def clip_to_stack(amount: float, myscore: float, oppscore: float) -> float:
    """Legal bets cannot exceed the smaller stack."""
    max_bet = max(min(myscore, oppscore), 0.0)
    return float(np.clip(amount, 0.0, max_bet))


def decode_action(
    action_idx: int,
    *,
    pot: float,
    minbet: float,
    myscore: float,
    oppscore: float,
) -> float:
    """
    Map discrete action id to a legal total bet size.
    Actions:
    0 = fold, 1 = call/check, 2 = raise 1x minbet, 3 = raise 2x, 4 = raise 4x, 5 = all-in
    """

    action_idx = int(action_idx)
    max_bet = clip_to_stack(min(myscore, oppscore), myscore, oppscore)

    if action_idx <= 0:
        return 0.0
    if action_idx == 1:
        return clip_to_stack(pot, myscore, oppscore)

    raise_multipliers = {
        2: 1,
        3: 2,
        4: 4,
    }
    if action_idx in raise_multipliers:
        addition = minbet * raise_multipliers[action_idx]
        return clip_to_stack(pot + addition, myscore, oppscore)
    # action 5 or anything larger -> shove
    return clip_to_stack(max_bet, myscore, oppscore)


def batch_encode_states(state_iter: Iterable[Dict]) -> np.ndarray:
    """
    Convenience helper for agents that want vectorized encoding.
    """
    encoded: list[np.ndarray] = [
        encode_state(**state_dict) for state_dict in state_iter
    ]
    return np.vstack(encoded)

