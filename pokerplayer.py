import random


class PokerPlayer:
    """
    Main PokerPlayer class - currently using OptimalThresholdPlayer (Phylum A4)
    as the strategy. This is a full GTO approximation using mathematically
    derived thresholds from continuous Kuhn poker theory.
    """
    def __init__(self):
        """Initialize my internal variables."""
        self.is_big_blind = False
        # Derived from continuous Kuhn poker theory
        self.BLUFF_THRESHOLD = 0.18
        self.FOLD_THRESHOLD = 0.35
        self.VALUE_THRESHOLD = 0.72

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
        self.is_big_blind = bigblind

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds - optimal GTO threshold strategy.

        card     - my card
        myscore  - my score
        oppscore - my opponent's score
        minbet   - the smallest bet increase that I am allowed make
        pot      - contains the current bid.
        """
        max_bet = min(myscore, oppscore)
        pot_odds = minbet / (pot + minbet) if (pot + minbet) > 0 else 0
        
        # Value betting range
        if card > self.VALUE_THRESHOLD:
            # Size bet based on card strength
            bet_multiplier = 1 + int((card - 0.7) / 0.1)
            bet_size = pot + minbet * bet_multiplier
            return min(bet_size, max_bet)
        
        # Bluffing range
        elif card < self.BLUFF_THRESHOLD:
            # Bluff frequency = pot odds (GTO optimal)
            if random.random() < pot_odds:
                bet_amount = pot + minbet
                return min(bet_amount, max_bet)
            else:
                return 0  # Fold
        
        # Folding range (weak non-bluffs)
        elif card < self.FOLD_THRESHOLD:
            return 0
        
        # Calling range (medium strength)
        else:
            return pot

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
        # Currently no state tracking needed for GTO strategy
        # This will be used in Phylum B (Opponent Modeling)
        pass


# ============================================================================
# Gen-0: Baseline Agents for Benchmarking
# ============================================================================

class AllInPlayer:
    """
    Baseline Agent B0.1: Bets entire stack every hand.
    Expected Win Rate: ~30%
    """
    def __init__(self):
        """Initialize my internal variables."""
        pass

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        """Start a new game of Random Texas."""
        pass

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds - always bet entire stack.
        Returns the maximum bet possible (min of both scores).
        """
        return min(myscore, oppscore)

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        """The game is over."""
        pass


class FoldBot:
    """
    Baseline Agent B0.2: Always folds unless Big Blind with card > 0.9.
    Expected Win Rate: ~10%
    """
    def __init__(self):
        """Initialize my internal variables."""
        self.is_big_blind = False

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        """Start a new game of Random Texas."""
        self.is_big_blind = bigblind

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds - fold unless Big Blind with very strong card.
        """
        # Only call if we're Big Blind and have a very strong card (>0.9)
        if self.is_big_blind and card > 0.9:
            return pot  # Call
        else:
            return 0  # Fold

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        """The game is over."""
        pass


class CallBot:
    """
    Baseline Agent B0.3: Always calls, never raises.
    Expected Win Rate: ~45-50%
    """
    def __init__(self):
        """Initialize my internal variables."""
        pass

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        """Start a new game of Random Texas."""
        pass

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds - always call, never raise.
        """
        return pot  # Always call

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        """The game is over."""
        pass


# ============================================================================
# Phylum A: GTO Lineage (Balanced Strategies)
# ============================================================================

class SimpleThresholdPlayer:
    """
    Phylum A1: SimpleThreshold Player
    Basic threshold strategy - highly predictable but establishes baseline.
    Strategy:
    - Fold if card < 0.3
    - Call if 0.3 <= card < 0.7
    - Raise if card >= 0.7
    """
    def __init__(self):
        """Initialize my internal variables."""
        pass

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        """Start a new game of Random Texas."""
        pass

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds - simple threshold strategy.
        """
        if card < 0.3:
            return 0  # Fold
        elif card < 0.7:
            return pot  # Call
        else:
            # Raise - bet pot + minbet, capped at max possible
            max_bet = min(myscore, oppscore)
            bet_amount = pot + minbet
            return min(bet_amount, max_bet)

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        """The game is over."""
        pass


class PositionAwarePlayer:
    """
    Phylum A2: PositionAware Player
    Exploits positional advantage by adjusting thresholds based on position.
    Strategy:
    - Small Blind (tighter): Fold < 0.35, Call 0.35-0.75, Raise > 0.75
    - Big Blind (wider/defensive): Fold < 0.25, Call 0.25-0.70, Raise > 0.70
    """
    def __init__(self):
        """Initialize my internal variables."""
        self.is_big_blind = False

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        """Start a new game of Random Texas."""
        self.is_big_blind = bigblind

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds - position-aware threshold strategy.
        """
        if self.is_big_blind:
            # Big Blind: wider range (already invested 2x, acts last)
            if card < 0.25:
                return 0  # Fold
            elif card < 0.70:
                return pot  # Call
            else:
                # Raise
                max_bet = min(myscore, oppscore)
                bet_amount = pot + minbet
                return min(bet_amount, max_bet)
        else:
            # Small Blind: tighter range (acts first, less invested)
            if card < 0.35:
                return 0  # Fold
            elif card < 0.75:
                return pot  # Call
            else:
                # Raise
                max_bet = min(myscore, oppscore)
                bet_amount = pot + minbet
                return min(bet_amount, max_bet)

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        """The game is over."""
        pass


class MixedStrategyPlayer:
    """
    Phylum A3: MixedStrategy Player
    Introduces randomization and polarization to prevent exploitation.
    Strategy:
    - Polarize ranges: Only raise with very strong hands (value) or select weak hands (bluffs)
    - Implement GTO bluffing: Use optimal bluffing frequency from pot odds
    """
    def __init__(self):
        """Initialize my internal variables."""
        self.is_big_blind = False

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        """Start a new game of Random Texas."""
        self.is_big_blind = bigblind

    def should_bluff(self, card, pot, minbet):
        """
        Determine if we should bluff based on GTO bluffing frequency.
        Bluff frequency should match pot odds offered.
        """
        if card < 0.15:  # Bluff with bottom 15% of range
            # Bluff frequency = minbet / (pot + minbet)
            bluff_frequency = minbet / (pot + minbet) if (pot + minbet) > 0 else 0
            return random.random() < bluff_frequency
        return False

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds - mixed strategy with value betting and GTO bluffing.
        """
        max_bet = min(myscore, oppscore)
        
        # Strong value hands - always raise
        if card > 0.75:
            bet_amount = pot + minbet
            return min(bet_amount, max_bet)
        
        # Bluffing range - randomized based on GTO frequency
        elif card < 0.15 and self.should_bluff(card, pot, minbet):
            bet_amount = pot + minbet
            return min(bet_amount, max_bet)
        
        # Weak non-bluffs - fold
        elif card < 0.30:
            return 0
        
        # Medium strength hands - call
        else:
            return pot

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        """The game is over."""
        pass


class OptimalThresholdPlayer:
    """
    Phylum A4: OptimalThreshold Player
    Full GTO approximation using mathematically derived thresholds.
    This is the "final boss" of the GTO lineage and serves as the baseline
    strategy for the Ultimate Hybrid.
    Strategy derived from continuous Kuhn poker theory.
    """
    def __init__(self):
        """Initialize my internal variables."""
        self.is_big_blind = False
        # Derived from continuous Kuhn poker theory
        self.BLUFF_THRESHOLD = 0.18
        self.FOLD_THRESHOLD = 0.35
        self.VALUE_THRESHOLD = 0.72

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        """Start a new game of Random Texas."""
        self.is_big_blind = bigblind

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds - optimal GTO threshold strategy.
        """
        max_bet = min(myscore, oppscore)
        pot_odds = minbet / (pot + minbet) if (pot + minbet) > 0 else 0
        
        # Value betting range
        if card > self.VALUE_THRESHOLD:
            # Size bet based on card strength
            bet_multiplier = 1 + int((card - 0.7) / 0.1)
            bet_size = pot + minbet * bet_multiplier
            return min(bet_size, max_bet)
        
        # Bluffing range
        elif card < self.BLUFF_THRESHOLD:
            # Bluff frequency = pot odds (GTO optimal)
            if random.random() < pot_odds:
                bet_amount = pot + minbet
                return min(bet_amount, max_bet)
            else:
                return 0  # Fold
        
        # Folding range (weak non-bluffs)
        elif card < self.FOLD_THRESHOLD:
            return 0
        
        # Calling range (medium strength)
        else:
            return pot

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        """The game is over."""
        pass
