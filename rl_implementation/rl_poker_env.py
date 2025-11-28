"""
RL Poker Environment: Gym-like interface for poker game
Wraps the poker game to provide standard RL interface
"""

import sys
import os
import random
import numpy as np

# Add parent directory to path to import from Assignment3_Class
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Assignment3_Class'))

from opponent_tracker import OpponentTracker
from utils import (normalize_state, get_valid_actions_mask, action_to_bet,
                   compute_reward)
from config import *


class PokerEnv:
    """
    Poker environment for RL training
    Provides gym-like interface: reset(), step(action)
    """

    def __init__(self, opponent_class, rng_seed=None, verbose=False):
        """
        Args:
            opponent_class: Class of opponent to play against
            rng_seed: Random seed for reproducibility
            verbose: Whether to print game details
        """
        self.opponent_class = opponent_class
        self.opponent = None
        self.verbose = verbose

        # RNG
        if rng_seed is not None:
            self.rng = random.Random(rng_seed)
        else:
            self.rng = random.Random()

        # Game state
        self.our_score = INITIAL_POINTS
        self.opp_score = INITIAL_POINTS
        self.minbet = 1.0
        self.hand_count = 0
        self.we_are_sb = False  # Small blind flag

        # Current hand state
        self.our_card = None
        self.opp_card = None
        self.pot = 0
        self.our_current_bet = 0
        self.opp_current_bet = 0
        self.initial_minbet = 1.0

        # Opponent tracking
        self.tracker = OpponentTracker()

        # Episode info
        self.done = False
        self.total_reward = 0.0

        # Hand tracking for context features
        self.first_action = True
        self.we_checked = False
        self.opp_raised = False

    def reset(self):
        """
        Start a new game against the opponent

        Returns:
            state: Initial state for first hand
        """
        # Reset game state
        self.opponent = self.opponent_class()
        self.our_score = INITIAL_POINTS
        self.opp_score = INITIAL_POINTS
        self.minbet = 1.0
        self.initial_minbet = 1.0
        self.hand_count = 0
        self.we_are_sb = self.rng.random() < 0.5

        # Reset opponent tracker
        self.tracker.reset()

        # Reset episode info
        self.done = False
        self.total_reward = 0.0

        # Start first hand
        state = self._start_new_hand()

        return state

    def _start_new_hand(self):
        """
        Start a new hand and return initial state

        Returns:
            state: State vector for this hand
        """
        # Deal cards
        self.our_card = self.rng.random()
        self.opp_card = self.rng.random()

        # Initialize pot with blinds
        if self.we_are_sb:
            self.our_current_bet = min(self.minbet, min(self.our_score, self.opp_score))
            self.opp_current_bet = min(2 * self.minbet, min(self.our_score, self.opp_score))
        else:
            self.our_current_bet = min(2 * self.minbet, min(self.our_score, self.opp_score))
            self.opp_current_bet = min(self.minbet, min(self.our_score, self.opp_score))

        self.pot = self.our_current_bet + self.opp_current_bet

        # Call player start methods
        if self.we_are_sb:
            self.opponent.start(True, self.opp_card, self.opp_score, self.our_score,
                                self.minbet, self.minbet)
        else:
            self.opponent.start(False, self.opp_card, self.opp_score, self.our_score,
                                self.minbet, 0)

        # Reset hand context
        self.first_action = True
        self.we_checked = False
        self.opp_raised = False

        # Get current state
        state = self._get_state()

        return state

    def _get_state(self):
        """
        Get current state vector

        Returns:
            state: Normalized state vector of shape (19,)
        """
        # Get opponent features
        opp_features = self.tracker.get_features()

        # Normalize state
        state = normalize_state(
            card=self.our_card,
            myscore=self.our_score,
            oppscore=self.opp_score,
            pot=self.pot,
            minbet=self.minbet,
            role=(0 if self.we_are_sb else 1),
            opponent_features=opp_features,
            first_action=self.first_action,
            we_checked=self.we_checked,
            opp_raised=self.opp_raised,
            initial_minbet=self.initial_minbet
        )

        return state

    def get_valid_actions_mask(self):
        """
        Get mask of valid actions in current state

        Returns:
            valid_mask: Boolean array of shape (7,)
        """
        return get_valid_actions_mask(
            pot=self.pot,
            minbet=self.minbet,
            myscore=self.our_score,
            oppscore=self.opp_score,
            bigblind=(not self.we_are_sb),
            role=(0 if self.we_are_sb else 1)
        )

    def step(self, action):
        """
        Execute action and advance game state

        Args:
            action: Action index (0-6)

        Returns:
            next_state: Next state vector
            reward: Immediate reward
            done: Whether game is over
            info: Additional information
        """
        # Convert action to bet
        our_bet = action_to_bet(
            action=action,
            pot=self.pot,
            minbet=self.minbet,
            myscore=self.our_score,
            oppscore=self.opp_score,
            role=(0 if self.we_are_sb else 1)
        )

        # Update hand context
        if our_bet == self.pot and not self.first_action:
            self.we_checked = True
        self.first_action = False

        # Get opponent's response
        opp_bet = self.opponent.bet(self.opp_card, self.opp_score, self.our_score,
                                     self.minbet, our_bet)

        # Track opponent's action
        if opp_bet > our_bet:
            self.opp_raised = True

        # Determine hand outcome
        hand_done, hand_reward, hand_info = self._resolve_hand(our_bet, opp_bet)

        # Update opponent tracker
        self._update_tracker(our_bet, opp_bet, hand_done, hand_info)

        # Update game state
        self.total_reward += hand_reward

        # Check if game is over
        if self.our_score <= 0 or self.opp_score <= 0:
            self.done = True
            next_state = self._get_state()
            info = {
                'won': (self.our_score > 0),
                'final_score': self.our_score,
                'total_reward': self.total_reward,
                'hands_played': self.hand_count
            }
            return next_state, hand_reward, True, info

        # Start next hand
        self.hand_count += 1

        # Update minbet every 100 hands
        if self.hand_count % 100 == 0:
            self.minbet *= 2

        # Switch blinds
        self.we_are_sb = not self.we_are_sb

        # Get next state
        next_state = self._start_new_hand()

        info = {
            'won': hand_info['we_won'],
            'hand_reward': hand_reward,
            'hands_played': self.hand_count
        }

        return next_state, hand_reward, False, info

    def _resolve_hand(self, our_bet, opp_bet):
        """
        Resolve hand outcome based on bets

        Args:
            our_bet: Our bet amount
            opp_bet: Opponent's bet amount

        Returns:
            done: Whether hand is over
            reward: Reward for this hand
            info: Additional info dict
        """
        minscore = min(self.our_score, self.opp_score)
        opp_bet = min(opp_bet, minscore)

        our_score_before = self.our_score
        opp_score_before = self.opp_score

        we_folded = (our_bet < self.pot)
        opp_folded = (opp_bet < our_bet)

        # Determine winner and pot
        if we_folded:
            # We folded, opponent wins
            pot_final = self.our_current_bet + self.opp_current_bet
            self.our_score -= pot_final
            self.opp_score += pot_final
            we_won = False
            oppcard_revealed = None
            winnings = pot_final
        elif opp_folded:
            # Opponent folded, we win
            pot_final = our_bet
            self.our_score += pot_final
            self.opp_score -= pot_final
            we_won = True
            oppcard_revealed = None
            winnings = pot_final
        else:
            # Showdown
            pot_final = opp_bet
            if self.our_card > self.opp_card:
                # We win
                self.our_score += pot_final
                self.opp_score -= pot_final
                we_won = True
            else:
                # Opponent wins
                self.our_score -= pot_final
                self.opp_score += pot_final
                we_won = False
            oppcard_revealed = self.opp_card
            winnings = pot_final

        # Call player end methods
        if we_won:
            self.opponent.end(False, self.our_card, self.opp_score, self.our_score,
                              self.minbet, winnings)
        else:
            self.opponent.end(True, self.our_card if oppcard_revealed is None else oppcard_revealed,
                              self.opp_score, self.our_score, self.minbet, winnings)

        # Compute reward
        reward = compute_reward(
            iwon=we_won,
            winnings=winnings,
            myscore_before=our_score_before,
            oppscore_before=opp_score_before,
            my_card=self.our_card,
            i_folded=we_folded,
            opp_folded=opp_folded
        )

        info = {
            'we_won': we_won,
            'we_folded': we_folded,
            'opp_folded': opp_folded,
            'oppcard_revealed': oppcard_revealed,
            'our_bet': our_bet,
            'opp_bet': opp_bet,
            'winnings': winnings
        }

        return True, reward, info

    def _update_tracker(self, our_bet, opp_bet, hand_done, hand_info):
        """Update opponent tracker with hand results"""
        we_won = hand_info['we_won']
        opp_folded = hand_info['opp_folded']
        oppcard_revealed = hand_info['oppcard_revealed']

        # Track opponent's response to our bet
        if our_bet > self.pot:  # We raised
            if opp_folded:
                self.tracker.update_bet_response('fold', opp_bet, our_bet,
                                                 self.minbet, self.opp_score)
            elif opp_bet == our_bet:
                self.tracker.update_bet_response('call', opp_bet, our_bet,
                                                 self.minbet, self.opp_score)
            elif opp_bet > our_bet:
                self.tracker.update_bet_response('raise', opp_bet, our_bet,
                                                 self.minbet, self.opp_score)

        # Track opponent betting when we checked
        if self.we_checked:
            self.tracker.update_check_response(opp_bet, our_bet, self.minbet)

        # Track showdowns
        if oppcard_revealed is not None:
            opp_bet_this_hand = (opp_bet > self.pot)
            self.tracker.update_showdown(oppcard_revealed, opp_bet_this_hand, opp_bet)

        # Update hand count
        self.tracker.update_hand_end()

    def render(self):
        """Print current game state (for debugging)"""
        print(f"\n=== Hand {self.hand_count} ===")
        print(f"Scores: Us={self.our_score:.1f}, Opp={self.opp_score:.1f}")
        print(f"Cards: Us={self.our_card:.3f}, Opp={self.opp_card:.3f}")
        print(f"Pot={self.pot:.1f}, Minbet={self.minbet:.1f}")
        print(f"Role: {'SmallBlind' if self.we_are_sb else 'BigBlind'}")
        print(f"Opponent: {self.tracker}")
