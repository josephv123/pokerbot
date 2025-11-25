"""
Unified CLI entrypoint for training all RL / CFR approaches.

Usage examples:
    python -m rl_training.train --agent dqn --steps 200000
    python -m rl_training.train --agent ppo --steps 500000
    python -m rl_training.train --agent cfr --iterations 1000000
    python -m rl_training.train --agent hybrid --iterations 2000
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np

from .cfr_agent import CFRTrainer
from .dqn_agent import DQNAgent, DQNConfig
from .hybrid_agent import HybridAgent, HybridConfig, OpponentProfile
from .poker_env import EnvConfig, RandomTexasEnv
from .ppo_agent import PPOAgent, PPOConfig


def train_dqn(args):
    env = RandomTexasEnv(EnvConfig(), seed=args.seed)
    config = DQNConfig(max_steps=args.steps, train_device=args.device)
    agent = DQNAgent(env, config)
    metrics = agent.train()
    path = agent.save("dqn.pt")
    return {"model_path": path, "episodes": len(metrics)}


def train_ppo(args):
    env = RandomTexasEnv(EnvConfig(), seed=args.seed)
    config = PPOConfig(max_steps=args.steps, train_device=args.device)
    agent = PPOAgent(env, config)
    history = agent.train()
    agent.save()
    return {"history": history}


def train_cfr(args):
    trainer = CFRTrainer(rng_seed=args.seed)
    trainer.train(iterations=args.iterations)
    strategy = trainer.export_strategy()
    path = Path("rl_training/models/cfr_strategy.json")
    path.write_text(json.dumps(strategy))
    return {"strategy_path": str(path), "num_nodes": len(strategy)}


def _mock_reward_fn(params, profile: OpponentProfile) -> float:
    """
    Simple differentiable reward surrogate: encourages params that
    exploit observed aggression levels.
    """
    bluff_mult, value_mult, call_mult, bet_mult = params
    aggression = profile.aggression
    value = (
        0.5 * (value_mult - 1.0)
        + 0.3 * (bluff_mult - aggression)
        - 0.2 * abs(call_mult - (1.0 - aggression / 2))
        + 0.1 * (bet_mult - 1.0)
    )
    return float(value)


def train_hybrid(args):
    rng = np.random.default_rng(args.seed)
    profiles = [
        OpponentProfile(
            fold_rate=float(rng.uniform(0.1, 0.6)),
            call_rate=float(rng.uniform(0.2, 0.6)),
            raise_rate=float(rng.uniform(0.1, 0.4)),
            aggression=float(rng.uniform(0.2, 1.5)),
            bet_card_mean=float(rng.uniform(0.3, 0.7)),
        )
        for _ in range(64)
    ]
    config = HybridConfig()
    agent = HybridAgent(config, device=args.device)
    history = agent.train(profiles, _mock_reward_fn, iterations=args.iterations)
    path = Path("rl_training/models/hybrid.pt")
    os.makedirs(path.parent, exist_ok=True)
    import torch  # local import to avoid mandatory dependency for CFR-only runs

    torch.save({"state_dict": agent.policy.state_dict()}, path)
    return {"history": history, "model_path": str(path)}


def main():
    parser = argparse.ArgumentParser(description="Train poker RL agents")
    parser.add_argument("--agent", choices=["dqn", "ppo", "cfr", "hybrid"], required=True)
    parser.add_argument("--steps", type=int, default=200_000, help="Env steps / timesteps")
    parser.add_argument("--iterations", type=int, default=1_000_000, help="Iterations for CFR/Hybrid")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", type=str, default="cpu")
    args = parser.parse_args()

    if args.agent == "dqn":
        result = train_dqn(args)
    elif args.agent == "ppo":
        result = train_ppo(args)
    elif args.agent == "cfr":
        result = train_cfr(args)
    else:
        result = train_hybrid(args)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

