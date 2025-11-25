import random

class PokerPlayer:
    def __init__(self):
        """Initialize my internal variables."""
        self.role = None  # 'SB' or 'BB'
        self.hand_strength = None
        self.minbet = None
        self.pot = None
        self.myscore = None
        self.oppscore = None
        self.epsilon = 1e-9  # For floating point comparisons
        
        # Track betting for correct B/P ratio in multi-raise scenarios
        self.my_contribution = 0  # What we've put in this hand
        self.last_pot_seen = 0    # Last pot level we saw
        
        # Opponent action tracking
        self.hands_played = 0
        self.opp_bet_count = 0      # Times opponent bet/raised
        self.opp_check_count = 0    # Times opponent checked
        self.opp_fold_count = 0     # Times opponent folded
        self.opp_call_count = 0     # Times opponent called our bet
        self.consecutive_folds = 0  # For boredom detection
        
        # Opponent classification
        self.opp_type = None  # None, 'allin', 'folder', 'caller', 'aggressor', 'balanced'
        self.opp_allin_count = 0  # Times opponent went all-in or near
        
        # Strategy mode: 'aggressive', 'balanced', 'tight', 'trapping'
        self.strategy_mode = 'aggressive'  # Default to aggressive strategy
        
        # Early detection thresholds
        self.early_detection_threshold = 15  # Minimum bets to classify
        self.early_allin_threshold = 30
        self.allin_detection_ratio = 0.70  # >70% all-in = allin player
        
        # Opponent classification thresholds
        self.folder_threshold = 0.55     # >55% fold rate = folder
        self.caller_threshold = 0.30     # <30% fold rate = caller
        self.aggressor_raise_threshold = 0.30  # >30% raise rate = aggressor
        
        # Adaptation detection
        self.recent_fold_decisions = []  # Last 40: 1=fold, 0=not fold
        self.early_fold_rate = None      # Stored after first 30 hands
        self.adaptation_window = 20
        self.drift_threshold = 0.20  # Threshold for detecting behavioral shift
        
        # Showdown statistics for better opponent modeling
        self.opp_bet_card_sum = 0.0     # Sum of opponent cards when they bet
        self.opp_bet_card_count = 0     # Count of showdowns where opponent bet
        
        # Aggression tracking (bets when checked to)
        self.we_checked_to_opp = 0      # Times we checked to opponent
        self.opp_bet_when_checked = 0   # Times opponent bet when we checked
        
        # Track opponent response to OUR bets specifically
        self.our_bet_count = 0       # Times we bet/raised
        self.our_bet_gets_fold = 0   # Times opponent folded to our bet
        self.our_bet_gets_call = 0   # Times opponent called our bet
        self.our_bet_gets_raise = 0  # Times opponent raised our bet
        
    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        """
        Start a game of poker.

        bigblind  - True if I'm the big blind, False if I'm the small blind.
        card      - contains my card.
        myscore   - my score
        oppscore  - my opponent's score
        minbet    - the smallest bet increase that I am allowed make
        pot       - contains the current bid.
        """
        self.role = 'BB' if bigblind else 'SB'
        self.hand_strength = card
        self.minbet = minbet
        self.pot = pot
        self.myscore = myscore
        self.oppscore = oppscore
        
        # Store initial pot value for this hand
        self.initial_bb_pot = 2 * minbet  # Total after both blinds
        self.last_action = None  # Track our last action: 'bet', 'check', or None
        
        # Initialize contribution tracking for this hand
        if bigblind:
            self.my_contribution = 2 * minbet  # BB puts in 2*minbet
        else:
            self.my_contribution = minbet  # SB puts in minbet
        self.last_pot_seen = 2 * minbet  # Initial betPot is always 2*minbet
        
        # Track opponent's action this hand
        self.opp_bet_this_hand = False
        self.opp_raised_this_hand = False
        self.we_bet_this_hand = False
        self.we_checked_this_hand = False  # Track if we checked to opponent
        
    def _detect_opponent_type(self):
        """
        Detect opponent type based on their response patterns to our bets.
        Called after we have enough data (15+ bet responses).
        """
        if self.our_bet_count < self.early_detection_threshold:
            return None  # Not enough data
        
        fold_rate = self.our_bet_gets_fold / self.our_bet_count
        raise_rate = self.our_bet_gets_raise / self.our_bet_count
        
        # Classify opponent
        if raise_rate >= self.aggressor_raise_threshold:
            return 'aggressor'
        elif fold_rate >= self.folder_threshold:
            return 'folder'
        elif fold_rate <= self.caller_threshold:
            return 'caller'
        else:
            return 'balanced'
    
    def _get_strategy_params(self):
        """
        Get strategy parameters based on detected opponent type.
        Returns dict with bet_mult, bluff_mult, value_mult, call_mult.
        """
        if self.strategy_mode == 'aggressive':
            # For folders: large bets, aggressive bluffing
            return {'bet_mult': 5, 'bluff_mult': 2.5, 'value_mult': 1.10, 'call_mult': 1.15}
        elif self.strategy_mode == 'tight':
            # For callers: smaller bets, minimal bluffing, tighter value
            return {'bet_mult': 2, 'bluff_mult': 0.3, 'value_mult': 1.0, 'call_mult': 1.0}
        elif self.strategy_mode == 'trapping':
            # For aggressors: pot-sized, let them bet, call wider
            return {'bet_mult': 2, 'bluff_mult': 0.5, 'value_mult': 1.15, 'call_mult': 0.85}
        else:  # balanced
            # Standard GTO-ish: pot-sized, normal bluffs
            return {'bet_mult': 3, 'bluff_mult': 1.5, 'value_mult': 1.05, 'call_mult': 1.05}
    
    def _update_strategy_mode(self):
        """Update strategy mode based on opponent detection."""
        opp_type = self._detect_opponent_type()
        
        if opp_type is None:
            return  # Not enough data yet
        
        self.opp_type = opp_type
        
        # Check for adaptation - if opponent is changing, use balanced mode
        if self._check_for_adaptation() and self.strategy_mode != 'tight':
            self.strategy_mode = 'balanced'
            return
        
        # Map opponent type to strategy mode
        if opp_type == 'folder':
            self.strategy_mode = 'aggressive'
        elif opp_type == 'caller':
            self.strategy_mode = 'tight'
        elif opp_type == 'aggressor':
            self.strategy_mode = 'trapping'
        else:  # balanced
            self.strategy_mode = 'balanced'
    
    def _check_for_adaptation(self):
        """Detect if opponent is changing strategy mid-match."""
        if len(self.recent_fold_decisions) < self.adaptation_window or self.early_fold_rate is None:
            return False
        
        recent_rate = sum(self.recent_fold_decisions[-self.adaptation_window:]) / self.adaptation_window
        drift = abs(recent_rate - self.early_fold_rate)
        
        return drift > self.drift_threshold  # Significant behavioral shift detected
    
    def _store_early_baseline(self):
        """Store baseline behavior after first 30 hands for drift detection."""
        if self.hands_played == 30 and self.our_bet_count >= 8:
            self.early_fold_rate = self.our_bet_gets_fold / self.our_bet_count
    
    def _calculate_gto_thresholds(self, bet_size_ratio=1.0):
        """
        Calculate GTO thresholds based on bet size relative to pot.
        Adjusts based on detected opponent type and strategy mode.
        """
        B = 2.0 * bet_size_ratio
        P = 2.0
        
        # Get strategy parameters based on mode
        params = self._get_strategy_params()
        SB_BLUFF_MULT = params['bluff_mult']
        BB_BLUFF_MULT = params['bluff_mult']
        VALUE_MULT = params['value_mult']
        CALL_MULT = params['call_mult']
        
        # P1 (SB) thresholds
        a = B / ((B + 1) * (B + 4)) * SB_BLUFF_MULT  # Bluff threshold
        c = (B * (B + 3)) / ((B + 1) * (B + 4)) * VALUE_MULT  # Value threshold
        
        # Check-call range
        check_range = c - a
        mdf = P / (P + B)
        call_range = check_range * mdf
        b = (c - call_range) * CALL_MULT  # Adjusted call threshold
        
        # P2 (BB) thresholds
        d = B / (P + B) * CALL_MULT  # Call threshold
        e = 1.0 / (B + 4) * BB_BLUFF_MULT  # Bluff threshold
        f = (B + 2) / (B + 4) * VALUE_MULT  # Value threshold
        
        return (a, b, c, d, e, f)
    
    def _get_pot_sized_bet(self, current_pot, minbet):
        """
        Calculate bet that is a valid multiple of minbet.
        Bet size varies based on strategy mode.
        """
        params = self._get_strategy_params()
        bet_mult = params['bet_mult']
        
        target_bet = current_pot * bet_mult
        bet = int(target_bet / minbet) * minbet
        return max(bet, current_pot + minbet)
    
    def _round_to_minbet(self, amount, minbet):
        """Round amount down to nearest valid multiple of minbet."""
        return int(amount / minbet) * minbet
    
    def _get_bet_size_ratio(self, pot):
        """
        Calculate correct B/P ratio for threshold calculation.
        Handles multi-raise scenarios properly.
        """
        if pot <= self.last_pot_seen + self.epsilon:
            # No raise occurred, use default pot-sized ratio
            return 1.0
        
        # Calculate the raise amount
        raise_amount = pot - self.last_pot_seen
        
        # The "pot" for ratio calculation is what was in before this raise
        effective_pot = self.last_pot_seen + self.my_contribution
        
        if effective_pot > self.epsilon:
            return raise_amount / effective_pot
        else:
            return 1.0
    
    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds.

        card     - my card
        myscore  - my score
        oppscore - my opponent's score
        minbet   - the smallest bet increase that I am allowed make
        pot      - contains the current bid.
        """
        self.hand_strength = card
        self.myscore = myscore
        self.oppscore = oppscore
        self.minbet = minbet
        self.pot = pot
        
        # Update strategy mode based on opponent detection
        self._update_strategy_mode()
        
        # Calculate correct bet size ratio
        bet_size_ratio = self._get_bet_size_ratio(pot)
        
        # Get GTO thresholds (adjusted for strategy mode)
        a, b, c, d, e, f = self._calculate_gto_thresholds(bet_size_ratio)
        
        # Apply exploitative adjustments
        a, b, c, d, e, f = self._apply_selective_exploitation(a, b, c, d, e, f)
        
        max_bet = min(myscore, oppscore)
        
        # Use epsilon comparison for floating point pot values
        def pot_equals(p1, p2):
            return abs(p1 - p2) < self.epsilon
        
        if self.role == 'SB':
            return self._bet_as_sb(pot, a, b, c, max_bet, minbet, pot_equals)
        else:
            return self._bet_as_bb(pot, d, e, f, max_bet, minbet, pot_equals)
    
    def _apply_selective_exploitation(self, a, b, c, d, e, f):
        """
        Selective exploitation based on opponent patterns.
        """
        # AllIn detection - if opponent frequently goes all-in, play tight
        if self.opp_bet_count >= 5:
            allin_freq = self.opp_allin_count / self.opp_bet_count
            if allin_freq > 0.70:
                return (0, 0.5, 1.0, 0.5, 0, 1.0)
        
        # Adjust calling threshold based on opponent's betting range
        if self.opp_bet_card_count >= 10:
            bet_card_mean = self.opp_bet_card_sum / self.opp_bet_card_count
            if bet_card_mean < 0.55:
                # Opponent bets with weak hands - widen calling range
                d = d * 0.90  # Call 10% more as BB
                b = b * 0.90  # Call 10% more as SB
            elif bet_card_mean > 0.75:
                # Opponent only bets strong hands - tighten calling range
                d = d * 1.10  # Call 10% less as BB
                b = b * 1.10  # Call 10% less as SB
        
        return (a, b, c, d, e, f)
    
    def _bet_as_sb(self, pot, a, b, c, max_bet, minbet, pot_equals):
        """Handle betting logic when we are Small Blind (act first)."""
        if self.last_action is None:
            # Opening action: can call (2*minbet) or raise
            if self.hand_strength < a:
                # Bluff: raise with pot-sized bet
                bet = self._get_pot_sized_bet(pot, minbet)
                bet = min(bet, max_bet)
                bet = self._round_to_minbet(bet, minbet)
                bet = max(bet, pot + minbet)
                self.last_action = 'bet'
                self.my_contribution = bet
                self.we_bet_this_hand = True
                return bet
            elif self.hand_strength >= c:
                # Value bet: raise with pot-sized bet
                bet = self._get_pot_sized_bet(pot, minbet)
                bet = min(bet, max_bet)
                bet = self._round_to_minbet(bet, minbet)
                bet = max(bet, pot + minbet)
                self.last_action = 'bet'
                self.my_contribution = bet
                self.we_bet_this_hand = True
                return bet
            else:
                # Check (call): match the big blind
                self.last_action = 'check'
                self.we_checked_this_hand = True
                self.we_checked_to_opp += 1  # Track for aggression metric
                self.my_contribution = self.initial_bb_pot
                return self.initial_bb_pot
        else:
            # Called again - either we bet and opp raised, or we checked and opp bet
            self.last_pot_seen = pot  # Update for next calculation
            
            if self.last_action == 'check':
                # Facing a bet from BB after we checked
                self.opp_bet_this_hand = True
                self.opp_bet_when_checked += 1  # Track for aggression metric
                # Decision: call or fold based on check-call threshold (b)
                if self.hand_strength >= b:
                    self.my_contribution = pot
                    return pot  # Call
                else:
                    return 0  # Fold
            else:
                # We bet and opponent raised
                self.opp_raised_this_hand = True
                # Check for all-in
                if pot >= max_bet - self.epsilon:
                    self.opp_allin_count += 1
                # Call if we have a strong hand
                if self.hand_strength >= c:
                    self.my_contribution = pot
                    return pot
                else:
                    return 0  # Fold
                    
    def _bet_as_bb(self, pot, d, e, f, max_bet, minbet, pot_equals):
        """Handle betting logic when we are Big Blind (act second)."""
        if pot_equals(pot, self.initial_bb_pot):
            # SB called (checked), we can check back or bet
            if self.hand_strength < e:
                # Bluff: bet
                bet = self._get_pot_sized_bet(pot, minbet)
                bet = min(bet, max_bet)
                bet = self._round_to_minbet(bet, minbet)
                bet = max(bet, pot + minbet)
                self.last_action = 'bet'
                self.my_contribution = bet
                self.we_bet_this_hand = True
                return bet
            elif self.hand_strength >= f:
                # Value bet: bet
                bet = self._get_pot_sized_bet(pot, minbet)
                bet = min(bet, max_bet)
                bet = self._round_to_minbet(bet, minbet)
                bet = max(bet, pot + minbet)
                self.last_action = 'bet'
                self.my_contribution = bet
                self.we_bet_this_hand = True
                return bet
            else:
                # Check back: end the hand
                self.last_action = 'check'
                return pot
        else:
            # Facing a raise from SB
            self.opp_bet_this_hand = True
            # Check for all-in
            if pot >= max_bet - self.epsilon:
                self.opp_allin_count += 1
            # Decision: call or fold based on MDF threshold (d)
            if self.hand_strength >= d:
                self.my_contribution = pot
                return pot  # Call
            else:
                return 0  # Fold

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        """
        The game is over. Who won? How much did they win?

        iwon     - True if I won, False if I lost.
        oppcard  - contains my opponent's card unless someone
                   folded. In that case, it contains None.
        myscore  - my new score after the win/loss
        oppscore - my opponent's score after the win/loss
        minbet   - the smallest bet increase that I am allowed make
        winnings - how many points were won by the winner
        """
        self.myscore = myscore
        self.oppscore = oppscore
        self.hands_played += 1
        
        # Track opponent actions
        if oppcard is None:
            # Someone folded
            if iwon:
                # Opponent folded
                self.opp_fold_count += 1
                self.consecutive_folds += 1
                
                # Track response to our bet
                if self.we_bet_this_hand:
                    self.our_bet_count += 1
                    self.our_bet_gets_fold += 1
                    # Track in rolling window for adaptation detection
                    self.recent_fold_decisions.append(1)
                    if len(self.recent_fold_decisions) > self.adaptation_window * 2:
                        self.recent_fold_decisions.pop(0)
            else:
                # We folded - opponent bet/raised
                self.consecutive_folds = 0
                if self.opp_bet_this_hand or self.opp_raised_this_hand:
                    self.opp_bet_count += 1
        else:
            # Showdown occurred
            self.consecutive_folds = 0
            
            # Track opponent's action
            if self.opp_bet_this_hand or self.opp_raised_this_hand:
                self.opp_bet_count += 1
                # They raised our bet
                if self.we_bet_this_hand:
                    self.our_bet_count += 1
                    self.our_bet_gets_raise += 1
                    # Track in rolling window for adaptation detection
                    self.recent_fold_decisions.append(0)
                    if len(self.recent_fold_decisions) > self.adaptation_window * 2:
                        self.recent_fold_decisions.pop(0)
                # Track showdown stats for opponent betting range
                self.opp_bet_card_sum += oppcard
                self.opp_bet_card_count += 1
            elif self.we_bet_this_hand:
                # They called our bet
                self.opp_call_count += 1
                self.our_bet_count += 1
                self.our_bet_gets_call += 1
                # Track in rolling window for adaptation detection
                self.recent_fold_decisions.append(0)
                if len(self.recent_fold_decisions) > self.adaptation_window * 2:
                    self.recent_fold_decisions.pop(0)
            else:
                # Both checked
                self.opp_check_count += 1
        
        # Check for AllIn opponents early
        if self.hands_played <= self.early_allin_threshold:
            self._check_early_allin()
        
        # Store early baseline for adaptation detection
        self._store_early_baseline()
    
    def _check_early_allin(self):
        """Detect AllIn opponents early (within 30 hands)."""
        if self.opp_bet_count < 5:
            return  # Not enough betting data
        
        allin_freq = self.opp_allin_count / self.opp_bet_count
        if allin_freq >= self.allin_detection_ratio:
            self.opp_type = 'allin'
            self.strategy_mode = 'tight'  # Against all-in, play tight
