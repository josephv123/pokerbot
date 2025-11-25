"""
Deep Q-Network implementation tailored for RandomTexasEnv.

Key features extracted from the project plan:
- 2 hidden layers of 128 units each
- Double DQN target calculation
- Target network update every `target_update_freq` steps
- Experience replay buffer (default 100k transitions)
- Epsilon-greedy exploration (linear decay)
"""

from __future__ import annotations

import os
from collections import deque
from dataclasses import dataclass
from typing import Deque, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from .poker_env import RandomTexasEnv


@dataclass
class DQNConfig:
    gamma: float = 0.99
    lr: float = 1e-4
    batch_size: int = 64
    buffer_size: int = 100_000
    min_buffer_size: int = 5_000
    target_update_freq: int = 1_000
    epsilon_start: float = 1.0
    epsilon_end: float = 0.01
    epsilon_decay_steps: int = 50_000
    max_steps: int = 200_000
    train_device: str = "cpu"
    save_dir: str = "rl_training/models"


class QNetwork(nn.Module):
    def __init__(self, input_dim: int = 10, num_actions: int = 6):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, num_actions),
        )

    def forward(self, x):
        return self.net(x)


class ReplayBuffer:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer: Deque[Tuple[np.ndarray, int, float, np.ndarray, bool]] = deque(
            maxlen=capacity
        )

    def add(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int):
        idx = np.random.choice(len(self.buffer), batch_size, replace=False)
        states, actions, rewards, next_states, dones = zip(*(self.buffer[i] for i in idx))
        return (
            np.array(states, dtype=np.float32),
            np.array(actions, dtype=np.int64),
            np.array(rewards, dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones, dtype=np.float32),
        )

    def __len__(self):
        return len(self.buffer)


class DQNAgent:
    def __init__(self, env: RandomTexasEnv, config: DQNConfig | None = None):
        self.env = env
        self.config = config or DQNConfig()
        self.device = torch.device(self.config.train_device)
        self.policy_net = QNetwork().to(self.device)
        self.target_net = QNetwork().to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=self.config.lr)
        self.replay = ReplayBuffer(self.config.buffer_size)
        self.steps_done = 0
        os.makedirs(self.config.save_dir, exist_ok=True)

    def select_action(self, state: np.ndarray, epsilon: float) -> int:
        if np.random.rand() < epsilon:
            return self.env.action_space.sample()
        with torch.no_grad():
            state_tensor = torch.from_numpy(state).float().unsqueeze(0).to(self.device)
            q_values = self.policy_net(state_tensor)
            return int(torch.argmax(q_values, dim=1).item())

    def compute_epsilon(self) -> float:
        decay_ratio = min(1.0, self.steps_done / self.config.epsilon_decay_steps)
        epsilon = self.config.epsilon_start + decay_ratio * (
            self.config.epsilon_end - self.config.epsilon_start
        )
        return max(self.config.epsilon_end, epsilon)

    def optimize(self):
        if len(self.replay) < self.config.min_buffer_size:
            return 0.0
        states, actions, rewards, next_states, dones = self.replay.sample(
            self.config.batch_size
        )
        states = torch.from_numpy(states).to(self.device)
        actions = torch.from_numpy(actions).unsqueeze(-1).to(self.device)
        rewards = torch.from_numpy(rewards).unsqueeze(-1).to(self.device)
        next_states = torch.from_numpy(next_states).to(self.device)
        dones = torch.from_numpy(dones).unsqueeze(-1).to(self.device)

        q_values = self.policy_net(states).gather(1, actions)

        with torch.no_grad():
            next_actions = torch.argmax(self.policy_net(next_states), dim=1, keepdim=True)
            next_q = self.target_net(next_states).gather(1, next_actions)
            target = rewards + self.config.gamma * (1 - dones) * next_q

        loss = nn.functional.mse_loss(q_values, target)
        self.optimizer.zero_grad()
        loss.backward()
        nn.utils.clip_grad_norm_(self.policy_net.parameters(), 5.0)
        self.optimizer.step()
        return loss.item()

    def train(self):
        obs, _ = self.env.reset()
        episode_reward = 0.0
        episode = 0
        metrics = []

        for step in range(1, self.config.max_steps + 1):
            self.steps_done = step
            epsilon = self.compute_epsilon()
            action = self.select_action(obs, epsilon)
            next_obs, reward, terminated, truncated, _ = self.env.step(action)
            done = terminated or truncated
            self.replay.add(obs, action, reward, next_obs, done)
            obs = next_obs
            episode_reward += reward

            loss = self.optimize()

            if step % self.config.target_update_freq == 0:
                self.target_net.load_state_dict(self.policy_net.state_dict())

            if done:
                metrics.append({"episode": episode, "reward": episode_reward})
                episode += 1
                obs, _ = self.env.reset()
                episode_reward = 0.0

        return metrics

    def save(self, name: str = "dqn.pt"):
        path = os.path.join(self.config.save_dir, name)
        torch.save(self.policy_net.state_dict(), path)
        return path

    def load(self, path: str):
        state_dict = torch.load(path, map_location=self.device)
        self.policy_net.load_state_dict(state_dict)
        self.target_net.load_state_dict(state_dict)

