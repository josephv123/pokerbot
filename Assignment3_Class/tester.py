from opponents import AllIn, John1, John3, training_opponents
from pokerplayer import PokerPlayer
from randomTexas import play, pokerTest

# Have John1 play 100 games against the training opponents.
play(John1, training_opponents, ngames=100, verbosity=0)

# Have PokerPlayer play 100 games against all available opponents.
# play(PokerPlayer, [AllIn, John1, John3] + training_opponents, ngames=100, verbosity=2)

# Have John1 play a single game against John3. Specify the random seed for repeatability.
# pokerTest(John1, John3, 1, seed='my_rng_seed', verbosity=1)
