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
        
        # Phase 4/5: Opponent classification - REVISED
        self.opp_type = None  # None, 'allin', 'passive'
        self.opp_allin_count = 0  # Times opponent went all-in or near
        
        # Step 5.2: Early AllIn detection (within first 30 hands)
        self.early_allin_threshold = 30
        self.allin_detection_ratio = 0.70  # >70% all-in = allin player
        
        # Step 5.3: Conservative passive detection (after 100+ hands)
        self.passive_detection_hands = 100
        self.passive_bluff_threshold = 0.05  # <5% bluff = passive
        self.passive_bet_threshold = 0.25    # <25% bet frequency = passive
        
        # Step 6.1: Rolling window for recent performance
        self.recent_results = []  # Last N hands: (won: bool, profit: int)
        self.rolling_window_size = 20
        
        # Step 6.2: EV tracking for dynamic tuning
        self.ev_window_size = 50
        self.ev_results = []  # Last 50 hands for EV calculation
        
        # Step 6.3: Variance management flags
        self.conservative_mode = False  # When leading significantly
        self.aggressive_mode = False    # When trailing or near endgame
        
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
        
    def _calculate_gto_thresholds(self, bet_size_ratio=1.0):
        """
        Calculate GTO thresholds based on bet size relative to pot.
        For pot limit (B=P), bet_size_ratio = 1.0
        """
        B = 2.0 * bet_size_ratio
        P = 2.0
        
        # P1 thresholds - optimized bluffing (2x GTO)
        a = B / ((B + 1) * (B + 4)) * 2.0  # Bluff threshold ~0.22 (2x GTO)
        c = (B * (B + 3)) / ((B + 1) * (B + 4))  # Value threshold ~0.556
        
        # Check-call range
        check_range = c - a
        mdf = P / (P + B)
        call_range = check_range * mdf
        b = c - call_range
        
        # P2 thresholds - increased BB bluffing
        d = B / (P + B)  # Call threshold ~0.5
        e = 1.0 / (B + 4) * 1.5  # Bluff threshold ~0.25 (increased 50%)
        f = (B + 2) / (B + 4)  # Value threshold ~0.667
        
        return (a, b, c, d, e, f)
    
    def _get_pot_sized_bet(self, current_pot, minbet):
        """
        Calculate a pot-sized bet that is a valid multiple of minbet.
        """
        target_bet = current_pot * 2
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
        
        # Phase 1b: Calculate correct bet size ratio
        bet_size_ratio = self._get_bet_size_ratio(pot)
        
        # Get GTO thresholds
        a, b, c, d, e, f = self._calculate_gto_thresholds(bet_size_ratio)
        
        # Step 5.2/5.3: Apply SELECTIVE exploitative adjustments
        a, b, c, d, e, f = self._apply_selective_exploitation(a, b, c, d, e, f)
        
        # Step 6.2/6.3: Disabled - pure GTO with selective exploitation performs best
        # a, b, c, d, e, f = self._apply_ev_tuning(a, b, c, d, e, f)
        # a, b, c, d, e, f = self._apply_variance_adjustments(a, b, c, d, e, f)
        
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
        Minimal exploitation: Only detect AllIn players.
        """
        if self.opp_bet_count >= 5:
            allin_freq = self.opp_allin_count / self.opp_bet_count
            if allin_freq > 0.70:
                return (0, 0.5, 1.0, 0.5, 0, 1.0)
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
                self.my_contribution = self.initial_bb_pot
                return self.initial_bb_pot
        else:
            # Called again - either we bet and opp raised, or we checked and opp bet
            self.last_pot_seen = pot  # Update for next calculation
            
            if self.last_action == 'check':
                # Facing a bet from BB after we checked
                self.opp_bet_this_hand = True
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
            elif self.we_bet_this_hand:
                # They called our bet
                self.opp_call_count += 1
            else:
                # Both checked
                self.opp_check_count += 1
            
            # Phase 3: Bayesian updates based on opponent's revealed card
            self._update_bayesian_model(oppcard)
            
            # Store showdown data
            action = 'bet' if (self.opp_bet_this_hand or self.opp_raised_this_hand) else 'passive'
            self.opp_showdown_hands.append((oppcard, action, winnings))
        
        # Step 5.2: Early AllIn detection (within first 30 hands)
        if self.hands_played <= self.early_allin_threshold and self.opp_type is None:
            self._check_early_allin()
        
        # Step 5.3: Conservative passive detection (after 100+ hands)
        if self.hands_played == self.passive_detection_hands and self.opp_type is None:
            self._check_passive_opponent()
    
    def _check_early_allin(self):
        """Step 5.2: Detect AllIn opponents early (within 30 hands)."""
        if self.opp_bet_count < 5:
            return  # Not enough betting data
        
        allin_freq = self.opp_allin_count / self.opp_bet_count
        if allin_freq >= self.allin_detection_ratio:
            self.opp_type = 'allin'
    
    def _check_passive_opponent(self):
        """Step 5.3: Detect passive opponents after 100+ hands with high confidence."""
        total_actions = self.opp_bet_count + self.opp_check_count + self.opp_fold_count + self.opp_call_count
        if total_actions < 50:
            return  # Not enough data
        
        bet_freq = self.opp_bet_count / total_actions
        bluff_freq = self._get_opp_bluff_freq()
        
        # Very conservative thresholds
        if bluff_freq < self.passive_bluff_threshold and bet_freq < self.passive_bet_threshold:
            self.opp_type = 'passive'
    
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
