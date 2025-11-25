
import sys
import random
from opponents import John3
from pokerplayer import PokerPlayer
from randomTexas import RandomNumberTexasHoldem

# Monkey patch print to see what's happening inside RandomNumberTexasHoldem if needed
# But better to add prints to PokerPlayer

p1 = PokerPlayer()
p2 = John3()
rng = random.Random(42)

print("Starting debug game...")
result = RandomNumberTexasHoldem(p1, p2, 100, rng)
print(f"Game result: {result}")
print(f"P1 Score: {p1.myscore}, P2 Score: {p1.oppscore}")

