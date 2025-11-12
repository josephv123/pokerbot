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


class ICMScoreAwarePlayer:
    """
    Phylum C2: ICM & Score-Aware Meta-Strategy Player
    Adjusts strategy based on score differential and blind levels (M-ratio).
    
    Core Concept: In winner-take-all tournaments, chips have non-linear value.
    Strategy must adapt based on:
    1. Score differential (ICM): Leading = risk-averse, Trailing = risk-seeking
    2. M-Ratio (blind levels): High M = deep-stacked, Low M = push/fold
    
    Strategy:
    - When Leading: Play risk-averse, protect lead, avoid high-variance spots
    - When Trailing: Play risk-seeking, increase variance, bluff more, call lighter
    - High M (Early): Play nuanced, deep-stacked poker
    - Low M (Late): Shift to push/fold strategy
    """
    def __init__(self):
        """Initialize my internal variables."""
        self.is_big_blind = False
        self.hand_count = 0  # Track hands to know when minbet doubles
        # GTO thresholds (baseline)
        self.BLUFF_THRESHOLD = 0.18
        self.FOLD_THRESHOLD = 0.35
        self.VALUE_THRESHOLD = 0.72

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        """Start a new game of Random Texas."""
        self.is_big_blind = bigblind
        self.hand_count += 1

    def calculate_m_ratio(self, myscore, minbet):
        """
        Calculate M-ratio: stack / (small_blind + big_blind)
        Small blind = minbet, Big blind = 2*minbet
        """
        blinds = minbet + 2 * minbet  # SB + BB
        if blinds > 0:
            return myscore / blinds
        return float('inf')  # Avoid division by zero

    def get_score_differential(self, myscore, oppscore):
        """
        Calculate score differential as a ratio.
        Returns positive if leading, negative if trailing.
        """
        total = myscore + oppscore
        if total > 0:
            return (myscore - oppscore) / total
        return 0.0

    def adjust_thresholds_for_icm(self, myscore, oppscore):
        """
        Adjust betting thresholds based on score differential (ICM).
        Returns adjusted thresholds.
        """
        score_diff = self.get_score_differential(myscore, oppscore)
        
        # Base thresholds
        bluff_thresh = self.BLUFF_THRESHOLD
        fold_thresh = self.FOLD_THRESHOLD
        value_thresh = self.VALUE_THRESHOLD
        
        if score_diff > 0.1:  # Leading significantly (e.g., 120 vs 80)
            # Risk-averse: Tighten up, reduce bluffing, protect lead
            bluff_thresh = 0.15  # Bluff less
            fold_thresh = 0.40   # Fold more (tighter)
            value_thresh = 0.75  # Only value bet with stronger hands
        elif score_diff < -0.1:  # Trailing significantly (e.g., 80 vs 120)
            # Risk-seeking: Loosen up, bluff more, call lighter
            bluff_thresh = 0.25  # Bluff more
            fold_thresh = 0.30   # Fold less (looser)
            value_thresh = 0.68  # Value bet with wider range
        
        return bluff_thresh, fold_thresh, value_thresh

    def adjust_for_m_ratio(self, m_ratio, card, pot, minbet):
        """
        Adjust strategy based on M-ratio (blind levels).
        Low M = push/fold strategy (simplified, aggressive)
        High M = nuanced poker
        """
        if m_ratio < 5:  # Very low M (short-stacked)
            # Push/fold strategy: All-in or fold with clear thresholds
            if card > 0.65:  # Strong hand - push
                return 'push'
            elif card < 0.25:  # Weak hand - fold
                return 'fold'
            else:
                return 'call'  # Medium - call if pot odds good
        elif m_ratio < 15:  # Medium M
            # Slightly more aggressive, but still nuanced
            return 'normal'
        else:  # High M (deep-stacked)
            # Play nuanced, deep-stacked poker
            return 'normal'

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds - ICM and M-ratio aware strategy.
        """
        max_bet = min(myscore, oppscore)
        pot_odds = minbet / (pot + minbet) if (pot + minbet) > 0 else 0
        required_equity = pot_odds
        
        # Calculate M-ratio and score differential
        m_ratio = self.calculate_m_ratio(myscore, minbet)
        m_strategy = self.adjust_for_m_ratio(m_ratio, card, pot, minbet)
        
        # Adjust thresholds based on ICM (score differential)
        bluff_thresh, fold_thresh, value_thresh = self.adjust_thresholds_for_icm(myscore, oppscore)
        
        # Low M push/fold strategy
        if m_strategy == 'push':
            # Push (all-in or large bet) with strong hands
            return max_bet
        elif m_strategy == 'fold':
            # Fold weak hands
            return 0
        
        # Normal strategy with ICM-adjusted thresholds
        # Value betting range
        if card > value_thresh:
            # Size bet based on card strength and ICM
            score_diff = self.get_score_differential(myscore, oppscore)
            if score_diff > 0.1:  # Leading - bet smaller to reduce variance
                bet_multiplier = 1 + int((card - 0.7) / 0.15)  # Smaller bets
            elif score_diff < -0.1:  # Trailing - bet larger to increase variance
                bet_multiplier = 1 + int((card - 0.7) / 0.08)  # Larger bets
            else:
                bet_multiplier = 1 + int((card - 0.7) / 0.1)  # Normal
            
            bet_size = pot + minbet * bet_multiplier
            return min(bet_size, max_bet)
        
        # Bluffing range (ICM-adjusted)
        elif card < bluff_thresh:
            # Adjust bluff frequency based on score differential
            score_diff = self.get_score_differential(myscore, oppscore)
            if score_diff < -0.1:  # Trailing - bluff more
                adjusted_bluff_freq = pot_odds * 1.5  # Increase bluffing
            elif score_diff > 0.1:  # Leading - bluff less
                adjusted_bluff_freq = pot_odds * 0.5  # Decrease bluffing
            else:
                adjusted_bluff_freq = pot_odds
            
            adjusted_bluff_freq = min(adjusted_bluff_freq, 1.0)  # Cap at 1.0
            
            if random.random() < adjusted_bluff_freq:
                bet_amount = pot + minbet
                return min(bet_amount, max_bet)
            else:
                return 0  # Fold
        
        # Folding range (ICM-adjusted)
        elif card < fold_thresh:
            # Check pot odds - trailing players call lighter
            score_diff = self.get_score_differential(myscore, oppscore)
            if score_diff < -0.1:  # Trailing - call lighter
                if card >= required_equity * 0.8:  # 20% looser calling
                    return pot  # Call
            elif score_diff > 0.1:  # Leading - fold tighter
                if card >= required_equity * 1.2:  # 20% tighter calling
                    return pot  # Call
            
            # Default: check pot odds
            if card >= required_equity:
                return pot  # Call
            else:
                return 0  # Fold
        
        # Calling range (medium strength)
        else:
            # Adjust calling based on ICM
            score_diff = self.get_score_differential(myscore, oppscore)
            if score_diff < -0.1:  # Trailing - call lighter
                if card >= required_equity * 0.9:
                    return pot  # Call
            elif score_diff > 0.1:  # Leading - call tighter
                if card >= required_equity * 1.1:
                    return pot  # Call
            
            # Default: standard pot odds
            if card >= required_equity:
                return pot  # Call
            else:
                return 0  # Fold

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        """The game is over."""
        # Reset hand count every 100 hands (when minbet doubles)
        if self.hand_count >= 100:
            self.hand_count = 0


# ============================================================================
# Phylum C: Advanced & Game-Specific Strategies
# ============================================================================

class KellyBettingPlayer:
    """
    Phylum C1: Kelly-Based Bet Sizing Player
    Uses the Kelly Criterion to determine mathematically optimal bet sizes.
    
    Core Concept: Since card value represents exact win probability, we can use
    Kelly Criterion (f* = 2p - 1) to maximize long-term bankroll growth.
    Uses fractional Kelly (0.4x) to reduce variance while retaining most growth.
    
    Strategy:
    - For positive EV hands (card > 0.5), use Kelly formula to size bets
    - For negative EV hands (card <= 0.5), fold or call only with good pot odds
    - Combine with GTO thresholds for decision-making
    """
    def __init__(self):
        """Initialize my internal variables."""
        self.is_big_blind = False
        self.kelly_multiplier = 0.4  # Fractional Kelly to reduce variance
        # GTO thresholds for decision-making
        self.BLUFF_THRESHOLD = 0.18
        self.FOLD_THRESHOLD = 0.35
        self.VALUE_THRESHOLD = 0.72

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        """Start a new game of Random Texas."""
        self.is_big_blind = bigblind

    def fractional_kelly(self, card_value, myscore, minbet, pot):
        """
        Calculate optimal bet size using fractional Kelly Criterion.
        
        Kelly formula for even-money bets: f* = 2p - 1
        where p is win probability (card value) and f* is fraction of stack to bet.
        
        Returns the total amount to put in pot (not incremental), or None if negative EV.
        """
        # Kelly fraction: f* = 2p - 1
        kelly_fraction = 2 * card_value - 1
        
        if kelly_fraction <= 0:
            # Negative or zero EV - should fold or call only with good pot odds
            return None
        
        # Use fractional Kelly for reduced variance
        conservative_fraction = kelly_fraction * self.kelly_multiplier
        
        # Calculate optimal bet as fraction of our stack
        # This is the amount we want to risk (the additional amount beyond current pot)
        optimal_risk = conservative_fraction * myscore
        
        # Ensure we're raising (bet must be > pot)
        if optimal_risk < minbet:
            optimal_risk = minbet
        
        # Round to nearest minbet multiple
        optimal_risk = int(optimal_risk / minbet) * minbet
        
        # Total amount to put in pot = current pot + our additional bet
        total_pot = pot + optimal_risk
        
        return total_pot

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds - Kelly-based bet sizing with GTO decision framework.
        """
        max_bet = min(myscore, oppscore)
        pot_odds = minbet / (pot + minbet) if (pot + minbet) > 0 else 0
        required_equity = pot_odds  # For calling decisions
        
        # Value betting range - use Kelly sizing
        if card > self.VALUE_THRESHOLD:
            kelly_bet = self.fractional_kelly(card, myscore, minbet, pot)
            if kelly_bet is not None:
                # Ensure we're raising (bet > pot) and respect max_bet
                if kelly_bet > pot:
                    return min(kelly_bet, max_bet)
                else:
                    # Kelly suggests calling, but we have a strong hand - raise minimum
                    return min(pot + minbet, max_bet)
            else:
                # Shouldn't happen with strong hands, but fallback
                return min(pot + minbet, max_bet)
        
        # Bluffing range - use GTO bluffing frequency
        elif card < self.BLUFF_THRESHOLD:
            if random.random() < pot_odds:
                # Bluff with minimum raise
                bet_amount = pot + minbet
                return min(bet_amount, max_bet)
            else:
                return 0  # Fold
        
        # Medium strength hands - use Kelly for sizing if positive EV
        elif card > 0.5:
            # Positive EV - consider Kelly sizing or call
            kelly_bet = self.fractional_kelly(card, myscore, minbet, pot)
            if kelly_bet is not None and kelly_bet > pot:
                # Kelly suggests a raise
                return min(kelly_bet, max_bet)
            else:
                # Call if we have required equity, otherwise fold
                if card >= required_equity:
                    return pot  # Call
                else:
                    return 0  # Fold
        
        # Weak hands - fold unless we have good pot odds
        elif card < self.FOLD_THRESHOLD:
            # Check if pot odds justify a call
            if card >= required_equity:
                return pot  # Call with good pot odds
            else:
                return 0  # Fold
        
        # Borderline medium hands - call
        else:
            if card >= required_equity:
                return pot  # Call
            else:
                return 0  # Fold

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        """The game is over."""
        pass
