class John1:
    def __init__(self):
        """Initialize my internal variables."""
        pass

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        """
        Start a new game of Random Texas.

        bigblind - True if I'm the big blind, False if I'm the small blind.
        card     - contains my card.
        myscore  - my score
        oppscore - my opponent's score
        minbet   - the smallest bet increase that I am allowed make
        pot      - contains the current bid.
        """
        if bigblind:
            self.role = 'big_blind'
        else:
            self.role = 'small_blind'

    def bet(self, card, myscore, oppscore, minbet, pot):
        """
        Betting rounds.

        card     - my card
        myscore  - my score
        oppscore - my opponent's score
        minbet   - the smallest bet increase that I am allowed make
        pot      - contains the current bid.
        """
        if pot > 10.0 * card * minbet:
            # current opponent bet is big relative to my card strength
            if  self.role=='big_blind' and pot == 2 * minbet:
                # but I'm BB, don't fold if bet size is what I have in already
                return pot
            else:
                # otherwise fold
                return 0
        elif pot > 5.0 * card * minbet:
            # opponent bet seems ok, so we leave this bet size as ours (call)
            return pot
        elif pot == oppscore:
            # player is all-in and we are ok with bet sizing thus far
            # so leave bet size as ours (call)
            return pot
        else:
            # otherwise let's bump up the bet size a little (raise)
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
        # not keeping track of anything based on the game's outcome
        pass

class AllIn:
    def __init__(self):
        pass
    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        pass
    def bet(self, card, myscore, oppscore, minbet, pot):
        return myscore
    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        pass
