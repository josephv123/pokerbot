# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based assignment for Psychology 213 (Human Information Processing and AI) focused on creating an AI player for a simplified poker game called "Random Number Texas Hold'Em". Students must implement a competitive poker bot that plays against 90+ opponent bots created by past students.

## Implementation Progress Tracking

**`researchProgress.md`** - Comprehensive implementation roadmap and progress tracker:

- Contains a Directed Acyclic Graph (DAG) structure for building poker bots incrementally
- Defines 5 levels of bot complexity: Baselines (L0), Foundation (L1), GTO Core (L2), Opponent Modeling (L3), Adaptive/Exploitative (L4), and Elite Integration (L5)
- Each level builds on previous levels with specific players to implement
- Includes mathematical foundations, strategy details, testing protocols, and expected win rates

**Usage Guidelines:**

- **Always consult this file** before implementing new features to understand the current phase
- **Update this file immediately** after implementing any new player or strategy with:
  - Implementation details (what was built, key decisions made)
  - Test results (win rates against training opponents, performance metrics)
  - Observations (what worked well, what didn't, insights gained)
  - Next steps (what to implement next based on results)
- Track the progression through the DAG by marking completed items
- Use this file to maintain context across development sessions
- Reference specific sections when debugging or optimizing strategies

This file serves as the single source of truth for the implementation plan and progress.

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

## Implementation Constraints and Possibilities

### State Persistence and Scope

**Instance Variables (`self.*`):**

- `__init__()` is called **once per game** (per opponent), creating a new player instance for each matchup
- Instance variables persist **across all hands within a single game** (randomTexas.py:91-92)
- State is automatically reset between different opponents
- Can track unlimited information within a game: opponent behavior patterns, hand history, statistics, etc.

**Global Variables:**

- Technically possible but not recommended (would persist across different opponents and test runs)
- Testing framework creates new instances for each game, indicating clean slate is intended

### Available Information Per Method

**`start(bigblind, card, myscore, oppscore, minbet, pot)`:**

- `bigblind`: Boolean indicating your role (True = Big Blind, False = Small Blind)
- `card`: Your card value (0.0 to 1.0, represents win probability)
- `myscore`, `oppscore`: Current point totals
- `minbet`: Current minimum bet (doubles every 100 hands)
- `pot`: Initial pot size after blinds are posted

**`bet(card, myscore, oppscore, minbet, pot)`:**

- Called multiple times per hand as betting rounds progress
- `pot`: Updated to reflect current bet total
- Other parameters same as `start()`

**`end(iwon, oppcard, myscore, oppscore, minbet, winnings)`:**

- `iwon`: Boolean indicating if you won the hand
- `oppcard`: Opponent's card value **OR `None` if someone folded**
- `myscore`, `oppscore`: Updated scores after the hand
- `winnings`: Points won by the winner
- Critical: You only see opponent's card when neither player folded

### Tracking Capabilities Between Hands

Within a single game (all hands against one opponent), you can track:

- Opponent betting patterns (fold/call/raise frequencies)
- Opponent cards when revealed (not revealed on folds)
- Relationship between opponent bets and their card strength
- Hand count (to track minbet doubling at 100-hand intervals)
- Win/loss history
- Score trajectories
- Any statistical metrics or patterns

### Betting Constraints

**Bet Amount Rules (randomTexas.py:31-37):**

- Must return **TOTAL** pot amount, not incremental raise
- Bets must be multiples of `minbet` (except when all-in at `min(myscore, oppscore)`)
- Invalid bets are rounded down by game engine with warning printed
- Maximum bet is `min(myscore, oppscore)` (player with fewer points)

**Bet Interpretation (randomTexas.py:39-56):**

- `return value < pot`: Fold (lose `oldBetPot`)
- `return value == pot` (after first bet): Call (showdown, higher card wins)
- `return value > pot`: Raise (betting continues)

### Information Limitations

**Opponent Card Visibility:**

- See opponent's card only when hand goes to showdown (neither player folded)
- Never see opponent's card when someone folds (`oppcard = None`)
- Limits ability to detect bluffs, but can infer from betting patterns
- Can correlate revealed cards with betting history to model opponent strategy

**Game State:**

- Both players always know current scores
- Both players know minbet and pot size
- Cannot see opponent's decision-making process
- Cannot communicate between player instances

### What Is Not Allowed

- Modifying files other than `pokerplayer.py`
- Changing method signatures or class interface
- File I/O operations (no reading/writing external data)
- Network access or inter-process communication
- Breaking the four-method interface (`__init__`, `start`, `bet`, `end`)

### Feasible Implementation Approaches

**Stateless Strategies:**

- Card-strength based thresholds (see John1 example)
- Position-aware betting (different strategy for Big/Small Blind)
- Score-differential risk management

**Stateful Strategies (tracking across hands):**

- Opponent behavior modeling (fold/raise frequencies)
- Bayesian inference on opponent strategy
- Adaptive thresholds based on observed patterns
- Hand history analysis
- Exploit detection (identifying exploitable patterns)

**Advanced Techniques:**

- Game theory optimal (GTO) strategies
- Mixed strategies (randomized decisions)
- Counter-strategy selection
- Statistical pattern recognition
- Multi-level opponent modeling

## Performance Benchmarks

- `AllIn`: ~30.4% win rate, very fast (~3.5 seconds)
- `John1`: ~59% win rate (varies by opponent)
- `John3` (reference solution): ~71-72% win rate, slower (~40 seconds)

Grading is based on performance against 89 held-out even-numbered opponents (P002-P178).

**Important**: Only modify `pokerplayer.py` - do not change other files.
