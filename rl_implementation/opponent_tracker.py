"""
OpponentTracker: Extracts behavioral features about opponents
Tracks statistics during gameplay to enable opponent modeling
"""

from collections import deque
import numpy as np


class OpponentTracker:
    """
    Tracks opponent behavior and computes 10 feature dimensions:
    1. fold_rate: How often opponent folds to our bets
    2. call_rate: How often opponent calls our bets
    3. raise_rate: How often opponent raises our bets
    4. aggression: How often opponent bets when we check
    5. bet_card_mean: Average card value when opponent bets (from showdowns)
    6. bet_card_confidence: Confidence in bet_card_mean (based on sample size)
    7. allin_frequency: How often opponent goes all-in
    8. hands_played_norm: Normalized hands played (game phase indicator)
    9. recent_fold_rate: Fold rate over last 20 decisions (for drift detection)
    10. drift_magnitude: |recent_fold_rate - early_fold_rate|
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all statistics for a new opponent/game"""
        # Response to our bets
        self.our_bet_count = 0
        self.our_bet_gets_fold = 0
        self.our_bet_gets_call = 0
        self.our_bet_gets_raise = 0

        # Opponent aggression
        self.we_checked_to_opp = 0
        self.opp_bet_when_checked = 0

        # Opponent betting range (from showdowns)
        self.opp_bet_card_sum = 0.0
        self.opp_bet_card_count = 0

        # All-in tracking
        self.opp_allin_count = 0
        self.total_opp_actions = 0

        # Game tracking
        self.hands_played = 0

        # Drift detection (last 20 fold decisions)
        self.recent_fold_decisions = deque(maxlen=20)
        self.early_fold_rate = None  # Set after 15 observations

        # Cache for features (avoid recomputation)
        self._feature_cache = None
        self._cache_valid = False

    def update_bet_response(self, opponent_action, opponent_bet, pot_before, minbet, oppscore):
        """
        Called when opponent responds to our bet

        Args:
            opponent_action: 'fold', 'call', or 'raise'
            opponent_bet: Amount opponent bet
            pot_before: Pot size before opponent's action
            minbet: Minimum bet
            oppscore: Opponent's score
        """
        self.our_bet_count += 1
        self.total_opp_actions += 1

        if opponent_action == 'fold':
            self.our_bet_gets_fold += 1
            self.recent_fold_decisions.append(1)
        elif opponent_action == 'call':
            self.our_bet_gets_call += 1
            self.recent_fold_decisions.append(0)
        elif opponent_action == 'raise':
            self.our_bet_gets_raise += 1
            self.recent_fold_decisions.append(0)

        # Check if all-in
        if opponent_bet >= oppscore:
            self.opp_allin_count += 1

        # Set early fold rate after 15 observations
        if self.early_fold_rate is None and self.our_bet_count >= 15:
            self.early_fold_rate = self.our_bet_gets_fold / self.our_bet_count

        self._cache_valid = False

    def update_check_response(self, opponent_bet, pot_before, minbet):
        """
        Called when opponent acts after we checked

        Args:
            opponent_bet: Amount opponent bet (pot_before means check, >pot_before means bet)
            pot_before: Pot size before opponent's action
            minbet: Minimum bet
        """
        self.we_checked_to_opp += 1
        self.total_opp_actions += 1

        # If opponent bet is greater than pot, they raised
        if opponent_bet > pot_before:
            self.opp_bet_when_checked += 1

        self._cache_valid = False

    def update_showdown(self, opponent_card, opponent_bet, pot):
        """
        Called at showdown when we see opponent's card

        Args:
            opponent_card: Opponent's card value [0, 1]
            opponent_bet: Whether opponent bet this hand (True/False)
            pot: Final pot size
        """
        # Only track if opponent bet (to estimate their betting range)
        if opponent_bet:
            self.opp_bet_card_sum += opponent_card
            self.opp_bet_card_count += 1

        self._cache_valid = False

    def update_hand_end(self):
        """Called at the end of each hand"""
        self.hands_played += 1
        self._cache_valid = False

    def get_features(self):
        """
        Returns 10-dimensional opponent feature vector
        All features normalized to [0, 1]

        Returns:
            np.array of shape (10,)
        """
        if self._cache_valid:
            return self._feature_cache

        # 1. Fold rate
        if self.our_bet_count > 0:
            fold_rate = self.our_bet_gets_fold / self.our_bet_count
        else:
            fold_rate = 0.5  # Neutral prior

        # 2. Call rate
        if self.our_bet_count > 0:
            call_rate = self.our_bet_gets_call / self.our_bet_count
        else:
            call_rate = 0.3  # Neutral prior

        # 3. Raise rate
        if self.our_bet_count > 0:
            raise_rate = self.our_bet_gets_raise / self.our_bet_count
        else:
            raise_rate = 0.2  # Neutral prior

        # 4. Aggression (bets when checked to)
        if self.we_checked_to_opp > 0:
            aggression = self.opp_bet_when_checked / self.we_checked_to_opp
        else:
            aggression = 0.3  # Neutral prior

        # 5. Bet card mean (average card when opponent bets)
        if self.opp_bet_card_count > 0:
            bet_card_mean = self.opp_bet_card_sum / self.opp_bet_card_count
        else:
            bet_card_mean = 0.5  # Neutral prior

        # 6. Bet card confidence (how many showdowns we've seen)
        bet_card_confidence = min(self.opp_bet_card_count / 10.0, 1.0)

        # 7. All-in frequency
        if self.total_opp_actions > 0:
            allin_frequency = self.opp_allin_count / self.total_opp_actions
        else:
            allin_frequency = 0.0

        # 8. Hands played normalized (game phase indicator)
        # Typical game is 50-200 hands, normalize by 200
        hands_played_norm = min(self.hands_played / 200.0, 1.0)

        # 9. Recent fold rate (last 20 decisions)
        if len(self.recent_fold_decisions) > 0:
            recent_fold_rate = sum(self.recent_fold_decisions) / len(self.recent_fold_decisions)
        else:
            recent_fold_rate = fold_rate

        # 10. Drift magnitude (adaptation detection)
        if self.early_fold_rate is not None:
            drift_magnitude = abs(recent_fold_rate - self.early_fold_rate)
        else:
            drift_magnitude = 0.0

        features = np.array([
            fold_rate,
            call_rate,
            raise_rate,
            aggression,
            bet_card_mean,
            bet_card_confidence,
            allin_frequency,
            hands_played_norm,
            recent_fold_rate,
            drift_magnitude
        ], dtype=np.float32)

        # Cache the result
        self._feature_cache = features
        self._cache_valid = True

        return features

    def get_classification(self):
        """
        Optional: Get opponent type classification for debugging
        Returns string describing opponent type
        """
        features = self.get_features()
        fold_rate = features[0]
        raise_rate = features[2]
        aggression = features[3]
        allin_freq = features[6]

        # Need sufficient observations
        if self.our_bet_count < 15:
            return "insufficient_data"

        # Classify based on same logic as current bot
        if allin_freq > 0.3:
            return "allin"
        elif fold_rate > 0.85 and aggression > 0.4:
            return "aggressive_folder"
        elif fold_rate > 0.55:
            return "folder"
        elif fold_rate < 0.30:
            return "caller"
        elif raise_rate > 0.30:
            return "aggressor"
        else:
            return "balanced"

    def __repr__(self):
        features = self.get_features()
        classification = self.get_classification()
        return (f"OpponentTracker(hands={self.hands_played}, "
                f"fold={features[0]:.2f}, call={features[1]:.2f}, "
                f"raise={features[2]:.2f}, agg={features[3]:.2f}, "
                f"type={classification})")
