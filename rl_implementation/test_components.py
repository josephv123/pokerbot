"""
Quick test script to verify core components work
"""

import sys
import os
import numpy as np

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Assignment3_Class'))

from opponent_tracker import OpponentTracker
from dqn_agent import DQNAgent, DuelingQNetwork
from rl_poker_env import PokerEnv
from opponents.basic_players import AllIn, John1
from config import *

def test_opponent_tracker():
    """Test opponent tracker"""
    print("Testing OpponentTracker...")
    tracker = OpponentTracker()

    # Simulate some observations
    for i in range(20):
        tracker.update_bet_response('fold', 0, 10, 1, 100)
        tracker.update_hand_end()

    features = tracker.get_features()
    print(f"  Features shape: {features.shape}")
    print(f"  Fold rate: {features[0]:.2f}")
    print(f"  Classification: {tracker.get_classification()}")
    print("  ✓ OpponentTracker working\n")

def test_dqn_network():
    """Test DQN network"""
    print("Testing DuelingQNetwork...")
    network = DuelingQNetwork()

    # Random input
    state = np.random.randn(19).astype(np.float32)
    import torch
    state_tensor = torch.FloatTensor(state).unsqueeze(0)

    # Forward pass
    q_values = network(state_tensor)
    print(f"  Input shape: {state.shape}")
    print(f"  Output shape: {q_values.shape}")
    print(f"  Q-values: {q_values.detach().numpy()}")
    print("  ✓ DuelingQNetwork working\n")

def test_dqn_agent():
    """Test DQN agent"""
    print("Testing DQNAgent...")
    agent = DQNAgent()

    # Test action selection
    state = np.random.randn(19).astype(np.float32)
    valid_mask = np.ones(7, dtype=bool)

    action = agent.act(state, valid_mask, epsilon=0.0)
    print(f"  Selected action (greedy): {action}")

    action = agent.act(state, valid_mask, epsilon=1.0)
    print(f"  Selected action (random): {action}")

    # Test learning
    for i in range(10):
        state = np.random.randn(19).astype(np.float32)
        next_state = np.random.randn(19).astype(np.float32)
        agent.step(state, i % 7, 1.0, next_state, False)

    if len(agent.buffer) >= BATCH_SIZE:
        loss = agent.learn()
        print(f"  Training loss: {loss}")
    print("  ✓ DQNAgent working\n")

def test_poker_env():
    """Test poker environment"""
    print("Testing PokerEnv...")
    env = PokerEnv(AllIn, rng_seed=42, verbose=False)

    # Reset and get initial state
    state = env.reset()
    print(f"  Initial state shape: {state.shape}")
    print(f"  Initial state: {state[:6]}... (showing first 6 features)")

    # Get valid actions
    valid_mask = env.get_valid_actions_mask()
    print(f"  Valid actions: {np.where(valid_mask)[0]}")

    # Take a few steps
    done = False
    steps = 0
    while not done and steps < 10:
        valid_mask = env.get_valid_actions_mask()
        action = np.random.choice(np.where(valid_mask)[0])
        next_state, reward, done, info = env.step(action)
        steps += 1

    print(f"  Took {steps} steps")
    print(f"  Last reward: {reward:.3f}")
    print(f"  Game done: {done}")
    if done:
        print(f"  Final info: Won={info['won']}, Score={info['final_score']:.1f}")
    print("  ✓ PokerEnv working\n")

def test_full_game():
    """Test a complete game"""
    print("Testing complete game...")
    env = PokerEnv(John1, rng_seed=42, verbose=False)
    agent = DQNAgent()

    state = env.reset()
    done = False
    total_reward = 0
    hands = 0

    while not done:
        valid_mask = env.get_valid_actions_mask()
        action = agent.act(state, valid_mask, epsilon=0.5)
        next_state, reward, done, info = env.step(action)

        # Store transition
        agent.step(state, action, reward, next_state, done)

        # Train if enough samples
        if len(agent.buffer) >= BATCH_SIZE and hands % 5 == 0:
            agent.learn()

        state = next_state
        total_reward += reward
        hands = info.get('hands_played', hands)

    print(f"  Game finished!")
    print(f"  Won: {info['won']}")
    print(f"  Total reward: {total_reward:.3f}")
    print(f"  Hands played: {hands}")
    print(f"  Buffer size: {len(agent.buffer)}")
    print("  ✓ Full game working\n")

if __name__ == '__main__':
    print("="*60)
    print("Running Component Tests")
    print("="*60 + "\n")

    try:
        test_opponent_tracker()
        test_dqn_network()
        test_dqn_agent()
        test_poker_env()
        test_full_game()

        print("="*60)
        print("ALL TESTS PASSED! ✓")
        print("="*60)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
