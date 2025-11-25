"""
Gym-compatible environment for Random Number Texas Hold'Em.

This environment is intentionally lightweight; it mirrors the flow of the
official `randomTexas.py` engine but simplifies betting so the agent makes a
single strategic decision per hand. The abstraction is sufficient for
reinforcement-learning loops while remaining faithful to the game's scoring
rules (chip conservation, blinds that double every 100 hands, etc.).
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

try:  # Prefer gymnasium but gracefully fall back to classic gym.
    import gymnasium as gym
    from gymnasium import spaces
except ModuleNotFoundError:  # pragma: no cover - fallback for legacy gym
    import gym
    from gym import spaces  # type: ignore

import numpy as np

from . import utils


@dataclass
class EnvConfig:
    starting_stack: float = 100.0
    initial_minbet: float = 1.0
    minbet_double_hands: int = 100
    opponent_aggression: float = 0.6  # [0,1], higher => more calls with weak cards
    max_hands: int = 1000  # safety horizon so episodes terminate


class RandomTexasEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self, config: Optional[EnvConfig] = None, seed: Optional[int] = None):
        super().__init__()
        self.config = config or EnvConfig()
        self.rng = random.Random(seed)
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(10,),
            dtype=np.float32,
        )

        # Dynamic state
        self.hand_count = 0
        self.myscore = self.config.starting_stack
        self.oppscore = self.config.starting_stack
        self.minbet = self.config.initial_minbet
        self.is_big_blind = False
        self.card = 0.0
        self.opp_card = 0.0
        self.pot = 0.0
        self.bet_round = 0
        self.done = False
        self.info: Dict = {}
        self.opp_stats = utils.OpponentStats()

    # ------------------------------
    # Gym API
    # ------------------------------
    def reset(self, *, seed: Optional[int] = None, options: Optional[Dict] = None):
        if seed is not None:
            self.rng.seed(seed)
        self.hand_count = 0
        self.myscore = self.config.starting_stack
        self.oppscore = self.config.starting_stack
        self.minbet = self.config.initial_minbet
        self.is_big_blind = bool(self.rng.getrandbits(1))
        self.done = False
        self.opp_stats.reset()
        self._start_new_hand()
        return self._get_obs(), self._get_info()

    def step(self, action: int):
        if self.done:
            raise RuntimeError("Episode already finished. Call reset().")

        reward, terminated = self._resolve_hand(action)
        truncated = False
        self.done = terminated

        observation = self._get_obs() if not self.done else np.zeros(10, dtype=np.float32)
        info = self._get_info()
        return observation, reward, terminated, truncated, info

    # ------------------------------
    # Core mechanics
    # ------------------------------
    def _start_new_hand(self):
        """Deal cards, post blinds, and prepare observation."""
        # Alternate blinds each hand.
        if self.hand_count > 0:
            self.is_big_blind = not self.is_big_blind
        self.hand_count += 1
        if self.hand_count % self.config.minbet_double_hands == 0:
            self.minbet *= 2

        self.card = self.rng.random()
        self.opp_card = self.rng.random()
        self.bet_round = 0

        # Post blinds
        sb = self.minbet
        bb = min(2 * self.minbet, min(self.myscore, self.oppscore))
        self.pot = 0.0
        if self.is_big_blind:
            invest_me = min(bb, self.myscore)
            invest_opp = min(sb, self.oppscore)
        else:
            invest_me = min(sb, self.myscore)
            invest_opp = min(bb, self.oppscore)
        self.myscore -= invest_me
        self.oppscore -= invest_opp
        self.pot = invest_me + invest_opp

    def _resolve_hand(self, action: int) -> Tuple[float, bool]:
        """
        Apply player's action, simulate opponent response, settle chips.
        Returns (reward, terminated).
        """
        total_before = self.myscore
        action_bet = utils.decode_action(
            action,
            pot=self.pot,
            minbet=self.minbet,
            myscore=self.myscore,
            oppscore=self.oppscore,
        )

        if action_bet < self.pot:  # fold
            self.opp_stats.update("raise")  # opponent effectively pressured fold
            self.oppscore += self.pot
        elif action_bet == self.pot:  # call/check -> showdown
            self.opp_stats.update("call")
            winner = self._compare_cards()
            if winner > 0:
                self.myscore += self.pot
            else:
                self.oppscore += self.pot
        else:  # raise -> opponent responds
            reward_delta = self._opponent_response(action_bet)
            # reward already applied inside _opponent_response via stack updates
        # Determine next state / termination
        terminated = self._is_terminal()
        reward = self.myscore - total_before
        if not terminated:
            self._start_new_hand()
        return reward, terminated

    def _opponent_response(self, agent_bet: float):
        """Opponent either folds or calls based on hidden card and aggression."""
        additional = max(agent_bet - self.pot, 0.0)
        call_threshold = 0.25 + 0.5 * self.config.opponent_aggression
        opponent_calls = self.opp_card >= call_threshold
        if not opponent_calls and self.opp_card < (call_threshold - 0.15):
            self.opp_stats.update("fold")
            # Agent scoops pot (opponent already contributed blinds earlier)
            self.myscore += self.pot
            return

        self.opp_stats.update("call")
        call_amount = min(additional, self.oppscore)
        self.oppscore -= call_amount
        self.pot += call_amount
        # Deduct agent's raise (already taken out of stack during decode via
        # utils.clip_to_stack -> reflect actual chips invested).
        agent_contribution = min(additional, self.myscore)
        self.myscore -= agent_contribution

        winner = self._compare_cards()
        if winner > 0:
            self.myscore += self.pot
        else:
            self.oppscore += self.pot

    def _compare_cards(self) -> int:
        """Return +1 if agent wins showdown, else -1."""
        if self.card >= self.opp_card:
            return 1
        return -1

    def _is_terminal(self) -> bool:
        stacks_exhausted = self.myscore <= 0 or self.oppscore <= 0
        hands_exhausted = self.hand_count >= self.config.max_hands
        return stacks_exhausted or hands_exhausted

    # ------------------------------
    # Helpers
    # ------------------------------
    def _get_obs(self) -> np.ndarray:
        return utils.encode_state(
            card=self.card,
            pot=self.pot,
            myscore=self.myscore,
            oppscore=self.oppscore,
            minbet=self.minbet,
            is_big_blind=self.is_big_blind,
            bet_round=self.bet_round,
            opponent_stats=self.opp_stats,
        )

    def _get_info(self) -> Dict:
        return {
            "myscore": self.myscore,
            "oppscore": self.oppscore,
            "minbet": self.minbet,
            "hand_count": self.hand_count,
        }

    # Gym render / close (optional)
    def render(self):
        print(
            f"Hand {self.hand_count} | "
            f"{'BB' if self.is_big_blind else 'SB'} | "
            f"card={self.card:.3f} opp={self.opp_card:.3f} | "
            f"pot={self.pot:.1f} | stacks=({self.myscore:.1f}, {self.oppscore:.1f})"
        )

    def close(self):
        pass

