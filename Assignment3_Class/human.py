import random
import randomTexas as rt
from opponents import AllIn, John1, John3, training_opponents

### Use input from the terminal to allow a human player to play
### against the computer opponents.

# ANSI colors
if __import__('sys').stdout.isatty():
    RED = "\033[0;31m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    BOLD = "\033[1m"
    END = "\033[0m"
else:
    RED = ''
    YELLOW = ''
    LIGHT_BLUE = ''
    PURPLE = ''
    CYAN = ''
    BOLD = ''
    END = ''

class HumanPlayer:
    def __init__(self):
        self.status('Welcome to Random Number Texas Hold\'em!')

    def status(self, msg):
        print(f'{RED}** {msg}{END}')

    def info(self, msg):
        print(f'{YELLOW}-- {msg}{END}')

    def i_do(self, msg):
        print(f'{CYAN}>> {msg}{END}')

    def opp_does(self, msg):
        print(f'{CYAN}<< {msg}{END}')

    def help(self, msg):
        print(f'%% {msg}')

    def announce_opening_bets(self, bigblind, myscore, oppscore, minbet):
        # We need to properly handle the special cases when scores get
        # lower than minbet * 2.
        minscore = min(myscore, oppscore)
        small_blind_text = small_blind_bet = min(minbet, minscore)
        if small_blind_bet < minbet:
            small_blind_text = f'{small_blind_bet} due to insufficient points'
        big_blind_text = big_blind_bet = min(minbet*2, minscore)
        if big_blind_bet < minbet*2:
            big_blind_text = f'{big_blind_bet} due to insufficient points'
        # Announce what happened in the opening bets.
        if bigblind:
            self.info('Opponent is the small blind.')
            self.opp_does(f'Opponent raises the bet to {BOLD}{small_blind_text}{END}.')
            if big_blind_bet > small_blind_bet:
                self.i_do(f'You raise the bet to {BOLD}{big_blind_text}{END}.')
            else:
                self.i_do('You {BOLD}call{END} due to insufficient points.')
        else:
            self.info('You are the small blind.')
            self.i_do(f'You {BOLD}raise{END} the bet to {small_blind_text}.')
            if big_blind_bet > small_blind_bet:
                self.opp_does(f'Opponent {BOLD}raises{END} the bet to {BOLD}{big_blind_text}{END}.')
            else:
                self.opp_does(f'Opponent {BOLD}calls{END} due to insufficient points.')

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        print()
        self.status('New hand')
        self.status(f'    Your score : {myscore}')
        self.status(f'Opponent score : {oppscore}')
        self.status(f'   Minimum bet : {minbet}')
        input('%% Press enter to start> ')
        self.announce_opening_bets(bigblind, myscore, oppscore, minbet)
        self.role = 'big' if bigblind else 'small'
        self.i_raised = self.role == 'big'
        self.lastPot = minbet*2
        self.mycard = card

    def bet(self, card, myscore, oppscore, minbet, pot):
        if pot > self.lastPot:
            self.opp_does(f'Opponent {BOLD}raises{END} the bet to {BOLD}{pot}{END}.')
        elif self.role == 'big':
            self.opp_does(f'Opponent {BOLD}calls{END}.')
        else:
            # I am the small blind and the opponent has raised to
            # minbet*2. No need to print a message.
            pass
        self.info(f'Your card is {card}')
        while True:
            choice = input('%% Your bet (h for help)> ')
            choice = choice.strip()
            if choice == '':
                continue
            elif choice[0] == 'h':
                self.help('To fold enter 0')
                self.help(f'To call enter {pot}')
                self.help(f'To raise enter a value larger than {pot}')
            else:
                try:
                    amount = float(choice)
                    break
                except ValueError:
                    self.help(f'Cannot parse "{choice}".')
        if amount > myscore:
            amount = myscore
        self.i_raised = False
        if amount < pot:
            self.i_do(f'You {BOLD}fold{END}.')
        elif amount == pot:
            self.i_do(f'You {BOLD}call{END}.')
        else:
            self.i_do(f'You {BOLD}raise{END} the bet to {BOLD}{amount}{END}.')
            self.i_raised = True
        self.lastPot = pot
        return amount

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        if oppcard:
            if self.i_raised:
                self.opp_does(f'Opponent {BOLD}calls{END}.')
            else:
                # I must have called. No need to print a message.
                pass
        else:
            if iwon:
                self.opp_does(f'Opponent {BOLD}folds{END}.')

        self.info('End of hand.')
        if iwon:
            self.info('You won.')
        else:
            self.info('Your opponent won.')
        self.info(f'    Your card : {self.mycard}')
        self.info(f'Opponent card : {oppcard}')
        self.info(f'     Winnings : {winnings}')
        input('%% Press enter to continue> ')

# Play one game against John1 where players start with 20 points.
winner = rt.RandomNumberTexasHoldem(
    p1 = HumanPlayer(),
    p2 = John1(),
    points = 20,
    rng = random.Random()
)
if winner == 1:
    print('You are the winner!')
else:
    print('Your opponent is the winner. Good game!')
