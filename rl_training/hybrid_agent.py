"""
Hybrid GTO + RL exploitation layer.

Baseline strategy: OptimalThresholdPlayer. The hybrid module learns four
continuous multipliers conditioned on opponent statistics:
- bluff_mult (0.1 - 4.0)
- value_mult (0.8 - 1.3)
- call_mult (0.6 - 1.2)
- bet_mult (1.0 - 6.0)

Those multipliers can be fed into a downstream PokerPlayer implementation to
modulate thresholds and bet sizing live.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Sequence, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


@dataclass
class OpponentProfile:
    fold_rate: float
    call_rate: float
    raise_rate: float
    aggression: float
    bet_card_mean: float

    def as_array(self) -> np.ndarray:
        return np.array(
            [
                self.fold_rate,
                self.call_rate,
                self.raise_rate,
                self.aggression,
                self.bet_card_mean,
            ],
            dtype=np.float32,
        )


@dataclass
class HybridConfig:
    obs_dim: int = 5
    action_dim: int = 4
    hidden_dim: int = 128
    learning_rate: float = 3e-4
    gamma: float = 0.99
    lam: float = 0.95
    clip_eps: float = 0.2
    entropy_coef: float = 0.005
    value_coef: float = 0.5
    rollout_size: int = 256
    minibatch_size: int = 64
    epochs: int = 4


PARAM_RANGES = [
    (0.1, 4.0),
    (0.8, 1.3),
    (0.6, 1.2),
    (1.0, 6.0),
]


class HybridPolicy(nn.Module):
    def __init__(self, config: HybridConfig):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(config.obs_dim, config.hidden_dim),
            nn.ReLU(),
            nn.Linear(config.hidden_dim, config.hidden_dim),
            nn.ReLU(),
        )
        self.mean_head = nn.Linear(config.hidden_dim, config.action_dim)
        self.log_std = nn.Parameter(torch.zeros(config.action_dim))
        self.value_head = nn.Linear(config.hidden_dim, 1)

    def forward(self, obs: torch.Tensor):
        feats = self.shared(obs)
        mean = torch.tanh(self.mean_head(feats))
        value = self.value_head(feats).squeeze(-1)
        return mean, value

    def sample(self, obs: torch.Tensor):
        mean, value = self.forward(obs)
        std = torch.exp(self.log_std)
        dist = torch.distributions.Normal(mean, std)
        raw_action = dist.rsample()
        log_prob = dist.log_prob(raw_action).sum(-1)
        action = torch.tanh(raw_action)
        scaled_action = self._scale_to_ranges(action)
        return scaled_action, log_prob, value

    def _scale_to_ranges(self, norm_action: torch.Tensor) -> torch.Tensor:
        scaled = []
        for idx, (low, high) in enumerate(PARAM_RANGES):
            a = norm_action[..., idx]
            scaled_val = (a + 1) / 2 * (high - low) + low
            scaled.append(scaled_val)
        return torch.stack(scaled, dim=-1)


class HybridAgent:
    def __init__(self, config: HybridConfig | None = None, device: str = "cpu"):
        self.config = config or HybridConfig()
        self.device = torch.device(device)
        self.policy = HybridPolicy(self.config).to(self.device)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=self.config.learning_rate)

    def rollout(
        self,
        profiles: Sequence[OpponentProfile],
        reward_fn: Callable[[np.ndarray, OpponentProfile], float],
    ):
        obs_buffer = []
        action_buffer = []
        logprob_buffer = []
        value_buffer = []
        reward_buffer = []
        done_buffer = []

        steps = 0
        while steps < self.config.rollout_size:
            profile = profiles[steps % len(profiles)]
            obs = torch.from_numpy(profile.as_array()).float().to(self.device)
            action, logprob, value = self.policy.sample(obs.unsqueeze(0))
            action_np = action.squeeze(0).detach().cpu().numpy()
            reward = reward_fn(action_np, profile)

            obs_buffer.append(obs.cpu().numpy())
            action_buffer.append(action_np)
            logprob_buffer.append(logprob.item())
            value_buffer.append(value.item())
            reward_buffer.append(reward)
            done_buffer.append(0.0)  # episodic boundaries handled externally

            steps += 1

        return {
            "obs": np.array(obs_buffer, dtype=np.float32),
            "actions": np.array(action_buffer, dtype=np.float32),
            "log_probs": np.array(logprob_buffer, dtype=np.float32),
            "values": np.array(value_buffer, dtype=np.float32),
            "rewards": np.array(reward_buffer, dtype=np.float32),
            "dones": np.array(done_buffer, dtype=np.float32),
        }

    def compute_advantages(self, rewards, values, dones):
        advantages = np.zeros_like(rewards)
        gae = 0.0
        next_value = 0.0
        for t in reversed(range(len(rewards))):
            mask = 1.0 - dones[t]
            delta = rewards[t] + self.config.gamma * next_value * mask - values[t]
            gae = delta + self.config.gamma * self.config.lam * mask * gae
            advantages[t] = gae
            next_value = values[t]
        returns = advantages + values
        return advantages, returns

    def update(self, batch):
        obs = torch.tensor(batch["obs"], dtype=torch.float32, device=self.device)
        actions = torch.tensor(batch["actions"], dtype=torch.float32, device=self.device)
        old_log_probs = torch.tensor(batch["log_probs"], dtype=torch.float32, device=self.device)
        values = torch.tensor(batch["values"], dtype=torch.float32, device=self.device)
        rewards = batch["rewards"]
        dones = batch["dones"]

        advantages, returns = self.compute_advantages(rewards, values.cpu().numpy(), dones)
        advantages = torch.tensor((advantages - advantages.mean()) / (advantages.std() + 1e-8), dtype=torch.float32, device=self.device)
        returns = torch.tensor(returns, dtype=torch.float32, device=self.device)

        dataset_size = obs.size(0)
        for _ in range(self.config.epochs):
            idx = np.arange(dataset_size)
            np.random.shuffle(idx)
            for start in range(0, dataset_size, self.config.minibatch_size):
                end = start + self.config.minibatch_size
                mb_idx = idx[start:end]

                mean, value = self.policy.forward(obs[mb_idx])
                std = torch.exp(self.policy.log_std)
                dist = torch.distributions.Normal(mean, std)
                raw_actions = torch.atanh(
                    torch.clamp(
                        (actions[mb_idx] - torch.tensor([low for low, _ in PARAM_RANGES], device=self.device))
                        / torch.tensor([high - low for low, high in PARAM_RANGES], device=self.device)
                        * 2
                        - 1,
                        -0.999,
                        0.999,
                    )
                )
                log_probs = dist.log_prob(raw_actions).sum(-1)
                entropy = dist.entropy().sum(-1).mean()

                ratios = torch.exp(log_probs - old_log_probs[mb_idx])
                surr1 = ratios * advantages[mb_idx]
                surr2 = torch.clamp(ratios, 1 - self.config.clip_eps, 1 + self.config.clip_eps) * advantages[mb_idx]
                policy_loss = -torch.min(surr1, surr2).mean()

                value_loss = nn.functional.mse_loss(value, returns[mb_idx])
                loss = policy_loss + self.config.value_coef * value_loss - self.config.entropy_coef * entropy
                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.policy.parameters(), 0.5)
                self.optimizer.step()

    def train(
        self,
        profiles: Sequence[OpponentProfile],
        reward_fn: Callable[[np.ndarray, OpponentProfile], float],
        iterations: int = 1000,
    ):
        history = []
        for it in range(iterations):
            batch = self.rollout(profiles, reward_fn)
            self.update(batch)
            mean_reward = float(np.mean(batch["rewards"]))
            history.append({"iter": it, "reward": mean_reward})
        return history

