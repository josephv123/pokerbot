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
        self.betting_history = []  # Track betting sequence
        self.epsilon = 1e-9  # For floating point comparisons
        
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
        self.betting_history = []  # Reset for new hand
        # Store initial pot values for this hand
        self.initial_sb_pot = minbet  # SB's blind
        self.initial_bb_pot = 2 * minbet  # Total after both blinds
        self.last_action = None  # Track our last action: 'bet', 'check', or None
        
    def _calculate_gto_thresholds(self, bet_size_ratio=1.0):
        """
        Calculate GTO thresholds based on bet size relative to pot.
        For pot limit (B=P), bet_size_ratio = 1.0
        
        Returns: (a, b, c, d, e, f) where:
        - a: P1 bluff threshold
        - b: P1 check-call threshold (boundary between check-fold and check-call)
        - c: P1 value threshold
        - d: P2 call threshold when facing bet
        - e: P2 bluff threshold when facing check
        - f: P2 value threshold when facing check
        """
        # For pot limit (B = P), normalized to B=2 if pot=2
        # Using formulas from research plan
        B = 2.0 * bet_size_ratio  # Normalized bet size
        
        # P1 thresholds
        a = B / ((B + 1) * (B + 4))  # Bluff threshold
        b = (B**2 + 4*B + 2) / ((B + 1) * (B + 4))  # Check-call threshold
        c = (B * (B + 3)) / ((B + 1) * (B + 4))  # Value threshold
        
        # Correct ordering: ensure a < b < c
        # If b > c, swap them (research plan has confusion here)
        if b > c:
            # Standard interpretation: check range is a to c, with b as call boundary
            # Set b to midpoint of check range for call/fold decision
            # b = (a + c) / 2
            # Correct derivation for Pot Limit (B=P):
            # P1 should call with (B/P) / (1 + B/P) fraction of check range?
            # No, P2 needs to be indifferent.
            # P1 call freq C, fold freq F. F/C = B/P.
            # C = (1 / (1+B/P)) * TotalCheckRange
            # If B=P, C = 1/2 TotalCheckRange.
            # So b should be midpoint.
            b = (a + c) / 2
        
        # print(f"DEBUG: Thresholds: a={a:.2f} b={b:.2f} c={c:.2f} d={d:.2f} e={e:.2f} f={f:.2f}")
        
        # P2 thresholds
        # When facing bet: MDF (Minimum Defense Frequency)
        # When facing bet: MDF (Minimum Defense Frequency)
        d = B / (B + 2)  # Call threshold (for B=2, d=0.5)
        
        # When facing check: P2 betting thresholds
        # From research plan table: e=1/6, f=2/3
        e = 1.0 / 6.0  # Bluff threshold
        f = 2.0 / 3.0  # Value threshold
        
        return (a, b, c, d, e, f)
    
    def _get_pot_sized_bet(self, current_pot, minbet):
        """
        Calculate a pot-sized bet that is a valid multiple of minbet.
        Returns the total amount to put in pot.
        
        Pot-sized bet means betting the current pot size more.
        If current_pot = P, we bet P more, so total = 2*P.
        """
        target_bet = current_pot * 2
        
        # Round down to nearest valid multiple of minbet (to avoid warnings)
        bet = int(target_bet / minbet) * minbet
        
        return bet
    
    def _round_to_minbet(self, amount, minbet):
        """Round amount to nearest valid multiple of minbet."""
        return round(amount / minbet) * minbet
    
    def _boundary_dither(self, hand, threshold):
        """
        Apply boundary dithering: if hand is very close to threshold,
        randomize the decision to prevent exploitation.
        """
        if abs(hand - threshold) < self.epsilon:
            return random.random() < 0.5
        return hand < threshold
    
    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds.

        card     - my card
        myscore  - my score
        oppscore - my opponent's score
        minbet   - the smallest bet increase that I am allowed make
        pot      - contains the current bid.
        """
        # print(f"DEBUG: Role={self.role} Card={card:.2f} Pot={pot} MyScore={myscore} OppScore={oppscore}")
        self.hand_strength = card
        self.myscore = myscore
        self.oppscore = oppscore
        self.minbet = minbet
        self.pot = pot
        
        # Calculate GTO thresholds
        # Determine bet size ratio B/P
        # If pot is small (opening), B/P is irrelevant (we use B=P for our bets)
        # If facing a bet, we need to know what B/P the opponent used.
        
        bet_size_ratio = 1.0 # Default
        if pot > self.initial_bb_pot + self.epsilon:
            # Opponent bet something
            # Assuming base pot was initial_bb_pot (2*minbet)
            bet_amount = pot - self.initial_bb_pot
            # Base pot P = initial_bb_pot
            # But wait, if we bet and they raised?
            # Simplified game usually has 1 bet then call/fold.
            # So we can assume base pot is initial_bb_pot.
            if self.initial_bb_pot > 0:
                 bet_size_ratio = bet_amount / self.initial_bb_pot
            else:
                 bet_size_ratio = 1.0
        
        a, b, c, d, e, f = self._calculate_gto_thresholds(bet_size_ratio)
        
        max_bet = min(myscore, oppscore)
        
        # Use epsilon comparison for floating point pot values
        def pot_equals(p1, p2):
            return abs(p1 - p2) < self.epsilon
        
        if self.role == 'SB':
            # Small Blind acts first
            # When SB acts first, pot is usually 2*minbet (betPot in game engine)
            # But better to rely on history: if we haven't acted yet, it's opening
            if self.last_action is None:
                # Opening action: can call (2*minbet) or raise
                if self.hand_strength < a:
                    # Bluff: raise with pot-sized bet
                    bet = self._get_pot_sized_bet(pot, minbet)
                    bet = min(bet, max_bet)
                    bet = self._round_to_minbet(bet, minbet)
                    bet = max(bet, pot + minbet)  # Must raise at least minbet
                    self.last_action = 'bet'
                    return bet
                elif self.hand_strength >= c:
                    # Value bet: raise with pot-sized bet
                    bet = self._get_pot_sized_bet(pot, minbet)
                    bet = min(bet, max_bet)
                    bet = self._round_to_minbet(bet, minbet)
                    bet = max(bet, pot + minbet)
                    self.last_action = 'bet'
                    return bet
                else:
                    # Check (call): return 2*minbet to call BB
                    self.last_action = 'check'
                    # print(f"DEBUG: SB Check-Call. Return {self.initial_bb_pot}")
                    return self.initial_bb_pot
            else:
                # Pot has increased - either we bet and opponent raised, or we checked and opponent bet
                if self.last_action == 'check':
                    # Facing a bet from BB after we checked
                    # Decision: call or fold based on check-call threshold (b)
                    if self.hand_strength >= b:
                        # Check-call: call the bet
                        # print(f"DEBUG: SB Check-Call (Defend). Return {pot}")
                        return pot
                    else:
                        # Check-fold: fold
                        # print(f"DEBUG: SB Check-Fold. Return 0")
                        return 0  # Return less than pot to fold
                else:
                    # We bet and opponent raised - this shouldn't happen in simplified game
                    # But handle it: call if strong enough
                    if self.hand_strength >= c:
                        return pot  # Call with value hands
                    else:
                        return 0  # Fold weaker hands
                    
        else:  # self.role == 'BB'
            # Big Blind acts second
            # We are facing SB's action.
            # If SB checked, pot is 2*minbet (initial_bb_pot).
            # If SB bet, pot > 2*minbet.
            if pot_equals(pot, self.initial_bb_pot):
                # SB called (checked), we can check back or bet
                if self.hand_strength < e:
                    # Bluff: bet
                    bet = self._get_pot_sized_bet(pot, minbet)
                    bet = min(bet, max_bet)
                    bet = self._round_to_minbet(bet, minbet)
                    bet = max(bet, pot + minbet)
                    self.last_action = 'bet'
                    return bet
                elif self.hand_strength >= f:
                    # Value bet: bet
                    bet = self._get_pot_sized_bet(pot, minbet)
                    bet = min(bet, max_bet)
                    bet = self._round_to_minbet(bet, minbet)
                    bet = max(bet, pot + minbet)
                    self.last_action = 'bet'
                    return bet
                else:
                    # Check back: call (return same pot to end hand)
                    self.last_action = 'check'
                    return pot
            else:
                # Facing a raise from SB
                # Decision: call or fold based on MDF threshold (d)
                if self.hand_strength >= d:
                    # Call
                    return pot
                else:
                    # Fold
                    return 0  # Return less than pot to fold

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
        # For now, just update scores (opponent modeling can be added later)
        self.myscore = myscore
        self.oppscore = oppscore
        # TODO: Add Bayesian opponent modeling here in future iterations