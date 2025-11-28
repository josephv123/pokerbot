"""
Utility functions for RL Poker Player
"""

import numpy as np
import math
from config import *


def get_valid_actions_mask(pot, minbet, myscore, oppscore, bigblind, role):
    """
    Determine which actions are valid in current situation

    Args:
        pot: Current pot size
        minbet: Minimum bet size
        myscore: Our score
        oppscore: Opponent's score
        bigblind: Whether we are big blind (True/False)
        role: 0 for small blind, 1 for big blind

    Returns:
        valid_mask: Boolean array of shape (7,) indicating valid actions
    """
    valid_mask = np.ones(ACTION_DIM, dtype=bool)

    # Maximum we can bet is the minimum of our score and opponent's score
    max_bet = min(myscore, oppscore)

    # Action 0: FOLD - always valid unless we can check
    # If we're big blind and pot == 2, we can check instead
    if role == 1 and pot == 2:
        valid_mask[ACTION_FOLD] = False  # Don't fold when we can check for free

    # Action 1: CALL - always valid (equals pot)
    # No special conditions

    # Action 2: MIN_RAISE (pot + minbet)
    if pot + minbet > max_bet:
        valid_mask[ACTION_MIN_RAISE] = False

    # Action 3: SMALL_RAISE (pot + 2*minbet)
    if pot + 2 * minbet > max_bet:
        valid_mask[ACTION_SMALL_RAISE] = False

    # Action 4: MED_RAISE (pot + 3*minbet)
    if pot + 3 * minbet > max_bet:
        valid_mask[ACTION_MED_RAISE] = False

    # Action 5: POT_RAISE (pot + pot)
    pot_size = pot - (1 if role == 0 else 2)  # Subtract our blind
    if pot + pot_size > max_bet:
        valid_mask[ACTION_POT_RAISE] = False

    # Action 6: ALLIN - always valid
    # No special conditions

    return valid_mask


def action_to_bet(action, pot, minbet, myscore, oppscore, role):
    """
    Convert action index to bet amount

    Args:
        action: Action index (0-6)
        pot: Current pot size
        minbet: Minimum bet size
        myscore: Our score
        oppscore: Opponent's score
        role: 0 for small blind, 1 for big blind

    Returns:
        bet: Amount to bet (total, not incremental)
    """
    max_bet = min(myscore, oppscore)

    if action == ACTION_FOLD:
        return 0
    elif action == ACTION_CALL:
        return pot
    elif action == ACTION_MIN_RAISE:
        return min(pot + minbet, max_bet)
    elif action == ACTION_SMALL_RAISE:
        return min(pot + 2 * minbet, max_bet)
    elif action == ACTION_MED_RAISE:
        return min(pot + 3 * minbet, max_bet)
    elif action == ACTION_POT_RAISE:
        pot_size = pot - (1 if role == 0 else 2)  # Subtract our blind
        return min(pot + pot_size, max_bet)
    elif action == ACTION_ALLIN:
        return max_bet
    else:
        raise ValueError(f"Invalid action: {action}")


def normalize_state(card, myscore, oppscore, pot, minbet, role,
                     opponent_features, first_action, we_checked, opp_raised,
                     initial_minbet=1):
    """
    Create normalized state vector from raw game state

    Args:
        card: Our card value [0, 1]
        myscore: Our score
        oppscore: Opponent's score
        pot: Current pot
        minbet: Minimum bet
        role: 0 for SB, 1 for BB
        opponent_features: 10-dim opponent feature vector
        first_action: Whether it's our first action this hand
        we_checked: Whether we checked to opponent
        opp_raised: Whether opponent raised this hand
        initial_minbet: Initial minimum bet (default 1)

    Returns:
        state: Normalized state vector of shape (19,)
    """
    # Hand state (6 features)
    card_strength = float(card)
    myscore_norm = myscore / TOTAL_POINTS
    oppscore_norm = oppscore / TOTAL_POINTS
    total_score = myscore + oppscore
    pot_norm = pot / total_score if total_score > 0 else 0.0
    minbet_level = math.log2(minbet / initial_minbet) if minbet > 0 else 0.0
    role_binary = float(role)

    hand_state = np.array([
        card_strength,
        myscore_norm,
        oppscore_norm,
        pot_norm,
        minbet_level,
        role_binary
    ], dtype=np.float32)

    # Opponent features (10 features) - already normalized
    opp_features = np.array(opponent_features, dtype=np.float32)

    # Hand context (3 features)
    context = np.array([
        float(first_action),
        float(we_checked),
        float(opp_raised)
    ], dtype=np.float32)

    # Concatenate all features
    state = np.concatenate([hand_state, opp_features, context])

    return state


def compute_reward(iwon, winnings, myscore_before, oppscore_before,
                    my_card=None, i_folded=False, opp_folded=False):
    """
    Compute reward for a completed hand

    Args:
        iwon: Whether we won
        winnings: Amount won/lost
        myscore_before: Our score before hand
        oppscore_before: Opponent's score before hand
        my_card: Our card (for intermediate rewards)
        i_folded: Whether we folded
        opp_folded: Whether opponent folded

    Returns:
        reward: Scalar reward
    """
    # Primary terminal reward (scaled by pot size)
    total_score = myscore_before + oppscore_before
    if iwon:
        reward = REWARD_WIN_SCALE * (winnings / total_score)
    else:
        reward = -REWARD_LOSS_SCALE * (winnings / total_score)

    # Optional intermediate rewards (disabled by default in config)
    if REWARD_BLUFF_SUCCESS > 0 and opp_folded and my_card is not None and my_card < 0.5:
        reward += REWARD_BLUFF_SUCCESS

    if REWARD_BAD_FOLD_PENALTY > 0 and i_folded and my_card is not None and my_card > 0.7:
        reward -= REWARD_BAD_FOLD_PENALTY

    return reward


def print_action(action, bet, pot, minbet):
    """Pretty print action for debugging"""
    action_name = ACTION_NAMES[action]
    return f"{action_name} (bet={bet}, pot={pot}, minbet={minbet})"


class Logger:
    """Simple logger for tracking training progress"""

    def __init__(self, log_file=None):
        self.log_file = log_file
        self.metrics = {
            'episodes': [],
            'wins': [],
            'losses': [],
            'epsilon': [],
            'avg_reward': []
        }

    def log(self, message, to_file=True, to_console=True):
        """Log a message"""
        if to_console:
            print(message)
        if to_file and self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(message + '\n')

    def record(self, episode, win, loss, epsilon, avg_reward):
        """Record metrics for an episode"""
        self.metrics['episodes'].append(episode)
        self.metrics['wins'].append(win)
        self.metrics['losses'].append(loss)
        self.metrics['epsilon'].append(epsilon)
        self.metrics['avg_reward'].append(avg_reward)

    def get_win_rate(self, last_n=None):
        """Get win rate over last N episodes"""
        if last_n is None:
            wins = self.metrics['wins']
        else:
            wins = self.metrics['wins'][-last_n:]

        if len(wins) == 0:
            return 0.0
        return sum(wins) / len(wins)


def estimate_training_time(num_opponents, games_per_opponent, num_epochs,
                            seconds_per_game=2.0):
    """
    Estimate total training time

    Args:
        num_opponents: Number of opponents
        games_per_opponent: Games per opponent
        num_epochs: Number of training epochs
        seconds_per_game: Average seconds per game

    Returns:
        Formatted time string
    """
    total_games = num_opponents * games_per_opponent * num_epochs
    total_seconds = total_games * seconds_per_game

    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)

    return f"{hours}h {minutes}m ({total_games} total games)"
