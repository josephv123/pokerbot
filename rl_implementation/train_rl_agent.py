"""
Train RL Poker Agent
Main training script for DQN poker player
"""

import sys
import os
import time
import random
import numpy as np
from tqdm import tqdm

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Assignment3_Class'))

from dqn_agent import DQNAgent
from rl_poker_env import PokerEnv
from config import *
from utils import estimate_training_time

# Import opponents
try:
    from opponents import training_opponents, John1, AllIn
    use_training_opponents = len(training_opponents) > 0
except:
    from opponents.basic_players import John1, AllIn
    training_opponents = []
    use_training_opponents = False
    print("Note: Training opponents not available. Using basic players for demonstration.")


def train(agent, opponents, num_epochs=NUM_EPOCHS, games_per_opponent=GAMES_PER_OPPONENT,
          save_dir=SAVE_DIR, verbose=VERBOSE):
    """
    Train DQN agent against multiple opponents

    Args:
        agent: DQNAgent instance
        opponents: List of opponent classes
        num_epochs: Number of passes through all opponents
        games_per_opponent: Games to play per opponent
        save_dir: Directory to save checkpoints
        verbose: Whether to print progress

    Returns:
        agent: Trained agent
        training_stats: Dictionary of training statistics
    """
    os.makedirs(save_dir, exist_ok=True)

    # Training statistics
    stats = {
        'total_games': 0,
        'total_wins': 0,
        'total_losses': 0,
        'win_rates_per_opponent': [],
        'losses_per_step': [],
        'epsilon_values': [],
        'opponent_names': []
    }

    total_steps = 0
    start_time = time.time()

    print("="*70)
    print(f"Starting RL Poker Training")
    print("="*70)
    print(f"Opponents: {len(opponents)}")
    print(f"Games per opponent: {games_per_opponent}")
    print(f"Epochs: {num_epochs}")
    print(f"Estimated time: {estimate_training_time(len(opponents), games_per_opponent, num_epochs)}")
    print("="*70 + "\n")

    for epoch in range(num_epochs):
        print(f"\n{'='*70}")
        print(f"EPOCH {epoch+1}/{num_epochs}")
        print(f"{'='*70}\n")

        epoch_wins = 0
        epoch_games = 0

        for opp_idx, opponent_class in enumerate(opponents):
            opponent_name = opponent_class.__name__
            wins = 0
            total_reward = 0.0
            games_played = 0

            # Training bar for this opponent
            pbar = tqdm(range(games_per_opponent),
                        desc=f"[Ep{epoch+1}] vs {opponent_name:>15s}",
                        leave=True)

            for game_num in pbar:
                # Create environment
                env = PokerEnv(opponent_class, rng_seed=None, verbose=False)
                state = env.reset()
                done = False
                game_steps = 0

                # Play one complete game
                while not done:
                    # Get valid actions
                    valid_mask = env.get_valid_actions_mask()

                    # Select action (epsilon-greedy)
                    action = agent.act(state, valid_mask, agent.epsilon)

                    # Take step
                    next_state, reward, done, info = env.step(action)

                    # Store transition
                    agent.step(state, action, reward, next_state, done)

                    # Train every TRAIN_FREQ steps
                    if total_steps % TRAIN_FREQ == 0 and len(agent.buffer) >= BATCH_SIZE:
                        loss = agent.learn(BATCH_SIZE)
                        if loss is not None:
                            stats['losses_per_step'].append((total_steps, loss))

                    # Update target network
                    if total_steps % TARGET_UPDATE_FREQ == 0:
                        agent.update_target_network()

                    state = next_state
                    total_steps += 1
                    game_steps += 1

                # Game finished
                if info['won']:
                    wins += 1
                total_reward += info['total_reward']
                games_played += 1

                # Update progress bar
                current_win_rate = wins / (game_num + 1)
                pbar.set_postfix({
                    'WR': f"{current_win_rate:.2%}",
                    'ε': f"{agent.epsilon:.3f}",
                    'buf': len(agent.buffer)
                })

                # Decay epsilon after each game
                agent.decay_epsilon()

            # Opponent finished
            win_rate = wins / games_played if games_played > 0 else 0
            stats['win_rates_per_opponent'].append(win_rate)
            stats['opponent_names'].append(opponent_name)
            stats['epsilon_values'].append(agent.epsilon)

            epoch_wins += wins
            epoch_games += games_played
            stats['total_games'] += games_played
            stats['total_wins'] += wins
            stats['total_losses'] += (games_played - wins)

            if verbose:
                print(f"  → {opponent_name}: {win_rate:.1%} ({wins}/{games_played}), "
                      f"ε={agent.epsilon:.3f}, buffer={len(agent.buffer)}")

            # Save checkpoint every N opponents
            if (opp_idx + 1) % CHECKPOINT_EVERY_N_OPPONENTS == 0:
                checkpoint_path = os.path.join(save_dir,
                                               f'checkpoint_ep{epoch+1}_opp{opp_idx+1}.pt')
                agent.save(checkpoint_path)
                if verbose:
                    print(f"  💾 Checkpoint saved: {checkpoint_path}")

        # Epoch summary
        epoch_win_rate = epoch_wins / epoch_games if epoch_games > 0 else 0
        elapsed = time.time() - start_time
        print(f"\n{'-'*70}")
        print(f"Epoch {epoch+1} Summary:")
        print(f"  Win Rate: {epoch_win_rate:.1%} ({epoch_wins}/{epoch_games})")
        print(f"  Epsilon: {agent.epsilon:.3f}")
        print(f"  Total Steps: {total_steps}")
        print(f"  Buffer Size: {len(agent.buffer)}")
        print(f"  Time Elapsed: {elapsed/60:.1f} minutes")
        print(f"{'-'*70}\n")

    # Save final model
    final_model_path = os.path.join(save_dir, 'final_model.pt')
    agent.save(final_model_path)
    print(f"\n✓ Training complete! Final model saved: {final_model_path}")

    # Final statistics
    total_time = time.time() - start_time
    overall_win_rate = stats['total_wins'] / stats['total_games'] if stats['total_games'] > 0 else 0

    print(f"\n{'='*70}")
    print(f"TRAINING SUMMARY")
    print(f"{'='*70}")
    print(f"Total Games: {stats['total_games']}")
    print(f"Overall Win Rate: {overall_win_rate:.1%} ({stats['total_wins']}/{stats['total_games']})")
    print(f"Final Epsilon: {agent.epsilon:.3f}")
    print(f"Total Training Steps: {total_steps}")
    print(f"Buffer Size: {len(agent.buffer)}")
    print(f"Total Time: {total_time/3600:.2f} hours ({total_time/60:.1f} minutes)")
    print(f"{'='*70}\n")

    return agent, stats


def main():
    """Main training function"""
    # Seed for reproducibility (optional)
    # random.seed(42)
    # np.random.seed(42)

    # Create agent
    print("Initializing DQN Agent...")
    agent = DQNAgent()
    print(f"  Network: {sum(p.numel() for p in agent.q_network.parameters())} parameters")
    print(f"  Device: {agent.device}\n")

    # Determine opponents to use
    if use_training_opponents and len(training_opponents) > 0:
        print(f"Using {len(training_opponents)} training opponents")
        opponents = training_opponents
    else:
        print("Using basic opponents for demonstration")
        # Use basic opponents multiple times to simulate variety
        opponents = [John1, AllIn] * 5  # 10 opponents total

    # Train agent
    agent, stats = train(agent, opponents,
                         num_epochs=NUM_EPOCHS,
                         games_per_opponent=GAMES_PER_OPPONENT)

    # Save final statistics
    import json
    stats_path = os.path.join(SAVE_DIR, 'training_stats.json')
    with open(stats_path, 'w') as f:
        # Convert to serializable format
        serializable_stats = {
            'total_games': stats['total_games'],
            'total_wins': stats['total_wins'],
            'total_losses': stats['total_losses'],
            'overall_win_rate': stats['total_wins'] / stats['total_games'],
            'win_rates_per_opponent': stats['win_rates_per_opponent'],
            'opponent_names': stats['opponent_names'],
            'final_epsilon': stats['epsilon_values'][-1] if stats['epsilon_values'] else EPSILON_END
        }
        json.dump(serializable_stats, f, indent=2)
    print(f"Training statistics saved: {stats_path}")


if __name__ == '__main__':
    main()
