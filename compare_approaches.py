"""
Script to benchmark all trained approaches side-by-side.

The comparison currently runs fast Gym rollouts for DQN/PPO as well as
prints metadata for CFR and Hybrid approaches if their artifacts exist.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from rl_training.dqn_agent import QNetwork
from rl_training.evaluate import evaluate_in_env
from rl_training.poker_env import RandomTexasEnv
from rl_training.ppo_agent import ActorCritic


def load_dqn_policy(path: Path):
    model = QNetwork()
    state_dict = torch.load(path, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()

    def policy(obs: np.ndarray) -> int:
        with torch.no_grad():
            tensor = torch.from_numpy(obs).float().unsqueeze(0)
            logits = model(tensor)
            return int(torch.argmax(logits, dim=1).item())

    return policy


def load_ppo_policy(path: Path):
    model = ActorCritic()
    state_dict = torch.load(path, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()

    def policy(obs: np.ndarray) -> int:
        with torch.no_grad():
            tensor = torch.from_numpy(obs).float()
            logits, _ = model(tensor)
            dist = torch.distributions.Categorical(logits=logits)
            return int(torch.argmax(dist.probs).item())

    return policy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=200)
    parser.add_argument("--models_dir", type=str, default="rl_training/models")
    args = parser.parse_args()

    models_dir = Path(args.models_dir)
    env = RandomTexasEnv()

    summary = {}

    dqn_path = models_dir / "dqn.pt"
    if dqn_path.exists():
        policy = load_dqn_policy(dqn_path)
        mean_reward, _ = evaluate_in_env(policy, env, episodes=args.episodes)
        summary["dqn"] = {"mean_reward": mean_reward}

    ppo_path = models_dir / "ppo.pt"
    if ppo_path.exists():
        policy = load_ppo_policy(ppo_path)
        mean_reward, _ = evaluate_in_env(policy, env, episodes=args.episodes)
        summary["ppo"] = {"mean_reward": mean_reward}

    cfr_path = models_dir / "cfr_strategy.json"
    if cfr_path.exists():
        summary["cfr"] = {"strategy_nodes": len(json.loads(cfr_path.read_text()))}

    hybrid_path = models_dir / "hybrid.pt"
    if hybrid_path.exists():
        summary["hybrid"] = {"path": str(hybrid_path)}

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

