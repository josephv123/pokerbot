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
        
        # Phase 1b: Track betting for correct B/P ratio in multi-raise scenarios
        self.my_contribution = 0  # What we've put in this hand
        self.last_pot_seen = 0    # Last pot level we saw
        
        # Phase 2: Opponent action tracking
        self.hands_played = 0
        self.opp_bet_count = 0      # Times opponent bet/raised
        self.opp_check_count = 0    # Times opponent checked
        self.opp_fold_count = 0     # Times opponent folded
        self.opp_call_count = 0     # Times opponent called our bet
        self.consecutive_folds = 0  # For boredom detection
        self.opp_showdown_hands = []  # (opp_card, opp_action, winnings)
        
        # Phase 3: Bayesian opponent modeling (Beta distributions)
        self.bluff_alpha, self.bluff_beta = 1, 9    # Prior: ~10% bluff rate
        self.call_alpha, self.call_beta = 1, 1      # Prior: 50% call rate  
        self.value_alpha, self.value_beta = 4, 1    # Prior: ~80% value rate
        
        # Phase 4/5: Opponent classification - REVISED with 3-mode system
        self.opp_type = None  # None, 'allin', 'folder', 'caller', 'aggressor'
        self.opp_allin_count = 0  # Times opponent went all-in or near
        
        # Strategy mode: 'aggressive', 'balanced', 'tight'
        self.strategy_mode = 'aggressive'  # Default to current aggressive strategy
        
        # Early detection thresholds (original best config)
        self.early_detection_threshold = 15  # Minimum bets to classify
        self.early_allin_threshold = 30
        self.allin_detection_ratio = 0.70  # >70% all-in = allin player
        
        # Opponent classification thresholds (original best config)
        self.folder_threshold = 0.55     # >55% fold rate = folder
        self.caller_threshold = 0.30     # <30% fold rate = caller
        self.aggressor_raise_threshold = 0.30  # >30% raise rate = aggressor
        
        # Adaptation detection (from plan)
        self.recent_fold_decisions = []  # Last 20: 1=fold, 0=not fold
        self.early_fold_rate = None      # Stored after first 30 hands
        self.adaptation_window = 20
        self.drift_threshold = 0.20  # Increased threshold to be more conservative
        
        # Showdown statistics for better opponent modeling
        self.opp_bet_card_sum = 0.0     # Sum of opponent cards when they bet
        self.opp_bet_card_count = 0     # Count of showdowns where opponent bet
        
        # Aggression tracking (bets when checked to)
        self.we_checked_to_opp = 0      # Times we checked to opponent
        self.opp_bet_when_checked = 0   # Times opponent bet when we checked
        
        # Step 6.1: Rolling window for recent performance
        self.recent_results = []  # Last N hands: (won: bool, profit: int)
        self.rolling_window_size = 20
        
        # Step 6.2: EV tracking for dynamic tuning
        self.ev_window_size = 50
        self.ev_results = []  # Last 50 hands for EV calculation
        
        # Step 6.3: Variance management flags
        self.conservative_mode = False  # When leading significantly
        self.aggressive_mode = False    # When trailing or near endgame
        
        # Phase A: Track opponent response to OUR bets specifically
        self.our_bet_count = 0       # Times we bet/raised
        self.our_bet_gets_fold = 0   # Times opponent folded to our bet
        self.our_bet_gets_call = 0   # Times opponent called our bet
        self.our_bet_gets_raise = 0  # Times opponent raised our bet
        
        # Phase A.2: Bluff profitability tracking
        self.bluff_attempts = 0      # Times we bluffed (bet with weak hand)
        self.bluff_profits = 0       # Total profit from bluffs
        
        # Phase B: Showdown range estimation
        self.opp_bet_showdown_cards = []   # Cards when opp bet and reached showdown
        self.opp_call_showdown_cards = []  # Cards when opp called and reached showdown
        self.opp_check_showdown_cards = [] # Cards when opp checked and reached showdown
        
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
        
        # Store initial pot values for this hand
        self.initial_sb_pot = minbet  # SB's blind
        self.initial_bb_pot = 2 * minbet  # Total after both blinds
        self.last_action = None  # Track our last action: 'bet', 'check', or None
        
        # Phase 1b: Initialize contribution tracking for this hand
        if bigblind:
            self.my_contribution = 2 * minbet  # BB puts in 2*minbet
        else:
            self.my_contribution = minbet  # SB puts in minbet
        self.last_pot_seen = 2 * minbet  # Initial betPot is always 2*minbet
        
        # Phase 2: Track opponent's action this hand
        self.opp_bet_this_hand = False
        self.opp_raised_this_hand = False
        self.we_bet_this_hand = False
        self.we_checked_this_hand = False  # Track if we checked to opponent
        
        # Phase A: Track our bet details this hand
        self.our_bet_was_bluff = False  # True if we bet with card < 0.35
        self.our_bet_amount = 0         # How much we bet
        
        # Step 6.3: Update variance management mode based on scores
        self._update_variance_mode(myscore, oppscore)
        
    def _update_variance_mode(self, myscore, oppscore):
        """Step 6.3: Determine if we should play more conservatively or aggressively."""
        # When leading significantly (>120 points): Play conservative
        if myscore > 120:
            self.conservative_mode = True
            self.aggressive_mode = False
        # When trailing (<80 points): Accept more variance
        elif myscore < 80:
            self.conservative_mode = False
            self.aggressive_mode = True
        # Near endgame (opponent has <20 points): Push harder
        elif oppscore < 20:
            self.conservative_mode = False
            self.aggressive_mode = True
        else:
            self.conservative_mode = False
            self.aggressive_mode = False
        
    def _detect_opponent_type(self):
        """
        Detect opponent type based on their response patterns to our bets.
        Called after we have enough data (15+ bet responses).
        """
        if self.our_bet_count < self.early_detection_threshold:
            return None  # Not enough data
        
        fold_rate = self.our_bet_gets_fold / self.our_bet_count
        call_rate = self.our_bet_gets_call / self.our_bet_count
        raise_rate = self.our_bet_gets_raise / self.our_bet_count
        
        # Calculate aggression (bets when checked to)
        aggression = 0.0
        if self.we_checked_to_opp >= 5:
            aggression = self.opp_bet_when_checked / self.we_checked_to_opp
        
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
        Returns (bet_mult, bluff_mult, value_mult, call_mult)
        """
        if self.strategy_mode == 'aggressive':
            # Default for folders: 4x pot, 2.5x bluff (original optimal)
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
        # Only apply after we've established a baseline
        if self._check_for_adaptation() and self.strategy_mode != 'tight':
            # Don't override tight mode (for callers/allin) but do override aggressive
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
        
        # P1 thresholds
        a = B / ((B + 1) * (B + 4)) * SB_BLUFF_MULT  # Bluff threshold
        c = (B * (B + 3)) / ((B + 1) * (B + 4)) * VALUE_MULT  # Value threshold
        
        # Check-call range
        check_range = c - a
        mdf = P / (P + B)
        call_range = check_range * mdf
        b = (c - call_range) * CALL_MULT  # Adjusted call threshold
        
        # P2 thresholds
        d = B / (P + B) * CALL_MULT  # Call threshold, adjusted
        e = 1.0 / (B + 4) * BB_BLUFF_MULT  # Bluff threshold
        f = (B + 2) / (B + 4) * VALUE_MULT  # Value threshold
        
        return (a, b, c, d, e, f)
    
    def _get_pot_sized_bet(self, current_pot, minbet):
        """
        Calculate bet that is a valid multiple of minbet.
        Bet size varies based on strategy mode.
        """
        # Get bet multiplier from strategy params
        params = self._get_strategy_params()
        bet_mult = params['bet_mult']
        
        # target_bet = current_pot * bet_mult (e.g., 5 for 4x pot overbet)
        target_bet = current_pot * bet_mult
        bet = int(target_bet / minbet) * minbet
        return max(bet, current_pot + minbet)
    
    def _round_to_minbet(self, amount, minbet):
        """Round amount down to nearest valid multiple of minbet."""
        return int(amount / minbet) * minbet
    
    def _get_bet_size_ratio(self, pot):
        """
        Phase 1b: Calculate correct B/P ratio for threshold calculation.
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
        
        # Phase 1b: Calculate correct bet size ratio
        bet_size_ratio = self._get_bet_size_ratio(pot)
        
        # Get GTO thresholds (adjusted for strategy mode)
        a, b, c, d, e, f = self._calculate_gto_thresholds(bet_size_ratio)
        
        # Step 5.2/5.3: Apply SELECTIVE exploitative adjustments
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
        # AllIn detection
        if self.opp_bet_count >= 5:
            allin_freq = self.opp_allin_count / self.opp_bet_count
            if allin_freq > 0.70:
                return (0, 0.5, 1.0, 0.5, 0, 1.0)
        
        # Adjust calling threshold based on opponent's betting range
        # If opponent bets with weak hands (low bet_card_mean), call more
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
    
    def _apply_ev_tuning(self, a, b, c, d, e, f):
        """
        Step 6.2: Dynamically tune thresholds based on recent EV.
        If losing significantly: tighten slightly
        If winning well: maintain current strategy
        
        REVISED: More conservative - only adjust after significant data
        """
        if len(self.ev_results) < self.ev_window_size:
            # Not enough data yet - use pure GTO
            return (a, b, c, d, e, f)
        
        # Calculate EV over last 50 hands
        recent_ev = sum(self.ev_results[-self.ev_window_size:])
        
        # Only adjust if losing significantly (> 10 points over 50 hands)
        if recent_ev < -10:
            # We're losing badly - tighten bluffs only by 3%
            new_a = a * 0.97  # Bluff slightly less
            new_e = e * 0.97  # Bluff slightly less
            return (new_a, b, c, d, new_e, f)
        
        # If winning or neutral, maintain current strategy
        return (a, b, c, d, e, f)
    
    def _apply_variance_adjustments(self, a, b, c, d, e, f):
        """
        Step 6.3: Adjust strategy based on score position.
        - Leading: Play slightly tighter (5%)
        - Trailing/Endgame: Accept slightly more variance
        
        REVISED: More conservative adjustments to not hurt baseline
        """
        if self.conservative_mode:
            # Play 5% tighter when leading significantly
            new_a = a * 0.95  # Bluff slightly less
            new_e = e * 0.95  # Bluff slightly less
            return (new_a, b, c, d, new_e, f)
        
        elif self.aggressive_mode:
            # Accept slightly more variance when trailing or near endgame
            # Slightly wider value range only
            new_c = max(c * 0.97, 0.52)  # Value bet slightly wider
            new_f = max(f * 0.97, 0.62)  # Value bet slightly wider
            return (a, b, new_c, d, e, new_f)
        
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
                self.our_bet_was_bluff = True  # Phase A: Mark as bluff
                self.our_bet_amount = bet
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
                self.our_bet_was_bluff = False  # Phase A: Not a bluff
                self.our_bet_amount = bet
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
                self.our_bet_was_bluff = True  # Phase A: Mark as bluff
                self.our_bet_amount = bet
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
                self.our_bet_was_bluff = False  # Phase A: Not a bluff
                self.our_bet_amount = bet
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
        
        # Step 6.1: Track recent performance (rolling window)
        profit = winnings if iwon else -winnings
        self.recent_results.append((iwon, profit))
        if len(self.recent_results) > self.rolling_window_size:
            self.recent_results.pop(0)
        
        # Step 6.2: Track EV for dynamic tuning
        self.ev_results.append(profit)
        if len(self.ev_results) > self.ev_window_size:
            self.ev_results.pop(0)
        
        # Phase 2: Track opponent actions
        if oppcard is None:
            # Someone folded
            if iwon:
                # Opponent folded
                self.opp_fold_count += 1
                self.consecutive_folds += 1
                
                # Phase A: Track response to our bet
                if self.we_bet_this_hand:
                    self.our_bet_count += 1
                    self.our_bet_gets_fold += 1
                    # Track in rolling window for adaptation detection
                    self.recent_fold_decisions.append(1)
                    if len(self.recent_fold_decisions) > self.adaptation_window * 2:
                        self.recent_fold_decisions.pop(0)
                    # Track bluff profitability
                    if self.our_bet_was_bluff:
                        self.bluff_attempts += 1
                        self.bluff_profits += winnings
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
                # Phase A: They raised our bet
                if self.we_bet_this_hand:
                    self.our_bet_count += 1
                    self.our_bet_gets_raise += 1
                    # Track in rolling window for adaptation detection (didn't fold)
                    self.recent_fold_decisions.append(0)
                    if len(self.recent_fold_decisions) > self.adaptation_window * 2:
                        self.recent_fold_decisions.pop(0)
            elif self.we_bet_this_hand:
                # They called our bet
                self.opp_call_count += 1
                # Phase A: Track response to our bet
                self.our_bet_count += 1
                self.our_bet_gets_call += 1
                # Track in rolling window for adaptation detection (didn't fold)
                self.recent_fold_decisions.append(0)
                if len(self.recent_fold_decisions) > self.adaptation_window * 2:
                    self.recent_fold_decisions.pop(0)
                # Track bluff profitability (we lost at showdown with bluff)
                if self.our_bet_was_bluff:
                    self.bluff_attempts += 1
                    if iwon:
                        self.bluff_profits += winnings
                    else:
                        self.bluff_profits -= winnings
            else:
                # Both checked
                self.opp_check_count += 1
            
            # Phase 3: Bayesian updates based on opponent's revealed card
            self._update_bayesian_model(oppcard)
            
            # Phase B: Track showdown cards by action type
            if self.opp_bet_this_hand or self.opp_raised_this_hand:
                self.opp_bet_showdown_cards.append(oppcard)
                # Track for bet_card_mean calculation
                self.opp_bet_card_sum += oppcard
                self.opp_bet_card_count += 1
            elif self.we_bet_this_hand:
                # They called our bet
                self.opp_call_showdown_cards.append(oppcard)
            else:
                # Both checked
                self.opp_check_showdown_cards.append(oppcard)
            
            # Store showdown data (legacy)
            action = 'bet' if (self.opp_bet_this_hand or self.opp_raised_this_hand) else 'passive'
            self.opp_showdown_hands.append((oppcard, action, winnings))
        
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
    
    def _update_bayesian_model(self, oppcard):
        """Phase 3: Update Bayesian model based on opponent's revealed card."""
        if self.opp_bet_this_hand or self.opp_raised_this_hand:
            # Opponent bet - was it a bluff or value?
            if oppcard < 0.25:
                # Weak hand - this was a bluff
                self.bluff_alpha += 1
            elif oppcard > 0.65:
                # Strong hand - this was value
                self.value_alpha += 1
            # Medium hands are harder to classify
        else:
            # Opponent was passive (checked or called)
            if oppcard < 0.15:
                # Should have bluffed but didn't
                self.bluff_beta += 1
            elif oppcard > 0.55:
                # Could have value bet but didn't
                self.value_beta += 1
    
    def _get_opp_bluff_freq(self):
        """Phase 3: Get posterior mean of opponent's bluff frequency."""
        return self.bluff_alpha / (self.bluff_alpha + self.bluff_beta)
    
    def _get_opp_value_freq(self):
        """Phase 3: Get posterior mean of opponent's value betting frequency."""
        return self.value_alpha / (self.value_alpha + self.value_beta)
