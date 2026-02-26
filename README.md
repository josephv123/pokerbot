# Poker Bot — Adaptive GTO Player

An AI poker bot built for **Psychology 213: Human Information Processing and AI**. It plays "Random Number Texas Hold'Em" against 90+ opponent bots and achieves a **~71.6–71.9% win rate** against the training set — matching the performance of the provided reference solution (John3).

---

## The Game

**Random Number Texas Hold'Em** is a simplified poker variant designed to isolate decision-making under uncertainty:

- Each player starts with **100 points**; the game ends when one player has all 200
- Each player receives a single card: a float in `[0, 1]` representing their probability of winning a showdown
- Players alternate between **Small Blind** (acts first) and **Big Blind** (acts second)
- Every 100 hands, the **minimum bet doubles**, escalating pressure over time
- Actions: **fold**, **call**, or **raise** (all raises must be multiples of `minbet`)

The core challenge: your card tells you exactly how likely you are to win — but you must decide *how much* to bet, whether to bluff, and how to model your opponent's behavior.

---

## Strategy Design

### 1. GTO Foundation

Betting thresholds are derived from **Game Theory Optimal (GTO) principles** for a simplified one-street game. For a given bet size `B` relative to pot `P`:

- **Bluff range** (`a`, `e`): the lowest cards where bluffing is profitable
- **Value range** (`c`, `f`): the minimum card strength for value betting
- **Call threshold** (`b`, `d`): the Minimum Defense Frequency (MDF) determines when calling is required to prevent profitable opponent bluffing

These thresholds are computed dynamically based on the actual bet size ratio encountered each hand, ensuring correct play across escalating blind levels.

### 2. Opponent Classification

After **15+ observed bet responses**, opponents are classified into one of seven archetypes:

| Type | Description | Detected By |
|---|---|---|
| `folder` | Folds >55% to our bets | High fold rate |
| `caller` | Folds <30% to our bets | Low fold rate |
| `aggressor` | Raises >30% of the time | High raise rate |
| `aggressive_folder` | Folds to bets but bets aggressively when checked to | Moderate fold rate + high aggression |
| `aggressive_caller` | Calls wide and bets aggressively when checked to | Low fold rate + high aggression |
| `hyper_aggressive` | Bets nearly every time we check | Aggression ≥ 90% |
| `allin` | Frequently goes all-in | All-in frequency ≥ 70% within first 30 hands |

### 3. Exploitative Strategy Modes

Each opponent type maps to a tailored strategy with four tunable parameters:

| Mode | `bet_mult` | `bluff_mult` | `value_mult` | `call_mult` | Used Against |
|---|---|---|---|---|---|
| `aggressive` | 5× | 2.5× | 1.10× | 1.15× | Folders |
| `tight` | 2× | 0.3× | 1.0× | 1.0× | Callers, AllIn |
| `trapping` | 2× | 0.5× | 1.15× | 0.85× | Aggressors |
| `trap_aggressive` | 5× | 3.5× | 1.25× | 0.90× | Aggressive folders |
| `aggressive_caller` | 3× | 0.4× | 0.90× | 0.70× | Aggressive callers |
| `hyper_aggressive` | 3× | 1.8× | 1.05× | 0.65× | Hyper-aggressive |
| `balanced` | 3× | 1.5× | 1.05× | 1.05× | Default / adapted opponents |

**Key insight:** ~70% of training opponents are "folders" — opponents who fold far too often to aggression. The default strategy exploits this immediately with oversized bets.

### 4. Adaptive Features

**Drift detection** — A rolling window of the last 40 fold decisions tracks behavioral shifts. If an opponent's recent fold rate diverges from their early baseline by >20%, the bot switches to `balanced` mode to avoid being counter-exploited.

**Bet-card-mean exploitation** — Showdown data is used to build a model of the opponent's *actual betting range*. Once 6+ showdowns are observed, call thresholds are adjusted to beat the opponent's average betting hand rather than relying on fixed GTO values.

**Aggression tracking** — The bot tracks how often opponents bet when checked to, enabling detection of passive-folding vs. aggressive-folding opponents who require fundamentally different strategies.

---

## Performance

| Benchmark | Win Rate |
|---|---|
| vs. `AllIn` | ~30% (expected — AllIn wins by variance) |
| vs. `John1` (basic strategy) | ~59% |
| vs. `John3` (reference solution) | ~50% |
| vs. full training set (90 opponents) | **~71.6–71.9%** |

---

## Opponent Analysis Tool

`analyze_opponents.py` is a standalone research tool that:

1. Profiles every training opponent using a dedicated `AnalysisPlayer` probe
2. Extracts a **5-dimensional feature vector** per opponent:
   - `fold_rate`, `call_rate`, `raise_rate`, `bet_card_mean`, `aggression`
3. Runs **k-means clustering** (k=5) to derive archetype centroids
4. Outputs optimal strategy parameters per cluster as embeddable Python constants

This was used to empirically validate the classification thresholds in `pokerplayer.py` and verify that the opponent archetypes reflect real behavioral clusters in the training set.

---

## Project Structure

```
Assignment3_Class/
├── pokerplayer.py          # Main bot implementation (PokerPlayer class)
├── randomTexas.py          # Game engine
├── opponents/
│   ├── basic_players.py    # John1, AllIn reference bots
│   └── poker_players_training.*  # 90 compiled training opponents (P001–P179)
├── analyze_opponents.py    # Offline opponent clustering tool
├── tester.py               # Quick test runner
├── debug_game.py           # Single-game debugger with fixed seed
└── human.py                # Interactive play against bots
```

---

## Running the Bot

```bash
cd Assignment3_Class

# Full test against all 90 training opponents (200 games each)
python3 -c "from opponents import training_opponents; from pokerplayer import PokerPlayer; from randomTexas import play; play(PokerPlayer, training_opponents, 200, 0)"

# Test against a specific opponent with verbose output
python3 -c "
from opponents import John3
from pokerplayer import PokerPlayer
from randomTexas import pokerTest
pokerTest(PokerPlayer, John3, ngames=200, verbosity=1)
"

# Run the default tester
python3 tester.py

# Play manually against the bot
python3 human.py
```

---

## Implementation Notes

- The `bet()` method returns the **total pot commitment**, not an incremental raise — returning less than the current pot is a fold
- Bets are rounded down to the nearest `minbet` multiple; the game engine warns on violations
- `__init__()` is called fresh for each new opponent matchup, resetting all tracking state
- Strategy parameters are cached per mode to avoid redundant dict creation in tight betting loops
