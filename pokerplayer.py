class PokerPlayer:
    def __init__(self):
        """Initialize my internal variables."""
        # TODO: fill in your code here
        pass

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
        # TODO: fill in your code here
        pass

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds.

        card     - my card
        myscore  - my score
        oppscore - my opponent's score
        minbet   - the smallest bet increase that I am allowed make
        pot      - contains the current bid.
        """
        # TODO: fill in your code here
        # TODO: set bet to your desired bet amount
        return pot + minbet

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
        if iwon:
            if oppcard is None:
                # opponent folded. I don't get to see opponent's card.
                # TODO: fill in your code here
                pass
            else:
                # I won by call. oppcard contains opponent's card.
                # TODO: fill in your code here
                pass
        else:
            if oppcard is None:
                # I folded. I don't get to see opponent's card.
                # TODO: fill in your code here
                pass
            else:
                # I lost by call. oppcard contains opponent's card.
                # TODO: fill in your code here
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
