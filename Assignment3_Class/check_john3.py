import sys
import os
# Ensure we can import opponents
sys.path.append(os.getcwd())

from opponents import John3
from opponents.basic_players import AllIn

p = John3()
print(f"John3 instantiated: {p}")
print(f"Has bet method: {hasattr(p, 'bet')}")

# Simulate a call
# card, myscore, oppscore, minbet, pot
action = p.bet(0.5, 100, 100, 1, 2)
print(f"Action on 0.5: {action}")

