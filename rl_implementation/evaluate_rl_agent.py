"""
Evaluate RL Poker Agent
Test trained agent against opponents
"""

import sys
import os
import time
import argparse
from tqdm import tqdm

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Assignment3_Class'))

from dqn_agent import DQNAgent
from rl_poker_env import PokerEnv
from config import *

# Import opponents
try:
    from opponents import training_opponents, John1, AllIn
    use_training_opponents = len(training_opponents) > 0
except:
    from opponents.basic_players import John1, AllIn
    training_opponents = []
    use_training_opponents = False


def evaluate_agent(agent, opponents, games_per_opponent=EVAL_GAMES_PER_OPPONENT,
                    epsilon=EVAL_EPSILON, verbose=True):
    """
    Evaluate trained agent against opponents

    Args:
        agent: Trained DQNAgent
        opponents: List of opponent classes
        games_per_opponent: Number of games to play per opponent
        epsilon: Exploration rate (0 for greedy)
        verbose: Whether to print detailed results

    Returns:
        results: Dictionary of evaluation results
    """
    agent.set_eval_mode()
    original_epsilon = agent.epsilon
    agent.epsilon = epsilon

    results = {
        'win_rates': [],
        'opponent_names': [],
        'wins': [],
        'losses': [],
        'total_games': 0,
        'total_wins': 0
    }

    print("="*70)
    print(f"Evaluating RL Agent")
    print("="*70)
    print(f"Opponents: {len(opponents)}")
    print(f"Games per opponent: {games_per_opponent}")
    print(f"Epsilon: {epsilon}")
    print("="*70 + "\n")

    start_time = time.time()

    for opp_idx, opponent_class in enumerate(opponents):
        opponent_name = opponent_class.__name__
        wins = 0
        games_played = 0

        # Progress bar
        pbar = tqdm(range(games_per_opponent),
                    desc=f"vs {opponent_name:>15s}",
                    leave=True)

        for game_num in pbar:
            # Create environment
            env = PokerEnv(opponent_class, rng_seed=None, verbose=False)
            state = env.reset()
            done = False

            # Play one complete game
            while not done:
                # Get valid actions
                valid_mask = env.get_valid_actions_mask()

                # Select action (greedy or epsilon-greedy)
                action = agent.act(state, valid_mask, epsilon)

                # Take step
                next_state, reward, done, info = env.step(action)
                state = next_state

            # Game finished
            if info['won']:
                wins += 1
            games_played += 1

            # Update progress bar
            current_win_rate = wins / (game_num + 1)
            pbar.set_postfix({'WR': f"{current_win_rate:.2%}"})

        # Opponent finished
        win_rate = wins / games_played if games_played > 0 else 0
        results['win_rates'].append(win_rate)
        results['opponent_names'].append(opponent_name)
        results['wins'].append(wins)
        results['losses'].append(games_played - wins)
        results['total_games'] += games_played
        results['total_wins'] += wins

        if verbose:
            print(f"  {opponent_name:>15s}: {win_rate:>6.1%} ({wins}/{games_played})")

    # Overall statistics
    overall_win_rate = results['total_wins'] / results['total_games'] if results['total_games'] > 0 else 0
    elapsed_time = time.time() - start_time

    print(f"\n{'='*70}")
    print(f"EVALUATION SUMMARY")
    print(f"{'='*70}")
    print(f"Overall Win Rate: {overall_win_rate:.1%} ({results['total_wins']}/{results['total_games']})")
    print(f"Total Time: {elapsed_time/60:.1f} minutes")
    print(f"{'='*70}\n")

    # Restore original epsilon and mode
    agent.epsilon = original_epsilon
    agent.set_train_mode()

    return results


def print_detailed_results(results):
    """Print detailed per-opponent results"""
    print("\nDetailed Results:")
    print("-"*70)
    print(f"{'Opponent':<20} {'Win Rate':<12} {'Wins':<6} {'Losses':<6}")
    print("-"*70)

    for i, name in enumerate(results['opponent_names']):
        win_rate = results['win_rates'][i]
        wins = results['wins'][i]
        losses = results['losses'][i]
        print(f"{name:<20} {win_rate:>6.1%}      {wins:>6}  {losses:>6}")

    print("-"*70)
    overall_wr = results['total_wins'] / results['total_games']
    print(f"{'OVERALL':<20} {overall_wr:>6.1%}      {results['total_wins']:>6}  {results['total_games'] - results['total_wins']:>6}")
    print("-"*70)


def main():
    """Main evaluation function"""
    parser = argparse.ArgumentParser(description='Evaluate RL Poker Agent')
    parser.add_argument('--model', type=str, default='rl_implementation/checkpoints/final_model.pt',
                        help='Path to trained model checkpoint')
    parser.add_argument('--games', type=int, default=EVAL_GAMES_PER_OPPONENT,
                        help='Games per opponent')
    parser.add_argument('--epsilon', type=float, default=EVAL_EPSILON,
                        help='Exploration rate (0 for greedy)')
    parser.add_argument('--detailed', action='store_true',
                        help='Print detailed per-opponent results')

    args = parser.parse_args()

    # Load agent
    print(f"Loading model from: {args.model}")
    agent = DQNAgent()

    if os.path.exists(args.model):
        agent.load(args.model)
        print(f"✓ Model loaded successfully")
    else:
        print(f"❌ Model not found: {args.model}")
        print("Please train a model first using train_rl_agent.py")
        return

    # Determine opponents
    if use_training_opponents and len(training_opponents) > 0:
        print(f"Using {len(training_opponents)} training opponents\n")
        opponents = training_opponents
    else:
        print("Using basic opponents for demonstration\n")
        opponents = [John1, AllIn]

    # Evaluate
    results = evaluate_agent(agent, opponents,
                             games_per_opponent=args.games,
                             epsilon=args.epsilon)

    # Print detailed results if requested
    if args.detailed:
        print_detailed_results(results)

    # Save results
    import json
    results_path = os.path.join(SAVE_DIR, 'evaluation_results.json')
    with open(results_path, 'w') as f:
        serializable_results = {
            'overall_win_rate': results['total_wins'] / results['total_games'],
            'total_wins': results['total_wins'],
            'total_games': results['total_games'],
            'win_rates': results['win_rates'],
            'opponent_names': results['opponent_names'],
            'wins': results['wins'],
            'losses': results['losses']
        }
        json.dump(serializable_results, f, indent=2)
    print(f"\nResults saved: {results_path}")


if __name__ == '__main__':
    main()
