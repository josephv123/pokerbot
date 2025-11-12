# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based assignment for Psychology 213 (Human Information Processing and AI) focused on creating an AI player for a simplified poker game called "Random Number Texas Hold'Em". Students must implement a competitive poker bot that plays against 90+ opponent bots created by past students.

## Game Rules Summary

- Each player starts with 100 points; game ends when one player has all 200 points
- Players alternate between Small Blind (1 point) and Big Blind (2 points) roles
- Each player receives a single card with value uniformly distributed between 0-1 (represents win probability)
- Players can fold, call, or raise in alternating turns
- Every 100 hands, minimum bet doubles
- Maximum bet is limited by the player with fewer points
- All raises must be multiples of the minimum bet (minbet)

## Development Commands

### Running Tests
```bash
# Run from Assignment3_Class directory
cd Assignment3_Class

# Test your player against training opponents (200 games per opponent)
python3 -c "from opponents import training_opponents; from pokerplayer import PokerPlayer; from randomTexas import play; play(PokerPlayer, training_opponents, 200, 0)"

# Quick test against first 5 opponents with verbose output
python3 -c "from opponents import training_opponents; from pokerplayer import PokerPlayer; from randomTexas import play; play(PokerPlayer, training_opponents[0:5], 200, 1)"

# Run the default tester
python3 tester.py

# Play manually against an opponent
python3 human.py
```

### Testing Against Specific Opponents
```python
from opponents import AllIn, John1, John3, training_opponents
from pokerplayer import PokerPlayer
from randomTexas import play, pokerTest

# Test against a single opponent
pokerTest(PokerPlayer, John1, ngames=100, verbosity=1)

# Test with a specific random seed for repeatability
pokerTest(PokerPlayer, John3, ngames=1, seed='my_rng_seed', verbosity=1)
```

### Verbosity Levels
- `verbosity=0`: Only final score and runtime (minimal output)
- `verbosity=1`: Win percentage against each opponent
- `verbosity=2`: Real-time progress updates during games

## Code Architecture

### Core Files

**`pokerplayer.py`** - The main file students edit. Contains the `PokerPlayer` class with four required methods:
- `__init__()`: Initialize internal state/variables before facing an opponent
- `start(bigblind, card, myscore, oppscore, minbet, pot)`: Called at the beginning of each hand
- `bet(card, myscore, oppscore, minbet, pot)`: Returns the total amount to put in pot (NOT incremental)
- `end(iwon, oppcard, myscore, oppscore, minbet, winnings)`: Called after each hand ends

**`randomTexas.py`** - Game engine implementing the poker variant:
- `RandomNumberTexasHoldem(p1, p2, points, rng)`: Runs a complete game between two players
- `pokerTest(p1_class, p2_class, n, verbosity, seed)`: Runs n games and returns win rate
- `play(p1_class, opps, ngames, verbosity)`: Tests a player against multiple opponents

**`tester.py`** - Simple test script that runs PokerPlayer against training opponents

**`human.py`** - Interactive terminal interface for humans to play against bots

### Opponent Structure

**`opponents/basic_players.py`** - Contains example players:
- `John1`: Simple strategy based on card strength vs bet size
- `AllIn`: Always bets entire score every hand

**`opponents/__init__.py`** - Imports training opponents from compiled modules

**`opponents/poker_players_training.*`** - Compiled Python modules containing 90 training opponents (P001-P179, odd numbers) and the reference solution John3. Platform-specific binaries for Windows, Linux, macOS and Python 3.11-3.13.

### Key Implementation Details

**Bet Return Value**: The `bet()` method must return the TOTAL amount to put in the pot, not an increment. Returning less than the current pot is interpreted as a fold.

**Bet Validation**: Bets must be multiples of `minbet`. The game engine will round down invalid bets and print a warning.

**Opponent Card Visibility**: The `oppcard` parameter in `end()` is `None` if someone folded, otherwise contains the opponent's actual card value.

**State Management**: Use `__init__()` to reset state between opponents. The game creates new player instances for each match.

**Score Tracking**: `myscore` and `oppscore` represent current point totals. When near zero, maximum bet is constrained by the minimum of both scores.

**Blind Roles**: Players alternate roles each hand. Small Blind acts first and starts with 1 point bet; Big Blind responds with 2 point bet.

## Performance Benchmarks

- `AllIn`: ~30.4% win rate, very fast (~3.5 seconds)
- `John1`: ~59% win rate (varies by opponent)
- `John3` (reference solution): ~71-72% win rate, slower (~40 seconds)

Grading is based on performance against 89 held-out even-numbered opponents (P002-P178).

## Assignment Requirements

Students must:
1. Implement a competitive poker bot in `pokerplayer.py`
2. Export logs of GenAI interactions used in development
3. Write a 1-2 page reflection on human decision-making and AI comparison

**Important**: Only modify `pokerplayer.py` - do not change other files.
