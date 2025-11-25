"""
Proximal Policy Optimization agent tailored for RandomTexasEnv.

Highlights:
- Shared feature extractor feeding actor/critic heads
- Clipped surrogate objective (epsilon = 0.2)
- Generalized Advantage Estimation (lambda = 0.95)
- Entropy bonus for exploration
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from .poker_env import RandomTexasEnv


@dataclass
class PPOConfig:
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_epsilon: float = 0.2
    entropy_coef: float = 0.01
    value_coef: float = 0.5
    learning_rate: float = 3e-4
    num_epochs: int = 4
    minibatch_size: int = 64
    rollout_steps: int = 2048
    max_steps: int = 500_000
    train_device: str = "cpu"
    save_path: str = "rl_training/models/ppo.pt"


class ActorCritic(nn.Module):
    def __init__(self, obs_dim: int = 10, num_actions: int = 6):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(obs_dim, 128),
            nn.Tanh(),
            nn.Linear(128, 128),
            nn.Tanh(),
        )
        self.policy_head = nn.Linear(128, num_actions)
        self.value_head = nn.Linear(128, 1)

    def forward(self, x):
        feats = self.shared(x)
        logits = self.policy_head(feats)
        value = self.value_head(feats)
        return logits, value.squeeze(-1)


class PPOAgent:
    def __init__(self, env: RandomTexasEnv, config: PPOConfig | None = None):
        self.env = env
        self.config = config or PPOConfig()
        self.device = torch.device(self.config.train_device)
        self.model = ActorCritic().to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.config.learning_rate)

    def select_action(self, obs: np.ndarray):
        obs_tensor = torch.from_numpy(obs).float().to(self.device)
        logits, value = self.model(obs_tensor)
        dist = torch.distributions.Categorical(logits=logits)
        action = dist.sample()
        return int(action.item()), dist.log_prob(action).item(), float(value.item()), dist.entropy().item()

    def collect_rollout(self):
        obs, _ = self.env.reset()
        batch = {
            "obs": [],
            "actions": [],
            "log_probs": [],
            "values": [],
            "rewards": [],
            "dones": [],
        }
        steps = 0
        while steps < self.config.rollout_steps:
            action, log_prob, value, _ = self.select_action(obs)
            next_obs, reward, terminated, truncated, _ = self.env.step(action)
            done = terminated or truncated

            for key, val in [
                ("obs", obs),
                ("actions", action),
                ("log_probs", log_prob),
                ("values", value),
                ("rewards", reward),
                ("dones", done),
            ]:
                batch[key].append(val)

            obs = next_obs
            steps += 1

            if done:
                obs, _ = self.env.reset()

        return batch

    def compute_advantages(self, rewards, values, dones):
        advantages = np.zeros_like(rewards, dtype=np.float32)
        last_adv = 0.0
        last_value = 0.0

        for t in reversed(range(len(rewards))):
            mask = 1.0 - float(dones[t])
            delta = rewards[t] + self.config.gamma * last_value * mask - values[t]
            last_adv = delta + self.config.gamma * self.config.gae_lambda * mask * last_adv
            advantages[t] = last_adv
            last_value = values[t]

        returns = advantages + values
        return advantages, returns

    def update(self, batch: Dict[str, List]):
        obs = torch.tensor(batch["obs"], dtype=torch.float32, device=self.device)
        actions = torch.tensor(batch["actions"], dtype=torch.long, device=self.device)
        old_log_probs = torch.tensor(batch["log_probs"], dtype=torch.float32, device=self.device)
        values = torch.tensor(batch["values"], dtype=torch.float32, device=self.device)
        rewards = np.array(batch["rewards"], dtype=np.float32)
        dones = np.array(batch["dones"], dtype=np.float32)

        advantages, returns = self.compute_advantages(rewards, values.cpu().numpy(), dones)
        advantages = torch.tensor(advantages, dtype=torch.float32, device=self.device)
        returns = torch.tensor(returns, dtype=torch.float32, device=self.device)
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        dataset_size = obs.size(0)
        for _ in range(self.config.num_epochs):
            indices = np.arange(dataset_size)
            np.random.shuffle(indices)
            for start in range(0, dataset_size, self.config.minibatch_size):
                end = start + self.config.minibatch_size
                mb_idx = indices[start:end]
                mb_obs = obs[mb_idx]
                mb_actions = actions[mb_idx]
                mb_old_log_probs = old_log_probs[mb_idx]
                mb_adv = advantages[mb_idx]
                mb_returns = returns[mb_idx]

                logits, values_pred = self.model(mb_obs)
                dist = torch.distributions.Categorical(logits=logits)
                log_probs = dist.log_prob(mb_actions)
                entropy = dist.entropy().mean()

                ratios = torch.exp(log_probs - mb_old_log_probs)
                surr1 = ratios * mb_adv
                surr2 = torch.clamp(ratios, 1.0 - self.config.clip_epsilon, 1.0 + self.config.clip_epsilon) * mb_adv
                policy_loss = -torch.min(surr1, surr2).mean()

                value_loss = nn.functional.mse_loss(values_pred, mb_returns)

                loss = policy_loss + self.config.value_coef * value_loss - self.config.entropy_coef * entropy
                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(self.model.parameters(), 0.5)
                self.optimizer.step()

    def train(self):
        total_steps = 0
        history = []
        while total_steps < self.config.max_steps:
            batch = self.collect_rollout()
            total_steps += len(batch["rewards"])
            self.update(batch)
            avg_reward = np.mean(batch["rewards"])
            history.append({"steps": total_steps, "avg_reward": float(avg_reward)})
        return history

    def save(self):
        torch.save(self.model.state_dict(), self.config.save_path)

    def load(self, path: str | None = None):
        path = path or self.config.save_path
        state_dict = torch.load(path, map_location=self.device)
        self.model.load_state_dict(state_dict)

