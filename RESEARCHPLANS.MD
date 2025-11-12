# PLAN 1:

# Ultimate Poker Bot Implementation Plan

## A Directed Acyclic Graph for Winning "Random Number Texas Hold'Em"

**Date:** 2025-11-11
**Objective:** Develop a competitive poker bot that wins 71%+ against diverse opponents in a uniform[0,1] single-card poker variant

---

## Game Analysis & Mathematical Properties

### Core Game Mechanics

This is a **continuous Kuhn poker variant** with the following unique properties:

1. **Card Distribution:** Each player receives a single card uniformly distributed on [0, 1]

   - Card value represents exact win probability at showdown
   - Showdown is deterministic: higher card always wins

2. **Betting Structure:**

   - Small Blind: 1 point (acts first pre-hand)
   - Big Blind: 2 points
   - Minimum bet doubles every 100 hands
   - Maximum bet = min(player1_score, player2_score)
   - All bets must be multiples of minbet

3. **Position Dynamics:**

   - Players alternate SB/BB roles each hand
   - Small Blind acts first in betting
   - No postflop action (single betting round after blinds)

4. **Information Structure:**

   - Perfect information about: own card, scores, pot, minbet
   - Hidden information: opponent's card (revealed only at showdown when neither folds)
   - Historical tracking: Can store all hand histories within a game

5. **Game Termination:** One player accumulates all 200 points

### Key Mathematical Insights from Research

**From Kuhn Poker Theory:**

- Mixed strategies are optimal (no pure strategy equilibrium)
- Bluffing with weak hands and value-betting with strong hands is essential
- Middle-strength hands should fold/call, never raise (polarized strategy)
- Optimal bluffing frequency relates to pot odds offered to opponent

**From Uniform Poker Models (Borel/von Neumann):**

- With uniform[0,1] cards, Nash equilibrium involves threshold strategies
- Position (SB vs BB) significantly impacts optimal thresholds
- Multi-round betting creates complexity requiring indifference conditions

**Key Strategic Principles:**

1. **Polarization:** Raise with strong hands + some weak hands; call/fold with medium
2. **Indifference:** Make opponent indifferent between folding and calling
3. **Exploitability:** GTO is unexploitable but may not maximize win rate
4. **Adaptation:** Exploitative adjustments outperform GTO against non-GTO opponents

---

## Implementation Architecture: The DAG

This plan structures bot development as a directed acyclic graph where each level builds on previous levels. Test each bot thoroughly before advancing.

```
Level 0 (Baselines)
    �
Level 1 (Foundation)
    �
Level 2 (GTO Core)
    �
Level 3 (Opponent Modeling)
    �
Level 4 (Adaptive & Exploitative)
    �
Level 5 (Elite Integration)
```

---

## LEVEL 0: Baseline Players (Benchmarking)

**Purpose:** Establish performance benchmarks and understand opponent spectrum

### B0.1: AllIn Player (Already Exists)

- **Strategy:** Bet entire stack every hand
- **Expected Win Rate:** ~30%
- **Purpose:** Lower bound benchmark
- **Test:** Verify 30% win rate

### B0.2: FoldBot

- **Strategy:** Always fold unless Big Blind with card > 0.9
- **Expected Win Rate:** ~10%
- **Purpose:** Worst-case baseline
- **Implementation Time:** 5 minutes

### B0.3: CallBot

- **Strategy:** Always call, never raise
- **Expected Win Rate:** ~45-50%
- **Purpose:** Passive strategy baseline
- **Implementation Time:** 5 minutes

### B0.4: John1 (Already Exists)

- **Strategy:** Card-strength threshold with pot-size consideration
- **Expected Win Rate:** ~59%
- **Purpose:** Simple heuristic baseline
- **Test:** Verify 59% win rate

**Deliverable:** Understand the 30-59% performance range

---

## LEVEL 1: Foundation Players (Core Strategies)

**Purpose:** Implement fundamental poker concepts with position awareness

### F1.1: SimpleThreshold

**Dependencies:** None
**Core Concept:** Basic threshold strategy with position adjustment

**Strategy:**

- Fold if card < 0.3
- Call if card between 0.3-0.7
- Raise if card > 0.7
- Adjust thresholds by 0.1 based on position (BB more aggressive)

**Implementation:**

```python
def bet(self, card, myscore, oppscore, minbet, pot):
    threshold_fold = 0.3 if self.is_bigblind else 0.35
    threshold_raise = 0.7 if self.is_bigblind else 0.65

    if card < threshold_fold and pot > 2 * minbet:
        return 0  # fold
    elif card > threshold_raise:
        return pot + minbet  # raise
    else:
        return pot  # call
```

**Testing:** Expect 55-60% win rate
**Time:** 30 minutes

### F1.2: PotOddsPlayer

**Dependencies:** F1.1
**Core Concept:** Integrate pot odds into decision-making

**Strategy:**

- Calculate implied pot odds
- Compare card strength to odds needed
- Fold if card < pot_odds_threshold
- Use Kelly Criterion for bet sizing with strong hands

**Key Calculation:**

```python
pot_odds = pot / (pot + minbet)
required_equity = pot / (2 * pot + minbet)
should_call = card > required_equity
```

**Testing:** Expect 60-63% win rate
**Time:** 1 hour

### F1.3: PositionAware

**Dependencies:** F1.2
**Core Concept:** Exploit positional advantage

**Strategy:**

- Small Blind (acts first): Tighter range, more caution
- Big Blind (invested 2x): Defend more aggressively
- Adjust fold/call/raise thresholds by position
- Track which position wins more

**Position Adjustments:**

- SB: Fold <0.35, Call 0.35-0.75, Raise >0.75
- BB: Fold <0.25, Call 0.25-0.70, Raise >0.70

**Testing:** Expect 62-65% win rate
**Time:** 1 hour

---

## LEVEL 2: GTO Core Players (Game Theory Optimal)

**Purpose:** Implement unexploitable mixed strategies based on game theory

### G2.1: MixedStrategyPlayer

**Dependencies:** F1.3
**Core Concept:** Introduce randomization to prevent exploitation

**Strategy:**

- Use mixed strategies for marginal decisions
- Implement bluffing with weak hands (polarized ranges)
- Value bet with strong hands
- Randomize action with medium hands

**Bluffing Logic:**

```python
import random

def should_bluff(card, pot, minbet):
    # Bluff with bottom 15% of range
    if card < 0.15:
        bluff_frequency = pot / (pot + minbet)  # Pot odds based
        return random.random() < bluff_frequency
    return False

def bet_decision(card, pot, minbet):
    if card > 0.75:  # Strong hands
        return pot + minbet  # Always raise
    elif card < 0.15 and should_bluff(card, pot, minbet):
        return pot + minbet  # Bluff raise
    elif card < 0.30:
        return 0  # Fold weak non-bluffs
    else:
        return pot  # Call with medium
```

**Testing:** Expect 64-67% win rate
**Time:** 2 hours

### G2.2: OptimalThresholdPlayer

**Dependencies:** G2.1
**Core Concept:** Calculate mathematically optimal thresholds

**Research-Based Thresholds (from Kuhn poker literature):**

- **Bluff threshold:** Bottom 15-20% of range
- **Value threshold:** Top 25-30% of range
- **Fold threshold:** Bottom 30-40% when facing raises
- **Call threshold:** Middle 40-50% of range

**Implementation:**

```python
class OptimalThresholdPlayer:
    # Derived from continuous Kuhn poker theory
    BLUFF_THRESHOLD = 0.18
    FOLD_THRESHOLD = 0.35
    VALUE_THRESHOLD = 0.72

    def bet(self, card, myscore, oppscore, minbet, pot):
        pot_odds = minbet / (pot + minbet)

        # Value betting range
        if card > self.VALUE_THRESHOLD:
            # Size bet based on card strength
            bet_size = pot + minbet * (1 + int((card - 0.7) / 0.1))
            return min(bet_size, min(myscore, oppscore))

        # Bluffing range
        elif card < self.BLUFF_THRESHOLD:
            if random.random() < pot_odds:  # Frequency = pot odds
                return pot + minbet
            else:
                return 0  # Fold

        # Folding range (weak non-bluffs)
        elif card < self.FOLD_THRESHOLD and pot > 3 * minbet:
            return 0

        # Calling range (medium strength)
        else:
            return pot
```

**Testing:** Expect 66-69% win rate
**Time:** 2 hours

### G2.3: EquilibriumPlayer

**Dependencies:** G2.2
**Core Concept:** Full Nash equilibrium approximation for this variant

**Strategy:**

- Implement indifference conditions for opponent
- Balance bluffing and value betting frequencies
- Position-specific equilibrium adjustments
- Dynamic threshold adjustment based on pot size

**Key Formulas:**

```python
# Make opponent indifferent to calling
# EV(call) = EV(fold)
# P(bluff) * pot - P(value) * (pot + call) = 0
# Optimal bluff frequency = call_amount / (pot + call_amount)

def equilibrium_bluff_frequency(pot, minbet):
    return minbet / (pot + minbet)

def equilibrium_value_frequency(pot, minbet):
    # Complement to maintain range balance
    return 1 - equilibrium_bluff_frequency(pot, minbet)
```

**Advanced Features:**

- Multi-level indifference (accounting for reraises)
- Bet sizing to maximize value/bluff efficiency
- Stack-size adjusted strategies (ICM-like considerations)

**Testing:** Expect 68-71% win rate
**Time:** 3 hours

---

## LEVEL 3: Opponent Modeling Players

**Purpose:** Track and exploit opponent tendencies

### O3.1: StatisticalTracker

**Dependencies:** G2.2
**Core Concept:** Collect opponent statistics

**Tracked Metrics:**

```python
class OpponentStats:
    def __init__(self):
        self.hands_played = 0
        self.folds = 0
        self.calls = 0
        self.raises = 0

        # Showdown data
        self.showdowns = []  # List of (their_card, their_bet, result)

        # Fold data
        self.fold_situations = []  # List of (pot_size, their_card_estimated)

        # Aggression metrics
        self.aggression_factor = 0.0  # (raises + bets) / (calls)
        self.vpip = 0.0  # Voluntarily put in pot %
        self.pfr = 0.0   # Pre-flop raise %
```

**Data Collection in `end()` method:**

```python
def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
    self.hands_played += 1

    if oppcard is not None:  # Showdown occurred
        self.showdowns.append({
            'opp_card': oppcard,
            'winnings': winnings,
            'pot': winnings,
            'hand_num': self.hands_played
        })
```

**Testing:** Expect 66-69% (same as G2.2 base, needed for next level)
**Time:** 1.5 hours

### O3.2: BasicAdaptivePlayer

**Dependencies:** O3.1
**Core Concept:** Simple adjustments based on opponent stats

**Strategy:**

- Against aggressive opponents (high raise %): Tighten calling range, trap more
- Against passive opponents (low raise %): Bluff more, value bet thinner
- Against tight opponents (high fold %): Increase bluff frequency
- Against loose opponents (low fold %): Reduce bluffs, value bet more

**Implementation:**

```python
def adjust_thresholds(self, opponent_stats):
    base_fold_threshold = 0.35
    base_bluff_threshold = 0.18
    base_value_threshold = 0.72

    # Calculate opponent tendencies
    fold_frequency = opponent_stats.folds / opponent_stats.hands_played
    aggression = opponent_stats.aggression_factor

    # Adjustments
    if fold_frequency > 0.5:  # Tight opponent
        self.bluff_threshold += 0.05  # Bluff more
        self.value_threshold -= 0.05   # Value bet wider

    if aggression > 2.0:  # Aggressive opponent
        self.fold_threshold += 0.05   # Fold less (call more)
        self.call_threshold += 0.05   # Trap with medium hands
```

**Testing:** Expect 68-71% win rate
**Time:** 2 hours

### O3.3: BayesianModelingPlayer

**Dependencies:** O3.2
**Core Concept:** Bayesian inference of opponent strategy

**Strategy:**

- Model opponent as mixture of archetypes
- Update beliefs after each hand using Bayes' theorem
- Adapt strategy based on most likely opponent type

**Opponent Archetypes:**

```python
ARCHETYPES = {
    'aggressive': {
        'bluff_freq': 0.30,
        'value_threshold': 0.65,
        'fold_threshold': 0.25
    },
    'tight': {
        'bluff_freq': 0.10,
        'value_threshold': 0.80,
        'fold_threshold': 0.45
    },
    'loose': {
        'bluff_freq': 0.25,
        'value_threshold': 0.60,
        'fold_threshold': 0.20
    },
    'gto': {
        'bluff_freq': 0.18,
        'value_threshold': 0.72,
        'fold_threshold': 0.35
    }
}
```

**Bayesian Update:**

```python
def update_beliefs(self, observation):
    # P(archetype | observation)  P(observation | archetype) * P(archetype)
    for archetype in self.beliefs:
        likelihood = self.calculate_likelihood(observation, archetype)
        self.beliefs[archetype] *= likelihood

    # Normalize
    total = sum(self.beliefs.values())
    for archetype in self.beliefs:
        self.beliefs[archetype] /= total

def calculate_likelihood(self, observation, archetype):
    # How likely is this observation given this archetype?
    # observation = {'action': 'raise', 'pot': 4, 'card': 0.45}
    expected_action = self.predict_action(observation['card'],
                                          observation['pot'],
                                          archetype)
    if expected_action == observation['action']:
        return 0.8  # High likelihood
    else:
        return 0.2  # Low likelihood
```

**Counter-Strategy Selection:**

```python
def select_counter_strategy(self):
    most_likely = max(self.beliefs, key=self.beliefs.get)

    counters = {
        'aggressive': 'trapping',  # Call more, trap with strong hands
        'tight': 'bluffing',       # Bluff more frequently
        'loose': 'value_heavy',    # Value bet more, bluff less
        'gto': 'gto'               # Play GTO back
    }

    return counters[most_likely]
```

**Testing:** Expect 70-73% win rate
**Time:** 4 hours

---

## LEVEL 4: Adaptive & Exploitative Players

**Purpose:** Advanced exploitation of specific opponent weaknesses

### A4.1: ExploitationEngine

**Dependencies:** O3.3
**Core Concept:** Identify and maximally exploit specific patterns

**Exploitation Strategies:**

**1. Exploit Predictable Folders:**

```python
def exploit_folder(self, opponent_stats):
    # If opponent folds to >60% of raises
    if opponent_stats.fold_to_raise_pct > 0.60:
        # Bluff aggressively
        self.bluff_threshold = 0.35  # Bluff with bottom 35%
        self.min_bluff_size = minbet  # Small bluffs work
```

**2. Exploit Calling Stations:**

```python
def exploit_caller(self, opponent_stats):
    # If opponent calls >70% and rarely raises
    if opponent_stats.call_pct > 0.70 and opponent_stats.raise_pct < 0.15:
        # Never bluff, value bet thin
        self.bluff_threshold = 0.0
        self.value_threshold = 0.55  # Value bet much wider
```

**3. Exploit Aggressive Maniacs:**

```python
def exploit_maniac(self, opponent_stats):
    # If opponent raises >50% of hands
    if opponent_stats.raise_pct > 0.50:
        # Trap with strong hands, fold weak
        self.slow_play_threshold = 0.85  # Trap with top hands
        self.fold_threshold = 0.45  # Fold medium more
```

**4. Exploit Pattern-Based Players:**

```python
def detect_patterns(self, opponent_history):
    # Detect if opponent always bluffs after losing
    recent_losses = [h for h in opponent_history[-5:] if not h['won']]
    if len(recent_losses) >= 2:
        next_hand_bluff_likelihood = 0.7
        # Call lighter on next hand
```

**Testing:** Expect 71-74% win rate
**Time:** 3 hours

### A4.2: MetaStrategyPlayer

**Dependencies:** A4.1
**Core Concept:** Strategy selection based on game state

**Multiple Sub-Strategies:**

```python
class MetaStrategyPlayer:
    def __init__(self):
        self.strategies = {
            'gto': EquilibriumPlayer(),
            'exploitative': ExploitationEngine(),
            'risk_averse': ConservativePlayer(),
            'aggressive': AggressivePlayer()
        }
        self.current_strategy = 'gto'
```

**Strategy Selection Logic:**

```python
def select_strategy(self, game_state):
    # When ahead by a lot, play safe
    if game_state['score_advantage'] > 50:
        return 'risk_averse'

    # When behind, play aggressive
    elif game_state['score_advantage'] < -50:
        return 'aggressive'

    # When exploitation is working
    elif self.recent_win_rate > 0.75:
        return 'exploitative'

    # Default to GTO
    else:
        return 'gto'
```

**Risk Management:**

```python
def adjust_for_risk(self, bet, myscore, oppscore):
    # Kelly Criterion: bet fraction of bankroll proportional to edge
    edge = self.estimated_win_probability - 0.5
    kelly_fraction = 2 * edge  # Simplified Kelly

    max_safe_bet = myscore * kelly_fraction
    return min(bet, max_safe_bet)
```

**Testing:** Expect 72-75% win rate
**Time:** 3 hours

### A4.3: DynamicThresholdPlayer

**Dependencies:** A4.2
**Core Concept:** Continuously adjust thresholds based on success

**Learning System:**

```python
class DynamicThresholdPlayer:
    def __init__(self):
        # Start with GTO thresholds
        self.thresholds = {
            'fold': 0.35,
            'bluff': 0.18,
            'value': 0.72
        }

        # Track performance of each threshold
        self.threshold_performance = defaultdict(lambda: {'wins': 0, 'total': 0})

    def update_thresholds(self):
        # Gradient-based adjustment
        for threshold_name, data in self.threshold_performance.items():
            if data['total'] > 10:  # Minimum sample size
                win_rate = data['wins'] / data['total']

                if win_rate < 0.45:  # Performing poorly
                    # Adjust threshold
                    if threshold_name == 'fold':
                        self.thresholds['fold'] += 0.02  # Fold less
                    elif threshold_name == 'bluff':
                        self.thresholds['bluff'] -= 0.02  # Bluff less
```

**Testing:** Expect 72-75% win rate
**Time:** 4 hours

---

## LEVEL 5: Elite Integration Players

**Purpose:** Combine best elements from all previous levels

### E5.1: HybridPlayer

**Dependencies:** All Level 4 players
**Core Concept:** Ensemble method combining multiple strategies

**Strategy:**

- Run multiple sub-players in parallel (simulation)
- Weight decisions by each player's historical performance
- Use voting/averaging for final decision

**Implementation:**

```python
class HybridPlayer:
    def __init__(self):
        self.sub_players = [
            EquilibriumPlayer(),
            BayesianModelingPlayer(),
            ExploitationEngine(),
            MetaStrategyPlayer()
        ]

        self.player_weights = [0.25, 0.25, 0.25, 0.25]  # Equal initially

    def bet(self, card, myscore, oppscore, minbet, pot):
        decisions = []

        # Get each sub-player's decision
        for player in self.sub_players:
            decision = player.bet(card, myscore, oppscore, minbet, pot)
            decisions.append(decision)

        # Weighted average
        final_decision = sum(d * w for d, w in zip(decisions, self.player_weights))

        # Round to valid bet
        return int(final_decision / minbet) * minbet

    def update_weights(self, result):
        # Increase weight of players whose decision would have performed better
        pass
```

**Testing:** Expect 73-76% win rate
**Time:** 3 hours

### E5.2: AdaptiveHybridPlayer

**Dependencies:** E5.1
**Core Concept:** Hybrid player with dynamic weight adjustment

**Weight Update System:**

```python
def update_weights(self, hand_result):
    # Track which sub-player's decision was closest to optimal
    optimal_decision = self.calculate_optimal_decision_hindsight(hand_result)

    for i, player in enumerate(self.sub_players):
        player_decision = player.last_decision
        error = abs(player_decision - optimal_decision)

        # Reduce weight if error is high
        if error > threshold:
            self.player_weights[i] *= 0.95
        else:
            self.player_weights[i] *= 1.05

    # Normalize weights
    total = sum(self.player_weights)
    self.player_weights = [w / total for w in self.player_weights]
```

**Testing:** Expect 74-77% win rate
**Time:** 2 hours

### E5.3: UltimatePlayer

**Dependencies:** E5.2
**Core Concept:** Best-of-breed integration with advanced features

**Comprehensive Features:**

1. **Multi-Level Opponent Modeling:**

   - Bayesian archetype classification
   - Pattern recognition for exploitable behaviors
   - Meta-game awareness (opponent adaptation detection)

2. **Dynamic Strategy Selection:**

   - GTO base with exploitative overlays
   - Risk-adjusted bet sizing
   - Score-differential awareness

3. **Advanced Betting:**

   - Pot odds optimization
   - Implied odds calculation
   - Stack-size adjusted aggression

4. **Learning System:**
   - Within-game adaptation
   - Cross-game learning (if allowed by framework)
   - Continuous threshold optimization

**Implementation Structure:**

```python
class UltimatePlayer:
    def __init__(self):
        # Core components
        self.gto_engine = EquilibriumPlayer()
        self.exploitation_engine = ExploitationEngine()
        self.opponent_model = BayesianModelingPlayer()
        self.meta_strategy = MetaStrategyPlayer()

        # State tracking
        self.game_state = GameState()
        self.opponent_profile = OpponentProfile()

        # Performance tracking
        self.decision_history = []
        self.performance_metrics = {}

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        self.game_state.update(bigblind, card, myscore, oppscore, minbet, pot)
        self.is_bigblind = bigblind
        self.hand_card = card

    def bet(self, card, myscore, oppscore, minbet, pot):
        # Update game state
        self.game_state.update_betting(pot)

        # Get opponent profile
        opponent_type = self.opponent_model.classify_opponent()

        # Select strategy
        if self.should_exploit(opponent_type):
            strategy = self.exploitation_engine
        else:
            strategy = self.gto_engine

        # Get base decision
        base_decision = strategy.bet(card, myscore, oppscore, minbet, pot)

        # Apply risk management
        risk_adjusted = self.meta_strategy.adjust_for_risk(
            base_decision, myscore, oppscore
        )

        # Apply score-differential adjustments
        final_decision = self.adjust_for_score_diff(
            risk_adjusted, myscore, oppscore
        )

        return final_decision

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        # Update opponent model
        if oppcard is not None:
            self.opponent_model.observe(oppcard, winnings)

        # Update performance metrics
        self.update_metrics(iwon, winnings)

        # Learn from result
        self.learn_from_hand(iwon, oppcard, winnings)

    def should_exploit(self, opponent_type):
        # Exploit if confident in opponent model
        return self.opponent_model.confidence > 0.7

    def adjust_for_score_diff(self, bet, myscore, oppscore):
        score_diff = myscore - oppscore

        # When ahead significantly, play more conservatively
        if score_diff > 50:
            return min(bet, myscore * 0.3)  # Risk less

        # When behind, need to take more risks
        elif score_diff < -50:
            return min(bet, myscore * 0.5)  # Risk more

        return bet
```

**Testing:** Expect 75-78%+ win rate
**Time:** 5 hours

---

## Testing & Iteration Framework

### Testing Protocol for Each Player

**1. Quick Test (First 5 Training Opponents)**

```bash
python3 -c "from opponents import training_opponents; from pokerplayer import PokerPlayer; from randomTexas import play; play(PokerPlayer, training_opponents[0:5], 200, 1)"
```

- Takes ~2-3 minutes
- Gives quick feedback on basic performance
- Target: Minimum 55% against first 5

**2. Full Training Test (All 90 Training Opponents)**

```bash
python3 -c "from opponents import training_opponents; from pokerplayer import PokerPlayer; from randomTexas import play; play(PokerPlayer, training_opponents, 200, 0)"
```

- Takes ~30-40 minutes
- Official training performance metric
- Target: 71%+ to match John3

**3. Detailed Analysis Test**

```bash
python3 -c "from opponents import training_opponents; from pokerplayer import PokerPlayer; from randomTexas import play; play(PokerPlayer, training_opponents, 200, 2)"
```

- Shows win rate against each opponent
- Identifies weak matchups
- Use for targeted improvements

**4. Specific Opponent Deep Dive**

```python
from opponents import John1, John3, training_opponents
from pokerplayer import PokerPlayer
from randomTexas import pokerTest

# Test specific opponent with high verbosity
pokerTest(PokerPlayer, training_opponents[0], ngames=1000, verbosity=2)

# Test with fixed seed for reproducibility
pokerTest(PokerPlayer, John3, ngames=100, seed='test_seed', verbosity=1)
```

### Performance Tracking Spreadsheet

Create a tracking document:

| Player Name     | Level | Quick Test (5 opps) | Full Test (90 opps) | Time (seconds) | Notes                     |
| --------------- | ----- | ------------------- | ------------------- | -------------- | ------------------------- |
| AllIn           | B0.1  | 35%                 | 30%                 | 3.5s           | Baseline                  |
| John1           | B0.4  | 60%                 | 59%                 | 10s            | Simple heuristic          |
| SimpleThreshold | F1.1  | ?                   | ?                   | ?              | Position-aware thresholds |
| ...             | ...   | ...                 | ...                 | ...            | ...                       |

### Iteration Strategy

**For Each Player Implementation:**

1. **Implement** (estimated time from plan)
2. **Quick Test** against first 5 opponents
3. **Debug** if performance is below expectations
4. **Full Test** once quick test looks good
5. **Analyze** which opponents are problematic
6. **Iterate** with targeted improvements
7. **Document** insights and move to next level

**Key Decision Points:**

- If a Level 1 player doesn't beat John1 (59%), revisit implementation
- If a Level 2 player doesn't reach 65%+, debug before advancing
- If a Level 3 player doesn't reach 70%+, revisit opponent modeling
- If a Level 4 player doesn't reach 72%+, check exploitation logic
- Level 5 is where you target 75%+

---

## Advanced Concepts & Theory

### 1. Optimal Bluffing Mathematics

**Indifference Principle:**

```
Make opponent indifferent between calling and folding
EV(call) = EV(fold)

When opponent calls:
EV = P(we have bluff) * pot - P(we have value) * (pot + call_amount)

Set EV(call) = 0:
P(bluff) * pot = P(value) * (pot + call_amount)

Optimal bluff frequency:
P(bluff) / (P(bluff) + P(value)) = call_amount / (pot + call_amount)
```

**Application:**

```python
def optimal_bluff_frequency(pot, minbet):
    call_amount = minbet
    return call_amount / (pot + call_amount)

# Example: pot = 4, minbet = 1
# Optimal bluff freq = 1/(4+1) = 20%
# For every 4 value bets, make 1 bluff
```

### 2. Bet Sizing Theory

**Polarized Betting:**

- Large bets with polarized range (very strong or very weak)
- Small bets with merged range (medium strength)

**Implementation:**

```python
def calculate_bet_size(card, pot, minbet, myscore, oppscore):
    max_bet = min(myscore, oppscore)

    if card > 0.85:  # Very strong
        # Large bet (2-3x pot) to get value
        return min(pot + 3 * minbet, max_bet)

    elif card > 0.72:  # Strong
        # Medium bet (1-2x minbet) for value
        return min(pot + 2 * minbet, max_bet)

    elif card < 0.18:  # Bluffing
        # Small bet (1x minbet) for fold equity
        return pot + minbet

    else:  # Medium strength
        # Call or check
        return pot
```

### 3. ICM-like Considerations

**Score Differential Impact:**

When far ahead:

- Avoid unnecessary risks
- Force opponent into mistakes
- Play more conservatively

When far behind:

- Must take risks to catch up
- Increase variance
- Bluff more, go for big pots

**Implementation:**

```python
def risk_adjustment_factor(myscore, oppscore):
    # Returns multiplier for bet sizing
    score_diff = myscore - oppscore
    total_points = myscore + oppscore

    advantage_ratio = score_diff / total_points

    if advantage_ratio > 0.3:  # Ahead by 30%+
        return 0.7  # Bet more conservatively
    elif advantage_ratio < -0.3:  # Behind by 30%+
        return 1.3  # Bet more aggressively
    else:
        return 1.0  # Normal betting
```

### 4. Opponent Categorization Framework

**Four Main Archetypes:**

**Archetype 1: Tight-Passive**

- Folds often
- Rarely raises
- Only bets with strong hands
- **Counter:** Bluff frequently, value bet thin

**Archetype 2: Loose-Aggressive**

- Rarely folds
- Raises often
- Bluffs frequently
- **Counter:** Trap with strong hands, fold weak, call light

**Archetype 3: Tight-Aggressive**

- Folds medium hands
- Raises with strong and some weak
- Plays close to GTO
- **Counter:** Play GTO back, small exploitative adjustments

**Archetype 4: Loose-Passive**

- Calls too much
- Rarely raises
- Poor hand selection
- **Counter:** Never bluff, value bet everything

**Classification Algorithm:**

```python
def classify_opponent(stats):
    fold_freq = stats.folds / stats.hands_played
    raise_freq = stats.raises / stats.hands_played

    is_tight = fold_freq > 0.45
    is_aggressive = raise_freq > 0.30

    if is_tight and is_aggressive:
        return 'tight-aggressive'
    elif is_tight and not is_aggressive:
        return 'tight-passive'
    elif not is_tight and is_aggressive:
        return 'loose-aggressive'
    else:
        return 'loose-passive'
```

### 5. Minbet Doubling Strategy

**Key Insight:** Minbet doubles every 100 hands

**Strategic Implications:**

- Early game (minbet=1): Bets are small relative to stacks, can play more hands
- Mid game (minbet=2,4): Normal poker dynamics
- Late game (minbet=8,16+): Bets become larger relative to remaining stack

**Adaptation:**

```python
def adjust_for_minbet_stage(minbet, myscore):
    # Early game: minbet <= 2
    if minbet <= 2:
        return 'wide_range'  # Play more hands

    # Mid game: 2 < minbet <= 8
    elif minbet <= 8:
        return 'balanced'  # Normal strategy

    # Late game: minbet > 8
    else:
        # Bets are large relative to stacks
        if myscore < 20:
            return 'push_fold'  # Simplified strategy
        else:
            return 'careful'  # Avoid variance
```

### 6. Unexploitability vs. Maximizing EV

**Key Trade-off:**

**GTO (Unexploitable):**

- Guarantees non-negative EV
- Cannot be exploited
- May not be maximally profitable against bad opponents

**Exploitative:**

- Maximizes EV against specific opponent
- Can be exploited if opponent adjusts
- Higher variance

**Recommended Approach:**

1. Start with GTO as baseline
2. Detect opponent deviations from GTO
3. Apply exploitative adjustments
4. Monitor if opponent is adapting
5. Return to GTO if opponent adjusts

```python
def strategy_selection(opponent_model, confidence):
    if confidence < 0.6:
        return 'gto'  # Not confident, stay unexploitable

    elif opponent_model.is_adaptive():
        return 'gto'  # Opponent adapts, don't get exploited

    else:
        return 'exploitative'  # Opponent is static, maximize EV
```

---

## Implementation Priorities

### Phase 1: Foundation (Days 1-2)

**Goal:** Beat John1 (59%)

Implement in order:

1. F1.1: SimpleThreshold (30 min)
2. F1.2: PotOddsPlayer (1 hour)
3. F1.3: PositionAware (1 hour)

**Expected outcome:** 62-65% win rate

### Phase 2: GTO Core (Days 3-4)

**Goal:** Approach John3 (71%)

Implement in order:

1. G2.1: MixedStrategyPlayer (2 hours)
2. G2.2: OptimalThresholdPlayer (2 hours)
3. G2.3: EquilibriumPlayer (3 hours)

**Expected outcome:** 68-71% win rate

### Phase 3: Opponent Modeling (Days 5-6)

**Goal:** Beat John3 consistently

Implement in order:

1. O3.1: StatisticalTracker (1.5 hours)
2. O3.2: BasicAdaptivePlayer (2 hours)
3. O3.3: BayesianModelingPlayer (4 hours)

**Expected outcome:** 70-73% win rate

### Phase 4: Advanced Exploitation (Days 7-8)

**Goal:** Significantly outperform John3

Implement in order:

1. A4.1: ExploitationEngine (3 hours)
2. A4.2: MetaStrategyPlayer (3 hours)
3. A4.3: DynamicThresholdPlayer (4 hours)

**Expected outcome:** 72-75% win rate

### Phase 5: Elite Integration (Days 9-10)

**Goal:** Maximum possible win rate

Implement in order:

1. E5.1: HybridPlayer (3 hours)
2. E5.2: AdaptiveHybridPlayer (2 hours)
3. E5.3: UltimatePlayer (5 hours)

**Expected outcome:** 75-78%+ win rate

---

## Critical Success Factors

### 1. Position Awareness

**Why Critical:** Small Blind vs Big Blind have fundamentally different optimal strategies

- BB has already invested 2x and should defend more
- SB acts first and should be more cautious
- Threshold adjustments of 0.05-0.10 can add 2-3% win rate

### 2. Mixed Strategies

**Why Critical:** Pure strategies are exploitable

- Must randomize to prevent opponents from adapting
- Bluffing is essential for making value bets profitable
- Implement proper RNG for unpredictability

### 3. Opponent Modeling

**Why Critical:** 90 diverse opponents require adaptation

- Some opponents are tight, some loose
- Some aggressive, some passive
- One-size-fits-all strategy won't maximize win rate
- Track statistics to identify patterns

### 4. Score-Differential Awareness

**Why Critical:** Risk management changes based on score

- When ahead, protect lead
- When behind, take calculated risks
- Similar to ICM in tournament poker

### 5. Bet Sizing

**Why Critical:** Not just fold/call/raise decision

- How much to raise matters
- Larger bets with stronger hands
- Smaller bets for bluffs (cheaper)
- Consider pot odds for opponent

---

## Common Pitfalls to Avoid

### 1. Over-fitting to Training Data

**Problem:** Exploiting specific training opponents may not generalize to test opponents
**Solution:** Maintain GTO base, add exploitative layers

### 2. Insufficient Bluffing

**Problem:** Only betting with strong hands is too predictable
**Solution:** Force yourself to bluff 15-20% of the time with weak hands

### 3. Ignoring Position

**Problem:** Playing the same strategy in SB and BB
**Solution:** Implement separate thresholds for each position

### 4. Poor Bet Sizing

**Problem:** Always betting pot + minbet regardless of card strength
**Solution:** Scale bet size with card strength and opponent tendencies

### 5. No Opponent Adaptation

**Problem:** Using same strategy against all opponents
**Solution:** Implement opponent modeling and adjust strategy

### 6. Rounding Errors

**Problem:** Forgetting bets must be multiples of minbet
**Solution:** Always round: `int(bet / minbet) * minbet`

### 7. Fold vs. Call Confusion

**Problem:** Returning value < pot when intending to call
**Solution:** To call, return exactly `pot`; to fold, return `0`

### 8. State Management

**Problem:** Not resetting state between opponents in `__init__()`
**Solution:** Always initialize fresh state in `__init__()`

---

## Research References

### Key Papers & Resources

1. **Kuhn, H. W. (1950)** - "A Simplified Two-Person Poker"

   - Foundation of simplified poker game theory
   - Nash equilibrium for 3-card poker

2. **Ferguson, Chris** - "Uniform(0,1) Two-Person Poker Models"

   - Directly applicable to this variant
   - Continuous card distribution analysis

3. **Billings et al. (1998)** - "Opponent Modeling in Poker"

   - Early work on Loki poker bot
   - Statistical opponent modeling

4. **Johanson et al. (2011)** - "Bayes' Bluff: Opponent Modeling in Poker"

   - Bayesian framework for opponent classification
   - Adaptive strategy selection

5. **Bowling et al. (2015)** - "Heads-up Limit Hold'em Poker is Solved"

   - Counterfactual regret minimization
   - Near-perfect GTO solution

6. **Friedman, L. (1971)** - "Optimal Bluffing Strategies in Poker"
   - Mathematical analysis of bluffing frequency
   - Indifference principle

### Online Resources

- **PokerSciences**: GTO fundamentals
- **GTO Wizard**: Bluffing frequencies and ranges
- **Red Chip Poker**: Exploitative strategies
- **Upswing Poker**: Bet sizing and value/bluff ratios

---

## Final Recommendations

### For Maximum Win Rate

**1. Start with Solid GTO Foundation**

- Implement G2.3 (EquilibriumPlayer) first as baseline
- This ensures you never get badly exploited
- Expected: ~68-70% win rate

**2. Add Opponent Modeling Layer**

- Implement O3.3 (BayesianModelingPlayer)
- Track opponent statistics
- Classify into archetypes
- Expected: +2-3% win rate boost

**3. Implement Exploitation Engine**

- Implement A4.1 (ExploitationEngine)
- Detect specific exploitable patterns
- Apply targeted counter-strategies
- Expected: +1-2% win rate boost

**4. Integrate Meta-Strategy**

- Implement A4.2 (MetaStrategyPlayer)
- Adjust for score differentials
- Risk management with Kelly Criterion
- Expected: +1-2% win rate boost

**5. Final Integration**

- Implement E5.3 (UltimatePlayer)
- Combine all components
- Fine-tune thresholds
- Expected: 75%+ win rate

### If Time Constrained

**Quick Path to 70%+:**

1. **Day 1:** Implement G2.2 (OptimalThresholdPlayer) - 2 hours

   - GTO thresholds with mixed strategies
   - Expected: ~66-68%

2. **Day 2:** Add opponent statistics tracking - 2 hours

   - Track fold/call/raise frequencies
   - Simple if-then exploitative adjustments
   - Expected: ~69-71%

3. **Day 3:** Refinement and testing - 4 hours
   - Tune thresholds
   - Fix bugs
   - Test against all training opponents
   - Expected: ~71-73%

### For Competitive Advantage

**Target 75%+ Path:**

- Follow full Phase 1-5 implementation (10 days)
- Implement all Level 1-5 players
- Test each thoroughly
- Keep best-performing components
- Create ensemble (HybridPlayer)
- Expected: 75-78% win rate

---

## Conclusion

This implementation plan provides a structured, research-backed approach to building a winning poker bot for this variant. The DAG structure allows you to:

1. **Build incrementally** from simple to complex
2. **Test each component** independently
3. **Identify what works** through empirical testing
4. **Iterate and improve** based on results
5. **Combine best elements** into elite player

**Key Insight:** This game is a beautiful blend of:

- **Mathematics** (GTO, Nash equilibrium, pot odds)
- **Statistics** (opponent modeling, Bayesian inference)
- **Psychology** (bluffing, exploitation, adaptation)
- **Risk Management** (score differential, Kelly criterion)

Success requires mastering all four dimensions.

**Good luck, and may your win rate exceed 75%!**

---

## Appendix: Quick Reference

### Essential Formulas

```python
# Pot odds
pot_odds = call_amount / (pot + call_amount)

# Optimal bluff frequency
bluff_freq = call_amount / (pot + call_amount)

# Kelly Criterion
bet_size = bankroll * edge / odds

# Expected value
EV = P(win) * winnings - P(lose) * loss

# Required equity to call
required_equity = call_amount / (pot + call_amount)
```

### Key Thresholds (Starting Points)

```python
FOLD_THRESHOLD = 0.35
BLUFF_THRESHOLD = 0.18
VALUE_THRESHOLD = 0.72
CALL_THRESHOLD_LOW = 0.35
CALL_THRESHOLD_HIGH = 0.72
```

### Position Adjustments

```python
# Big Blind (more aggressive)
BB_FOLD_THRESHOLD = 0.30  # Fold less
BB_VALUE_THRESHOLD = 0.70  # Value bet wider

# Small Blind (more conservative)
SB_FOLD_THRESHOLD = 0.40  # Fold more
SB_VALUE_THRESHOLD = 0.75  # Value bet tighter
```

### Testing Commands

```bash
# Quick test (5 opponents)
python3 -c "from opponents import training_opponents; from pokerplayer import PokerPlayer; from randomTexas import play; play(PokerPlayer, training_opponents[0:5], 200, 1)"

# Full test (all 90 opponents)
python3 -c "from opponents import training_opponents; from pokerplayer import PokerPlayer; from randomTexas import play; play(PokerPlayer, training_opponents, 200, 0)"

# Specific opponent
python3 -c "from opponents import John3; from pokerplayer import PokerPlayer; from randomTexas import pokerTest; pokerTest(PokerPlayer, John3, 100, 1)"
```

===========================================================
Plan 2:

# Ultimate Implementation Plan: Random Number Texas Hold'Em Poker Bot

## Strategic Overview

This comprehensive guide provides a directed acyclic graph (DAG) of poker bot strategies for Random Number Texas Hold'Em, progressing from simple baseline approaches to sophisticated game-theory-optimal play. **The critical insight: your variant simplifies traditional poker because win probabilities are explicit (card values 0-1), eliminating hidden information while preserving strategic depth in bet sizing, bluffing frequencies, and opponent exploitation.**

---

## Game Mechanics Reminder

- **Card Values**: Each player receives one card valued 0-1 (this IS their exact showdown win probability)
- **Starting Stacks**: 100 points each
- **Victory Condition**: First to 200 points
- **Blinds**: Small Blind (1 pt), Big Blind (2 pts), alternating positions
- **Blind Escalation**: Minimum bet doubles every 100 hands
- **Actions**: Fold, Call, Raise (multiples of minimum bet)
- **Bet Limits**: Maximum bet = smaller stack size

---

## Strategy Evolution DAG

```
LEVEL 0: BASELINES (Control Strategies)
├─ A0: Random Bot
├─ A1: Always-Fold Bot
└─ A2: Always-Call Bot

↓ (Foundation)

LEVEL 1: THRESHOLD-BASED (O(1) Decisions)
├─ B1: Simple Threshold (fold \u003c 0.4, call 0.4-0.6, raise \u003e 0.6)
├─ B2: Pot-Odds Aware (compare card value to pot odds)
└─ B3: Position-Aware Thresholds (adjust by SB vs BB)

↓ (Add probabilistic reasoning)

LEVEL 2: KELLY-BASED BET SIZING (O(1) with sophistication)
├─ C1: Full Kelly (bet f* = 2p-1 of stack)
├─ C2: Fractional Kelly (0.25x-0.5x Kelly for reduced variance)
└─ C3: Stack-Aware Kelly (adjust by M-ratio)

↓ (Introduce mixed strategies)

LEVEL 3: BALANCED STRATEGIES (O(1) + randomization)
├─ D1: GTO Bluffing (bluff at frequency = bet/(pot+bet))
├─ D2: Mixed Thresholds (randomize in 0.45-0.55 range)
└─ D3: Nash-Approximation (implement equilibrium frequencies)

↓ (Add adaptation)

LEVEL 4: OPPONENT MODELING (O(n) tracking)
├─ E1: Statistical Tracker (track VPIP, PFR, Aggression Factor)
├─ E2: Bayesian Classifier (classify into 4 types: Tight/Loose × Passive/Aggressive)
└─ E3: Pattern Recognition (detect fold thresholds, bluff frequencies)

↓ (Exploit discovered patterns)

LEVEL 5: EXPLOITATIVE STRATEGIES (O(n*m))
├─ F1: Fold-Exploit (increase bluff frequency vs tight opponents)
├─ F2: Call-Exploit (eliminate bluffs vs calling stations)
├─ F3: Aggression-Exploit (trap vs maniacs, pressure vs passive)
└─ F4: Multi-Armed Bandit (select counter-strategy dynamically)

↓ (Add game phase awareness)

LEVEL 6: ICM-AWARE STRATEGIES (O(n*m))
├─ G1: Score-Differential Adjustment (risk-averse when leading, aggressive when trailing)
├─ G2: M-Ratio Adaptation (shift to push/fold at M\u003c10)
└─ G3: Blind-Level Response (widen ranges as blinds increase)

↓ (Ultimate sophistication)

LEVEL 7: GAME-THEORY OPTIMAL (O(tree))
├─ H1: CFR-Computed Blueprint (offline Nash equilibrium via Counterfactual Regret Minimization)
├─ H2: Real-Time Subgame Solving (online strategy refinement)
└─ H3: Hybrid GTO+Exploit (GTO baseline with exploitative deviations)
```

---

## Detailed Strategy Specifications

### LEVEL 0: BASELINES

**Purpose**: Benchmarking and sanity checks

#### A0: Random Bot

**Algorithm**: `random.choice([FOLD, CALL, RAISE])`  
**Complexity**: O(1)  
**Expected Performance**: ~0-5% win rate  
**Strengths**: None (control only)  
**Weaknesses**: Everything  
**Implementation**: 5 lines of code

#### A1: Always-Fold Bot

**Algorithm**: Always folds  
**Complexity**: O(1)  
**Expected Performance**: Loses blinds every hand, ~0% win rate  
**Purpose**: Minimum baseline

#### A2: Always-Call Bot

**Algorithm**: Never folds, never raises, always calls  
**Complexity**: O(1)  
**Expected Performance**: ~30-40% vs exploitative opponent  
**Vulnerability**: Bled dry by value bets

---

### LEVEL 1: THRESHOLD-BASED STRATEGIES

**Core Concept**: Make decisions based solely on card value

#### B1: Simple Threshold

```python
def decide(card_value, pot, bet):
    if card_value \u003c 0.40:
        return FOLD
    elif card_value \u003c 0.60:
        return CALL
    else:
        return RAISE(amount=pot * 0.5)
```

**Complexity**: O(1)  
**Memory**: O(1)  
**Expected Performance**: 40-50% vs random opponents  
**Strengths**: Simple, fast, beats random play  
**Weaknesses**: Highly exploitable (predictable), ignores pot odds, fixed bet sizing  
**Countered By**: Any opponent who notices fold threshold and adjusts bluff frequency  
**Beats**: Random, always-fold, always-call bots

#### B2: Pot-Odds Aware

```python
def decide(card_value, pot, bet_to_call):
    pot_odds = bet_to_call / (pot + bet_to_call)
    if card_value \u003c pot_odds:
        return FOLD
    elif card_value \u003c pot_odds + 0.15:
        return CALL
    else:
        # Raise when significant edge
        raise_size = pot * min(card_value, 0.75)
        return RAISE(raise_size)
```

**Complexity**: O(1)  
**Expected Performance**: 50-55% vs simple opponents  
**Strengths**: Mathematically sound calling decisions  
**Weaknesses**: Still predictable, no opponent modeling  
**Key Insight**: Compare card value directly to pot odds - correct call/fold decision is simple math

#### B3: Position-Aware Thresholds

```python
def decide(card_value, position, pot, bet):
    # Button (Small Blind) can play wider
    if position == BUTTON:
        fold_threshold = 0.35
        raise_threshold = 0.55
    else:  # Big Blind - tighter
        fold_threshold = 0.45
        raise_threshold = 0.65

    if card_value \u003c fold_threshold:
        return FOLD
    elif card_value \u003c raise_threshold:
        return CALL
    else:
        return RAISE(pot * 0.6)
```

**Complexity**: O(1)  
**Expected Performance**: 52-58% vs non-positional opponents  
**Strengths**: Exploits button advantage (70-90% opening range standard in heads-up)  
**Weaknesses**: Fixed thresholds still exploitable  
**Builds On**: B1, B2 by adding positional dimension

---

### LEVEL 2: KELLY-BASED BET SIZING

**Core Concept**: Optimal bet sizing based on known win probability

#### C1: Full Kelly

```python
def kelly_bet_size(card_value, stack):
    # Kelly formula for even-money bets: f* = 2p - 1
    kelly_fraction = 2 * card_value - 1

    if kelly_fraction \u003c= 0:
        return FOLD

    optimal_bet = kelly_fraction * stack
    return min(optimal_bet, stack)  # Cap at stack size
```

**Complexity**: O(1)  
**Expected Performance**: 55-60% vs fixed-size bettors  
**Strengths**: Mathematically optimal growth rate, maximizes long-term bankroll  
**Weaknesses**: High variance, can be exploited by adjusting to bet sizes  
**Key Formula**: f\* = 2p - 1 for even-money scenarios  
**Example**: With 0.70 win probability → bet 40% of stack

#### C2: Fractional Kelly (RECOMMENDED)

```python
def fractional_kelly(card_value, stack, kelly_multiplier=0.4):
    kelly_fraction = 2 * card_value - 1

    if kelly_fraction \u003c= 0:
        return FOLD

    # Use 0.25-0.5x Kelly for reduced variance
    # 0.5x Kelly retains 75% of growth with only 25% of variance
    conservative_fraction = kelly_fraction * kelly_multiplier
    optimal_bet = conservative_fraction * stack

    return min(optimal_bet, stack)
```

**Complexity**: O(1)  
**Expected Performance**: 58-63% vs non-Kelly opponents  
**Strengths**: Balances growth vs variance, more robust  
**Recommended Multiplier**: 0.4 (between quarter-Kelly and half-Kelly)  
**Builds On**: C1 by reducing risk

#### C3: Stack-Aware Kelly

```python
def stack_aware_kelly(card_value, stack, blinds_total):
    # M-ratio = stack / cost_per_orbit
    m_ratio = stack / blinds_total

    # Adjust Kelly multiplier based on stack depth
    if m_ratio \u003e 20:
        kelly_mult = 0.4  # Conservative with deep stack
    elif m_ratio \u003e 10:
        kelly_mult = 0.5  # Moderate
    elif m_ratio \u003e 5:
        kelly_mult = 0.6  # Aggressive
    else:
        kelly_mult = 0.8  # Desperate - need chips

    kelly_fraction = (2 * card_value - 1) * kelly_mult
    return max(0, min(kelly_fraction * stack, stack))
```

**Complexity**: O(1)  
**Expected Performance**: 60-65% vs non-adaptive opponents  
**Strengths**: Adapts to game phase, optimal for doubling blind structure  
**Key Metric**: M-ratio (stack/blinds) determines aggression level

---

### LEVEL 3: BALANCED STRATEGIES

**Core Concept**: Prevent exploitation through mixed strategies and GTO principles

#### D1: GTO Bluffing Frequencies

```python
def gto_bluff_decision(card_value, pot, bet_size):
    # Optimal bluff frequency = bet / (pot + bet)
    optimal_bluff_freq = bet_size / (pot + bet_size)

    # Categorize hand strength
    if card_value \u003e 0.5:
        # Value hands - bet deterministically
        return BET(bet_size)
    else:
        # Bluff with correct frequency
        if random.random() \u003c optimal_bluff_freq:
            return BET(bet_size)
        else:
            return FOLD
```

**Complexity**: O(1) + randomization  
**Expected Performance**: 62-67% vs exploitative opponents, ~50% vs GTO  
**Strengths**: Unexploitable, forces opponent indifference  
**Key Formula**: Bluff frequency = B/(P+B) where B=bet, P=pot  
**Example**: $100 pot, $75 bet → bluff 43% of weak hands

#### D2: Mixed Thresholds

```python
def mixed_threshold_decision(card_value, pot, position):
    # Deterministic zones
    if card_value \u003c 0.35:
        return FOLD
    if card_value \u003e 0.65:
        return RAISE(pot * 0.6)

    # Mixed strategy zone (0.35-0.65)
    # Prevents opponent from exploiting exact thresholds
    randomization = random.uniform(-0.05, 0.05)
    adjusted_value = card_value + randomization

    if adjusted_value \u003c 0.50:
        return FOLD if random.random() \u003c 0.3 else CALL
    else:
        return RAISE if random.random() \u003c 0.4 else CALL
```

**Complexity**: O(1) + randomization  
**Expected Performance**: 63-68%  
**Strengths**: Unpredictable, balanced ranges  
**Builds On**: B3 + D1 combining threshold logic with mixing

#### D3: Nash Equilibrium Approximation

```python
class NashBot:
    def __init__(self):
        # Precomputed Nash equilibrium strategies
        self.sb_open_threshold = 0.42
        self.sb_raise_threshold = 0.58
        self.bb_call_threshold = 0.38
        self.bb_3bet_threshold = 0.72

    def decide_sb(self, card_value, pot, min_bet):
        if card_value \u003c self.sb_open_threshold:
            return FOLD
        elif card_value \u003c self.sb_raise_threshold:
            # Mixed: Call 30%, Raise 70%
            if random.random() \u003c 0.70:
                return RAISE(min_bet * 2.5)
            return CALL
        else:
            # Always raise strong hands
            bet_size = self.kelly_sizing(card_value)
            return RAISE(bet_size)

    def decide_bb(self, card_value, pot, bet_to_call):
        pot_odds = bet_to_call / (pot + bet_to_call)

        if card_value \u003c pot_odds:
            return FOLD
        elif card_value \u003c self.bb_3bet_threshold:
            return CALL
        else:
            # 3-bet strong hands
            if random.random() \u003c 0.80:
                return RAISE(bet_to_call * 3)
            return CALL  # Trap occasionally
```

**Complexity**: O(1) + lookup + randomization  
**Expected Performance**: 65-70% vs non-GTO, ~50% vs perfect GTO  
**Strengths**: Theoretically unexploitable, solid baseline  
**Weaknesses**: Doesn't exploit weak opponents (leaves money on table)  
**Implementation**: Can be computed offline via CFR (see H1)

---

### LEVEL 4: OPPONENT MODELING

**Core Concept**: Track opponent statistics to enable exploitation

#### E1: Statistical Tracker

```python
class OpponentStats:
    def __init__(self):
        self.hands_seen = 0
        self.voluntarily_played = 0  # VPIP
        self.preflop_raised = 0  # PFR
        self.bets_made = 0
        self.raises_made = 0
        self.calls_made = 0
        self.folds_to_bet = 0
        self.opportunities_to_fold = 0

    def update(self, action, context):
        self.hands_seen += 1
        if action in [CALL, RAISE]:
            self.voluntarily_played += 1
        if action == RAISE:
            self.preflop_raised += 1
            self.raises_made += 1
        elif action == BET:
            self.bets_made += 1
        elif action == CALL:
            self.calls_made += 1
        elif action == FOLD and context['facing_bet']:
            self.folds_to_bet += 1
            self.opportunities_to_fold += 1

    def get_vpip(self):
        return self.voluntarily_played / max(1, self.hands_seen)

    def get_pfr(self):
        return self.preflop_raised / max(1, self.hands_seen)

    def get_aggression_factor(self):
        aggressive = self.bets_made + self.raises_made
        passive = self.calls_made
        return aggressive / max(1, passive)

    def get_fold_frequency(self):
        return self.folds_to_bet / max(1, self.opportunities_to_fold)
```

**Complexity**: O(1) per update, O(1) per query  
**Memory**: O(1) per opponent  
**Expected Performance**: 65-72% when combined with exploitation  
**Key Metrics**: VPIP (15-20% = tight, \u003e30% = loose), PFR (2-4% below VPIP), AF (3 = balanced)  
**Minimum Sample**: Require 20-30 hands before trusting statistics

#### E2: Bayesian Opponent Classifier

```python
class BayesianClassifier:
    def __init__(self):
        self.opponent_types = {
            'TIGHT_PASSIVE': {'vpip': 0.15, 'af': 1.5},
            'TIGHT_AGGRESSIVE': {'vpip': 0.18, 'af': 3.5},
            'LOOSE_PASSIVE': {'vpip': 0.40, 'af': 1.5},
            'LOOSE_AGGRESSIVE': {'vpip': 0.45, 'af': 4.5},
            'BALANCED': {'vpip': 0.25, 'af': 3.0}
        }
        # Prior probabilities (uniform initially)
        self.beliefs = {t: 0.20 for t in self.opponent_types}

    def update_beliefs(self, observed_vpip, observed_af):
        # Bayesian update: P(Type|Obs) ∝ P(Obs|Type) × P(Type)
        likelihoods = {}

        for opp_type, expected in self.opponent_types.items():
            # Gaussian likelihood
            vpip_likelihood = self.gaussian(observed_vpip, expected['vpip'], 0.05)
            af_likelihood = self.gaussian(observed_af, expected['af'], 0.8)
            likelihoods[opp_type] = vpip_likelihood * af_likelihood

        # Update beliefs
        for opp_type in self.beliefs:
            self.beliefs[opp_type] *= likelihoods[opp_type]

        # Normalize
        total = sum(self.beliefs.values())
        self.beliefs = {k: v/total for k, v in self.beliefs.items()}

    def classify(self):
        return max(self.beliefs.items(), key=lambda x: x[1])

    @staticmethod
    def gaussian(x, mu, sigma):
        return math.exp(-0.5 * ((x - mu) / sigma) ** 2)
```

**Complexity**: O(k) where k = number of opponent types (5)  
**Expected Performance**: 68-73% with exploitation  
**Strengths**: Probabilistic classification, handles uncertainty  
**Converges**: 20-50 hands for confident classification

#### E3: Pattern Recognition

```python
class PatternRecognizer:
    def __init__(self):
        self.fold_thresholds = {}  # bet_size → fold_rate
        self.bluff_frequencies = []
        self.bet_sizing_by_strength = {}

    def track_fold_response(self, bet_size, did_fold):
        if bet_size not in self.fold_thresholds:
            self.fold_thresholds[bet_size] = []
        self.fold_thresholds[bet_size].append(did_fold)

    def estimate_fold_threshold(self):
        # Find bet size where opponent folds 50%+
        for size in sorted(self.fold_thresholds.keys()):
            fold_rate = sum(self.fold_thresholds[size]) / len(self.fold_thresholds[size])
            if fold_rate \u003e= 0.50:
                return size
        return float('inf')  # Never folds

    def track_showdown(self, betting_sequence, final_hand_strength):
        # Was this a bluff?
        if 'BET' in betting_sequence and final_hand_strength \u003c 0.5:
            self.bluff_frequencies.append(1)
        elif 'BET' in betting_sequence:
            self.bluff_frequencies.append(0)

    def get_bluff_frequency(self):
        if len(self.bluff_frequencies) \u003c 5:
            return 0.30  # Population default
        return sum(self.bluff_frequencies) / len(self.bluff_frequencies)
```

**Complexity**: O(n) total observations  
**Expected Performance**: 70-75% when exploiting patterns  
**Key Insights**: Fold thresholds and bluff frequencies most exploitable

---

### LEVEL 5: EXPLOITATIVE STRATEGIES

**Core Concept**: Deviate from GTO to maximally exploit opponent weaknesses

#### F1: Fold-Exploit (vs Tight Opponents)

```python
def exploit_tight_opponent(stats, card_value, pot, position):
    fold_frequency = stats.get_fold_frequency()

    if fold_frequency \u003e 0.65:  # Opponent folds too much
        # Increase bluff frequency dramatically
        if card_value \u003c 0.45:
            # Would normally fold, but bluff aggressively
            if random.random() \u003c 0.60:  # 60% bluff rate vs 33% GTO
                # Use smaller bets (they fold anyway)
                return RAISE(pot * 0.4)

        # Widen opening range from button
        if position == BUTTON and card_value \u003e 0.30:  # vs 0.42 GTO
            return RAISE(pot * 0.5)

    # Default to GTO if not exploitable
    return gto_strategy(card_value, pot, position)
```

**Expected Performance**: 75-82% vs tight-passive opponents  
**Risk**: If opponent adjusts and traps, losses can be severe  
**Countered By**: Opponent starts calling down lighter or trap-calling  
**Beats**: Any robot with fold_frequency \u003e 65%

#### F2: Call-Exploit (vs Loose/Passive Opponents)

```python
def exploit_calling_station(stats, card_value, pot):
    vpip = stats.get_vpip()
    af = stats.get_aggression_factor()

    if vpip \u003e 0.35 and af \u003c 2.0:  # Calling station
        # Never bluff - they won't fold
        if card_value \u003c 0.50:
            return FOLD

        # Value bet wider and larger
        if card_value \u003e 0.55:  # Lower threshold (was 0.65)
            # Bet larger (they call anyway)
            bet_size = pot * 1.5  # vs 0.6x GTO
            return RAISE(bet_size)

        # Even medium hands can value bet
        if card_value \u003e 0.50:
            return RAISE(pot * 0.75)

    return gto_strategy(card_value, pot)
```

**Expected Performance**: 78-85% vs loose-passive opponents  
**Strengths**: Extremely profitable vs calling stations  
**Risk**: Minimal - opponent unlikely to adjust  
**Builds On**: E1, E2 statistics + C2 Kelly sizing

#### F3: Aggression-Exploit (vs Maniacs)

```python
def exploit_maniac(stats, card_value, pot):
    af = stats.get_aggression_factor()
    bluff_freq = stats.pattern.get_bluff_frequency()

    if af \u003e 4.5 or bluff_freq \u003e 0.45:  # Maniac/Over-aggressive
        # Trap with strong hands
        if card_value \u003e 0.70:
            # Check-call or min-raise to keep them in
            return CALL  # Let them bluff

        # Call down lighter
        if card_value \u003e 0.50:  # Would normally fold
            # They're often bluffing
            return CALL

        # Don't bluff - they won't fold
        if card_value \u003c 0.45:
            return FOLD

    return gto_strategy(card_value, pot)
```

**Expected Performance**: 72-80% vs loose-aggressive opponents  
**Strengths**: Capitalizes on excessive aggression  
**Key Adjustment**: Call lighter, trap more, bluff less

#### F4: Multi-Armed Bandit Strategy Selection

```python
class MultiArmedBandit:
    def __init__(self):
        self.strategies = ['GTO', 'FOLD_EXPLOIT', 'CALL_EXPLOIT', 'AGG_EXPLOIT']
        self.rewards = {s: 0 for s in self.strategies}
        self.counts = {s: 0 for s in self.strategies}
        self.total_hands = 0

    def select_strategy(self, exploration_rate=0.10):
        # Epsilon-greedy selection
        if random.random() \u003c exploration_rate or self.total_hands \u003c 50:
            return random.choice(self.strategies)

        # UCB (Upper Confidence Bound)
        ucb_scores = {}
        for strat in self.strategies:
            if self.counts[strat] == 0:
                ucb_scores[strat] = float('inf')
            else:
                avg_reward = self.rewards[strat] / self.counts[strat]
                exploration = math.sqrt(2 * math.log(self.total_hands) / self.counts[strat])
                ucb_scores[strat] = avg_reward + exploration

        return max(ucb_scores.items(), key=lambda x: x[1])[0]

    def update(self, strategy, reward):
        self.rewards[strategy] += reward
        self.counts[strategy] += 1
        self.total_hands += 1
```

**Complexity**: O(k) where k = number of strategies  
**Expected Performance**: 73-82% (adapts to opponent type)  
**Strengths**: Automatically finds best counter-strategy  
**Exploration Schedule**: 30% hands 1-50, 15% hands 51-150, 5% hands 151+

---

### LEVEL 6: ICM-AWARE STRATEGIES

**Core Concept**: Adjust for score differentials and game phase

#### G1: Score-Differential Adjustment

```python
def icm_adjusted_decision(card_value, my_score, opp_score, base_decision, base_bet):
    score_diff = my_score - opp_score

    # Calculate ICM pressure
    icm_multiplier = 1.0

    if score_diff \u003e 40:  # Leading by 40+ (e.g., 140-60)
        # Maximum risk aversion
        icm_multiplier = 0.65  # Reduce bet sizes
        equity_threshold = 0.62  # Need higher equity for all-in

    elif score_diff \u003e 20:  # Leading by 20-40 (e.g., 120-80)
        # Moderate risk aversion
        icm_multiplier = 0.80
        equity_threshold = 0.58

    elif abs(score_diff) \u003c= 20:  # Even (90-110)
        # Standard play
        icm_multiplier = 1.0
        equity_threshold = 0.55

    elif score_diff \u003c -20:  # Trailing by 20-40 (e.g., 80-120)
        # Increased aggression
        icm_multiplier = 1.15
        equity_threshold = 0.52

    elif score_diff \u003c -40:  # Trailing by 40+ (e.g., 60-140)
        # Maximum aggression
        icm_multiplier = 1.30
        equity_threshold = 0.48

    # Adjust bet sizing
    adjusted_bet = base_bet * icm_multiplier

    # Fold marginal spots when leading
    if base_decision == 'ALL_IN' and card_value \u003c equity_threshold:
        return FOLD

    return (base_decision, adjusted_bet)
```

**Expected Performance**: 72-80% (critical in tournament-style format)  
**Key Insight**: Chips have non-linear value; leading by 40 points ≠ 40/200 = 20% advantage (it's more like 65-35% win probability)  
**Impact**: Can swing decisions by 10-15% equity requirement

#### G2: M-Ratio Push/Fold Adaptation

```python
def m_ratio_strategy(card_value, stack, blinds_sum, position):
    m_ratio = stack / blinds_sum

    if m_ratio \u003e 20:  # Deep stack
        # Normal play, full strategy available
        return normal_strategy(card_value, position)

    elif m_ratio \u003e 10:  # Medium stack
        # Slightly tighter, increase aggression
        fold_threshold = 0.42
        raise_threshold = 0.58

    elif m_ratio \u003e 5:  # Short stack
        # Push/fold primary strategy
        if position == BUTTON:
            push_threshold = 0.35  # Push 65% of hands
        else:
            call_threshold = 0.42  # Call 58% of hands

        if card_value \u003e push_threshold:
            return ALL_IN
        else:
            return FOLD

    else:  # M \u003c 5 - Critical zone
        # Pure push/fold, very wide ranges
        if position == BUTTON:
            if card_value \u003e 0.25:  # Push 75% of hands!
                return ALL_IN
            else:
                return FOLD
        else:
            if card_value \u003e 0.35:  # Call 65% of hands
                return CALL
            else:
                return FOLD
```

**Expected Performance**: 70-78% (essential for late game survival)  
**Key Metric**: M = stack / (SB + BB)  
**Critical Thresholds**: M\u003c10 = push/fold consideration, M\u003c5 = pure push/fold

#### G3: Blind-Level Response

```python
class BlindLevelTracker:
    def __init__(self):
        self.hands_played = 0
        self.current_level = 1
        self.base_blinds = (1, 2)

    def update_blinds(self):
        self.hands_played += 1
        if self.hands_played % 100 == 0:
            self.current_level += 1

        # Blinds double every 100 hands
        multiplier = 2 ** (self.current_level - 1)
        return (self.base_blinds[0] * multiplier, self.base_blinds[1] * multiplier)

    def get_urgency_factor(self):
        # Urgency increases with blind level
        return 1.0 + (self.current_level - 1) * 0.15

    def adjust_thresholds(self, base_fold, base_raise):
        urgency = self.get_urgency_factor()

        # Widen ranges as blinds increase
        adjusted_fold = base_fold / urgency
        adjusted_raise = base_raise / urgency

        return (adjusted_fold, adjusted_raise)
```

**Expected Performance**: 75-82% (adapts to time pressure)  
**Key Adjustment**: Widen ranges by ~15% per blind level  
**Example**: Level 1 fold at 0.40, Level 3 fold at 0.35, Level 5 fold at 0.30

---

### LEVEL 7: GAME-THEORY OPTIMAL

**Core Concept**: Compute true Nash equilibrium for unexploitable play

#### H1: CFR-Computed Blueprint

```python
class CFRBot:
    def __init__(self):
        # Precomputed via Counterfactual Regret Minimization
        self.strategy = self.load_computed_strategy()
        # strategy[info_set] = {action: probability}

    def get_info_set(self, card_value, pot, history, position):
        # Information set = everything the player knows
        # Round to buckets for tractability
        card_bucket = int(card_value * 10) / 10  # 0.0, 0.1, ..., 1.0
        pot_bucket = self.discretize_pot(pot)
        history_abstraction = self.abstract_history(history)

        return (card_bucket, pot_bucket, history_abstraction, position)

    def decide(self, game_state):
        info_set = self.get_info_set(game_state)

        if info_set not in self.strategy:
            # Fallback to default strategy
            return self.default_strategy(game_state)

        # Sample action according to strategy distribution
        action_probs = self.strategy[info_set]
        return self.sample_action(action_probs)

    @staticmethod
    def compute_strategy_offline():
        # Run CFR for many iterations
        # This is done BEFORE playing
        cfr = CounterfactualRegretMinimization()

        for iteration in range(100000):
            cfr.traverse_game_tree()
            cfr.update_regrets()
            cfr.update_strategy()

        return cfr.get_average_strategy()
```

**Complexity**: O(tree) offline, O(1) online (lookup)  
**Expected Performance**: 68-75% (unexploitable baseline, doesn't exploit weak opponents)  
**Strengths**: Theoretically optimal, unexploitable, perfect defense  
**Weaknesses**: Computationally expensive, doesn't exploit mistakes  
**Convergence**: ~10,000-100,000 iterations for simple variant

**CFR Algorithm Sketch**:

```python
def cfr_iteration(node, reach_probs):
    if node.is_terminal():
        return node.utility()

    info_set = node.get_info_set()
    strategy = get_strategy(info_set)

    # Counterfactual values for each action
    action_values = {}
    node_value = 0

    for action in node.legal_actions():
        child = node.take_action(action)
        action_values[action] = cfr_iteration(child, updated_reach_probs)
        node_value += strategy[action] * action_values[action]

    # Update regrets
    for action in node.legal_actions():
        regret = action_values[action] - node_value
        cumulative_regret[info_set][action] += regret

    return node_value
```

#### H2: Real-Time Subgame Solving

```python
class RealtimeSolver:
    def __init__(self):
        self.blueprint = load_cfr_blueprint()

    def decide(self, game_state):
        # Check if we're in a critical decision
        if self.is_critical_spot(game_state):
            # Solve subgame in real-time
            subgame_strategy = self.solve_subgame(
                game_state,
                depth=3,  # Look ahead 3 actions
                time_limit=2.0  # seconds
            )
            return subgame_strategy.get_action()
        else:
            # Use precomputed blueprint
            return self.blueprint.get_action(game_state)

    def solve_subgame(self, state, depth, time_limit):
        # Nested CFR on remaining game tree
        # Used by Libratus
        solver = CFRSolver(state, depth_limit=depth)
        solver.solve(time_limit=time_limit)
        return solver.get_strategy()
```

**Complexity**: O(subgame_tree) online  
**Expected Performance**: 72-78% (stronger than static blueprint)  
**Strengths**: Adapts to specific game state, more precise  
**Used By**: Libratus (2017 champion bot)

#### H3: Hybrid GTO+Exploit (RECOMMENDED)

```python
class HybridBot:
    def __init__(self):
        self.gto_strategy = load_cfr_blueprint()
        self.opponent_model = OpponentModel()
        self.exploiter = ExploitativeEngine()

    def decide(self, game_state, opponent_id):
        # Update opponent model
        self.opponent_model.observe(opponent_id, game_state)

        # Calculate exploitability
        opponent_type = self.opponent_model.classify(opponent_id)
        confidence = self.opponent_model.get_confidence()
        exploitability = self.estimate_exploitability(opponent_type)

        # Decide whether to exploit or play GTO
        if confidence \u003e 0.70 and exploitability \u003e 0.15:
            # High confidence opponent is exploitable
            # Deviate from GTO to exploit
            exploit_decision = self.exploiter.get_decision(
                game_state, opponent_type
            )

            # Blend with GTO (80% exploit, 20% GTO for safety)
            if random.random() \u003c 0.80:
                return exploit_decision
            else:
                return self.gto_strategy.get_action(game_state)
        else:
            # Low confidence or tough opponent - use GTO
            return self.gto_strategy.get_action(game_state)

    def estimate_exploitability(self, opponent_type):
        # How much can we gain by exploiting?
        exploit_values = {
            'TIGHT_PASSIVE': 0.35,  # Highly exploitable
            'LOOSE_PASSIVE': 0.40,  # Very exploitable
            'LOOSE_AGGRESSIVE': 0.25,  # Moderately exploitable
            'TIGHT_AGGRESSIVE': 0.10,  # Slightly exploitable
            'BALANCED': 0.05  # Minimally exploitable
        }
        return exploit_values.get(opponent_type, 0.05)
```

**Complexity**: O(1) + opponent modeling  
**Expected Performance**: 76-88% (best of both worlds)  
**Strengths**: Unexploitable baseline + exploits weaknesses  
**Recommended Mix**: 80% exploit when confident, 100% GTO when uncertain  
**Builds On**: All previous levels

---

## Strategy Relationships \u0026 Counters

### What Beats What

```
H3 (Hybrid) → Beats all strategies (83-88% vs most)
   ↓ counters
F1-F4 (Exploit) → Beats D1-D3, E1-E3 (75-85%)
   ↓ counters
D3 (Nash) → Beats B1-C3 (65-70%), ties H1-H3 (~50%)
   ↓ counters
E2 (Bayesian) → Beats B1-C3 (68-74%)
   ↓ counters
C2 (Fractional Kelly) → Beats B1-B3 (58-63%)
   ↓ counters
B3 (Position-Aware) → Beats B1-B2 (52-58%)
   ↓ counters
B1 (Simple) → Beats A0-A2 (40-50%)
```

### Vulnerability Analysis

| Strategy              | Exploited By        | How                            |
| --------------------- | ------------------- | ------------------------------ |
| B1 (Simple Threshold) | All higher levels   | Predictable thresholds         |
| B2 (Pot Odds)         | E1+                 | Fixed calling ranges           |
| C1 (Full Kelly)       | E2+                 | Bet sizes reveal hand strength |
| D1 (GTO Bluff)        | H3 only             | Nearly unexploitable           |
| E1 (Stats)            | F4 (MAB)            | Adjusts counter-strategy       |
| F1 (Fold Exploit)     | Opponent trapping   | Over-bluffing punished         |
| F2 (Call Exploit)     | Opponent tightening | Missing bluff opportunities    |
| H1 (Pure GTO)         | H3 (Hybrid)         | Doesn't exploit weaknesses     |

---

## Implementation Roadmap

### Phase 1: MVP (Days 1-3)

**Goal**: Beat random opponents (50%+)

**Implement**:

1. B2: Pot-Odds Aware Threshold
2. C2: Fractional Kelly Bet Sizing (0.4x multiplier)
3. Basic game engine integration

**Expected Performance**: 55-60% vs random/weak opponents

**Complexity**: ~200 lines of code

### Phase 2: Solid Foundation (Days 4-7)

**Goal**: Beat 71-72% reference bot

**Implement**:

1. D3: Nash Equilibrium Approximation
2. E1: Statistical Opponent Tracker
3. G1: Score-Differential Adjustment
4. G2: M-Ratio Push/Fold

**Expected Performance**: 68-75% vs reference bot

**Complexity**: ~500 lines of code

### Phase 3: Exploitation (Days 8-14)

**Goal**: Maximize win rate vs diverse opponents

**Implement**:

1. E2: Bayesian Opponent Classifier
2. F1-F3: Type-Specific Exploitation
3. F4: Multi-Armed Bandit Strategy Selection
4. G3: Blind-Level Response

**Expected Performance**: 75-82% vs diverse field

**Complexity**: ~1000 lines of code

### Phase 4: Advanced (Days 15-30, Optional)

**Goal**: Approach theoretical maximum

**Implement**:

1. H1: CFR-Computed Blueprint
2. H3: Hybrid GTO+Exploit
3. Advanced pattern recognition
4. Real-time strategy refinement

**Expected Performance**: 80-88% vs diverse field

**Complexity**: ~2000-3000 lines of code

---

## Critical Implementation Details

### Decision Function Template

```python
class PokerBot:
    def __init__(self, strategy_level='hybrid'):
        self.level = strategy_level
        self.stats = OpponentStats()
        self.classifier = BayesianClassifier()
        self.bandit = MultiArmedBandit()
        self.icm = ICMCalculator()

    def decide(self, game_state):
        # Extract state
        card_value = game_state.my_card_value
        pot = game_state.pot
        my_score = game_state.my_score
        opp_score = game_state.opponent_score
        position = game_state.position

        # Update models
        self.stats.update(game_state.opponent_last_action)

        # Select strategy
        if self.level == 'threshold':
            return self.threshold_strategy(card_value, pot)
        elif self.level == 'kelly':
            return self.kelly_strategy(card_value, my_score)
        elif self.level == 'gto':
            return self.nash_strategy(card_value, pot, position)
        elif self.level == 'exploit':
            opp_type = self.classifier.classify()
            return self.exploit_strategy(card_value, pot, opp_type)
        elif self.level == 'hybrid':
            return self.hybrid_strategy(game_state)

    def hybrid_strategy(self, state):
        # Phase 1: Learn (hands 1-30)
        if self.stats.hands_seen \u003c 30:
            return self.nash_strategy(state)

        # Phase 2: Exploit (hands 31+)
        opp_type, confidence = self.classifier.classify()

        if confidence \u003e 0.70:
            # Select counter-strategy
            strategy = self.bandit.select_strategy()
            decision = self.execute_strategy(strategy, state, opp_type)

            # Update bandit
            reward = state.result_of_last_hand
            self.bandit.update(strategy, reward)

            return decision
        else:
            # Not confident - play GTO
            return self.nash_strategy(state)
```

### Key Parameters

**Thresholds** (tune for your variant):

- Fold threshold: 0.38-0.45 depending on pot odds
- Raise threshold: 0.55-0.65 depending on position
- Bluff frequency: bet/(pot+bet) for GTO
- Kelly multiplier: 0.3-0.5 (recommend 0.4)

**Opponent Classification** (minimum samples):

- Statistics: 20 hands minimum
- Type classification: 30 hands minimum
- Pattern recognition: 40 hands minimum

**Exploration Rates**:

- Hands 1-50: 30% exploration
- Hands 51-150: 15% exploration
- Hands 151+: 5% exploration

**ICM Adjustments**:

- Leading 40+: reduce bet sizes by 35%, equity threshold +7%
- Leading 20-40: reduce bet sizes by 20%, equity threshold +3%
- Trailing 20-40: increase bet sizes by 15%, equity threshold -3%
- Trailing 40+: increase bet sizes by 30%, equity threshold -7%

**M-Ratio Thresholds**:

- M \u003e 20: Normal play
- M = 10-20: Tighten slightly
- M = 5-10: Push/fold primary
- M \u003c 5: Push/fold only

---

## Benchmarking \u0026 Testing

### Test Suite

**Level 1: Sanity Checks**

- Beats always-fold (100%)
- Beats always-call (60%+)
- Beats random (55%+)

**Level 2: Basic Opponents**

- Beats simple threshold (58%+)
- Beats pot-odds only (52%+)

**Level 3: Reference**

- Beats 71-72% reference bot (52%+)
- Target: 60-65% win rate vs reference

**Level 4: Diverse Field**

- Test vs 89 opponents
- Target: 55%+ vs each type
- Overall: 58-62% average

**Level 5: Exploitability**

- Measure vs best-response opponent
- GTO: 50% (unexploitable)
- Exploitative: may drop to 45-48% vs perfect counter

### Performance Metrics

**Win Rate**: Primary metric

- \u003c50%: Losing strategy
- 50-55%: Weak edge
- 55-60%: Solid edge
- 60-65%: Strong edge
- 65-70%: Very strong edge
- 70%+: Dominant (rare vs good opponents)

**Variance**: Important for tournament format

- Standard deviation in points
- Risk of ruin calculation
- Bankroll requirements

**Exploitability**: How much can perfect opponent gain?

- GTO: 0% exploitability
- Balanced: \u003c2% exploitability
- Exploitative: 5-10% exploitability
- Predictable: 15%+ exploitability

---

## Game-Specific Insights

### Your Variant vs Traditional Poker

**Simplifications**:

1. **No hand ranges** - you know exact equity (card value 0-1)
2. **No card reading** - win probability is explicit
3. **Simpler information sets** - likely fewer than Kuhn poker (12 sets)

**Preserved Complexity**:

1. **Bet sizing** - still critical for value extraction
2. **Bluffing** - necessary for GTO balance
3. **Opponent modeling** - patterns still exploitable
4. **ICM** - score differentials create risk/reward trade-offs
5. **Position** - button advantage remains significant

**Key Implications**:

- CFR should converge FASTER than traditional poker (simpler game tree)
- Kelly Criterion applies DIRECTLY (known probabilities)
- GTO strategy should be COMPUTABLE in hours/days (not weeks)
- Exploitation may be MORE valuable (opponent patterns clearer)

### Optimal Strategy Hypothesis

Based on research, the **theoretical optimal** strategy for your variant likely:

1. **Uses Nash equilibrium as baseline** (computed via CFR)
2. **Applies Kelly bet sizing** (with 0.3-0.5x multiplier for safety)
3. **Adjusts for ICM** (score-differential awareness)
4. **Exploits when confident** (80/20 rule: exploit when confidence \u003e 70%)
5. **Adapts to blind levels** (progressive aggression)
6. **Randomizes in mixed zones** (0.45-0.55 card value ranges)

**Estimated Performance**: 78-85% win rate vs 71-72% reference bot

### Against 89 Diverse Opponents

**Strategy**:

1. **First 30 hands per opponent**: Play GTO, gather statistics
2. **Hands 31-100**: Exploit based on classification
3. **Hands 101+**: Refine exploitation, adapt to adjustments

**Expected Distribution**:

- 20% weak/exploitable opponents → 75-85% win rate
- 50% medium opponents → 58-65% win rate
- 25% strong/GTO opponents → 48-52% win rate
- 5% superior opponents → 40-48% win rate

**Overall**: 60-67% average win rate (vs 50% random baseline)

---

## Complexity vs Performance

| Strategy Level   | Implementation Time | Code Lines | Win Rate | Exploitability |
| ---------------- | ------------------- | ---------- | -------- | -------------- |
| B1 (Threshold)   | 2 hours             | 50         | 45-50%   | Very High      |
| B2 (Pot Odds)    | 4 hours             | 100        | 52-57%   | High           |
| C2 (Kelly)       | 8 hours             | 200        | 58-63%   | Medium-High    |
| D3 (Nash)        | 2 days              | 400        | 65-70%   | Low            |
| E2 (Bayesian)    | 3 days              | 600        | 68-73%   | Low            |
| F4 (MAB Exploit) | 5 days              | 1000       | 75-80%   | Medium         |
| G1-G3 (ICM)      | 7 days              | 1200       | 76-82%   | Low-Medium     |
| H3 (Hybrid)      | 14 days             | 2000       | 80-88%   | Very Low       |

**Recommendation**: Start with **Phase 2** (D3 + E1 + G1-G2) for best ROI. This gives 70-75% win rate with manageable complexity.

---

## Final Recommendations

### For Beating 71-72% Reference Bot

**Minimum Viable Strategy**:

1. **D3: Nash Equilibrium Approximation** - unexploitable baseline
2. **C2: Fractional Kelly Sizing** - optimal bet sizing
3. **G2: M-Ratio Adaptation** - survive late game
4. **E1: Basic Statistics** - enable light exploitation

**Expected Result**: 60-70% win rate vs reference bot

### For Winning Tournament

**Comprehensive Strategy**:

1. **H3: Hybrid GTO+Exploit** - best of both worlds
2. **E2: Bayesian Classification** - identify opponent types
3. **F4: Multi-Armed Bandit** - select counter-strategies
4. **G1: ICM Awareness** - score-differential adjustments
5. **G3: Blind Adaptation** - game phase awareness

**Expected Result**: 65-75% average win rate vs diverse field

### Development Priority

**Week 1**: Implement D3 + C2 + E1 → Beat reference bot (60-65%)  
**Week 2**: Add E2 + F1-F3 → Improve to 70-75%  
**Week 3**: Add G1-G3 → Improve to 75-80%  
**Week 4**: Add H1 + H3 → Improve to 80-85%

---

## Appendix: Key Formulas

**Kelly Criterion**:

```
f* = 2p - 1 (for even money)
Bet = f* × kelly_multiplier × stack
Recommend: kelly_multiplier = 0.4
```

**GTO Bluff Frequency**:

```
Optimal_bluff_freq = Bet / (Pot + Bet)
Example: $100 pot, $50 bet → bluff 33% of weak hands
```

**Pot Odds**:

```
Pot_odds = Bet_to_call / (Pot + Bet_to_call)
Call if: Card_value \u003e Pot_odds
```

**M-Ratio**:

```
M = Stack / (Small_Blind + Big_Blind)
M \u003c 10 → Push/fold mode
M \u003c 5 → Critical/desperate
```

**ICM Equity Adjustment**:

```
Equity_required = Base_equity × (1 + ICM_pressure)
ICM_pressure = |score_diff| / 200
```

**Expected Value**:

```
EV = P(win) × Amount_won - P(lose) × Amount_lost
EV = Card_value × (Pot + Bet) - (1 - Card_value) × Bet
```

**Exploitability**:

```
Exploitability = max_strategy [EV(best_response) - EV(GTO)]
Target: \u003c 2% for robust strategy
```

---

This implementation plan provides a complete roadmap from baseline strategies to game-theory-optimal play with exploitation. The DAG structure shows clear progression paths, and each strategy includes specific algorithms, performance expectations, and vulnerabilities. Start with Phase 2 for the best complexity/performance trade-off, then iterate based on results.

**Most Critical Insight**: Your variant's explicit win probabilities make it simpler than traditional poker while preserving strategic depth. Kelly Criterion applies directly, CFR should converge quickly, and opponent exploitation may be more valuable than in hidden-information games. A well-implemented hybrid strategy (GTO + exploitation + ICM awareness) should achieve 75-85% win rates against most opponents.

==========================================================================
Plan 3:
The ULTIMATE Implementation Plan: A Directed Acyclic Graph of Poker AgentsExecutive Overview: The Directed Acyclic Graph of Poker AgentsThis document presents a comprehensive, expert-level implementation plan for creating a "winning poker player." The user's directive—to create a "directed acyclic graph (DAG) of winning poker players"—is a sophisticated request for a complete research and development ecosystem, not a single, monolithic agent. This plan is therefore structured as an evolutionary graph.Each "Node" in this graph represents a distinct, buildable, and testable AI agent. The "Edges" connecting these nodes represent either:Dependencies: A node that is a prerequisite for another (e.g., a "Blueprint" agent must be built before a "Subgame Solving" agent).Competitive Relationships: A node that is trained against or evaluated by another (e.g., an "Exploitative" agent is trained against a pool of "Heuristic" agents).The DAG is organized into three primary "Phylums" (lineages) that diverge from a common ancestor, the "Gen-0" Foundational Infrastructure.Phylum A (Exploitative): This lineage focuses on agents designed to maximize profitability (win rate) by identifying and capitalizing on opponent mistakes.1 These agents are offensive, adaptive, and highly profitable against suboptimal opponents, but are themselves inherently exploitable.2Phylum B (GTO): This lineage focuses on agents designed to minimize exploitability by adhering to a "Game Theory Optimal" (GTO) strategy.3 These agents are defensive and play a mathematically balanced, unexploitable style derived from Nash Equilibrium principles.5Phylum C (Hybrid/Next-Gen): This lineage explores advanced, alternative architectures that merge the concepts of the first two phylums or introduce entirely new paradigms. This includes state-of-the-art architectures like DeepStack (continual re-solving) 7, AlphaHoldem (MCTS + Deep Learning) 8, and PokerGPT (LLM-based).9The "ultimate winner" is not a single node, but is discovered through the Iteration Engine—a comprehensive evaluation framework that forces all agents to compete. This engine allows a developer to measure performance, identify weaknesses ("which players work and don't work"), and iterate towards a superior, hybrid agent that combines GTO's defensive soundness with exploitative profitability.10I. The Progenitor Node (Gen-0): Foundational InfrastructureBefore any agent can be developed, a non-negotiable foundational layer of infrastructure must be constructed. This "Gen-0" node is the root of the DAG and serves as the computational "universe" in which the game of poker exists. It provides the game engine, the rules of physics (evaluation), and the language of logic (mathematics) that all subsequent agents will depend upon.A. The Environment: Core Game Engine ImplementationDirective: Implement a robust, high-speed, and extensible No-Limit Texas Hold'em (NLHE) game engine. This engine is the state machine that enforces all game rules and manages game flow.Core Components:The engine must be a perfect, procedural representation of NLHE rules.State Representation: The engine's core responsibility is to maintain the complete game state. This includes player stacks, the dealer button position, blind and ante amounts 12, the pot size (with correct handling for main and side pots in "all-in" scenarios 13), the five community cards (flop, turn, river) 14, each player's private two hole cards 15, and a complete history of actions (check, call, bet, raise, fold) for all four betting rounds (preflop, flop, turn, river).14Action Handling: The engine must strictly enforce all legal moves. This includes validating minimum bet and raise amounts (a minimum raise must be at least the size of the previous bet/raise 13), managing "all-in" mechanics 13, and handling player options (check, call, bet, raise, fold).15Game Flow Management: The engine must automate the progression of the game, including rotating the dealer button and blinds clockwise after each hand 12, dealing cards, managing the betting rounds, initiating the showdown for all remaining players, and correctly awarding the pot (or splitting it in a "chop").15Build vs. Buy Analysis:A critical first decision is whether to build this engine or leverage existing open-source frameworks.Buy (Prototype Path): For rapid prototyping, especially for Phylum A agents (Exploitative), open-source environments are the logical choice.RLCard: A research-focused toolkit for card games.16 It provides a standardized API (env = rlcard.make('no-limit-holdem')) 16 and a env.step(action) loop familiar to any reinforcement learning practitioner. It includes pre-built agents for simpler games (e.g., CFR for Leduc Hold'em 18, DQN for Blackjack 18), making it an ideal platform for bootstrapping an agent like our Node A3 (DQN Agent).19PyPokerEngine: A robust, Python-native engine excellent for agent development.21 It provides a BasePokerPlayer class that must be subclassed, with abstract methods like declare_action that the AI must implement.21 It also features an Emulator for fine-grained, step-wise simulation, which is useful for debugging and RL.22 This engine is frequently used in DQN tutorials and provides a clear path for development.23Build (GTO/Performance Path): A custom engine, likely written in C++ with Python bindings, is an absolute requirement for the advanced research in Phylum B and C.The core algorithms of Phylum B (GTO), such as Counterfactual Regret Minimization (CFR) 24 and the architecture of Libratus 25, are not standard RL step-forward loops. They are game-tree traversal algorithms. They require the ability to create copies of the game state, traverse deep into a subgame, and, for some sampling methods, even step_back() (a feature RLCard's API supports but is not designed around 16).The architectures of open-source projects like pluribus-poker-AI 26 and poker_ai 28 demonstrate this "engine-first" approach. A custom-built engine provides the total control necessary to implement Monte Carlo CFR (MCCFR) 29 and real-time subgame solving.25Recommendation: The most efficient path is a dual approach. Begin development of Phylum A agents immediately using RLCard for its fast setup. Concurrently, begin the implementation of a high-performance, custom C++ engine, as this will be a necessary, long-lead-time item for all GTO-based research.B. The Arbiter: High-Speed Hand and Equity EvaluationDirective: Implement the "physics" of poker. This module must answer two fundamental questions with maximum speed: (1) "What is the absolute rank of this five-card hand?" and (2) "What is the winning probability (equity) of this hand against an opponent's range of possible hands?"Implementation:Hand Evaluator: This is the most computationally critical inner loop in the entire system. During self-play (Phylum B/C) or Monte Carlo simulations, this function will be called billions or trillions of times. A naive Python implementation (e.g., with if/then checks for a Straight, Flush, etc. 12) is computationally unacceptable.Solution: Integrate a high-speed, bit-manipulation library. The fastest evaluators use perfect hashing or bitwise operations to map 7 cards to a unique rank.Options: treys 30 (Python wrapper for C), OMPEval (C++) 31, or eval7.32 Performance is measured in millions of hands per second; for example, OMPEval can evaluate 7-card hands at rates exceeding 60 M/s.34Equity Calculator (Monte Carlo): This module answers the question, "What is my percent chance to win?".35 In an imperfect information game, this can only be answered by simulating against a range of possible opponent hands.Algorithm: calculate_equity(my_hand, board_cards, opponent_range)Process:Loop N times (e.g., N=10,000).Randomly select one opponent_hand from the opponent_range.Randomly deal the remaining board_cards (e.g., turn and river).Call the high-speed Hand Evaluator (I.B.1) for both my_hand and opponent_hand.If my_hand wins, increment wins.Return wins / N.This calculator is the foundation of all rational decision-making.35The performance of the Arbiter directly gates the research velocity of the entire project. The necessity of a high-speed C++ evaluator (I.B.1) reinforces the recommendation to build a custom C++ game engine (I.A) to avoid costly data marshalling between Python and C++ in the system's inner-most loop.C. The Lexicon: Core Mathematical Principles ModuleDirective: Implement a library of foundational mathematical functions. If the Arbiter is the "physics," the Lexicon is the "brain stem" or "language of logic" for all rational agents (all nodes except the most primitive).Functions:This module implements the central triad of poker logic: Pot Odds, Equity, and Expected Value.37calculate_pot_odds(pot_size, bet_to_call):Definition: The ratio of the total pot (including the bet to be called) to the cost of the call.37 Example: Pot is $100. Opponent bets $20. The pot is now $120. It costs $20 to call. The pot odds are $120:$20, or 6-to-1.37Purpose: This function defines the required equity an agent must have to make a call profitable. To call a 6-to-1 bet, the agent needs to win more than 1 out of (6+1) = 7 times, or >14.3% equity.calculate_equity(my_hand, board, opponent_range):Definition: This function calls the "Arbiter" module (I.B.2) to run a Monte Carlo simulation and return the agent's win percentage.35Purpose: This provides the actual equity the agent possesses in the hand.calculate_expected_value(EV):Definition: The core metric for all decisions in poker.37 It is the average amount an agent stands to win or lose from a specific decision if the same situation were run infinitely.39Formula (for a call): EV_call = (Equity * $Pot_if_we_win) - ( (1 - Equity) * $Bet_to_call).37Purpose: This module ties everything together. A rational agent's entire decision process is a comparison of EV.EV_fold = $0 (always).39The agent calculates EV_call and EV_raise.It then chooses the action with the highest positive EV. If all actions have a negative EV, it must fold (as EV_fold = $0 is preferable).39The logical flow for any rational agent is:Call calculate_pot_odds() to determine the required equity.Call calculate_equity() to determine the actual equity.Compare them to calculate calculate_expected_value() for the action.This "Triad of Logic" is the fundamental upgrade from a "dumb" agent (like Node A1) to a "rational" agent (like Node A2).38II. Phylum A: The Exploitative Lineage (Heuristic & Model-Based Agents)Phylum Goal: This lineage is focused on a single objective: maximizing profitability, measured in win rate (e.g., mbb/g). These agents are designed to exploit the mistakes and tendencies of suboptimal opponents.1 They deviate from a balanced GTO strategy to deliberately target opponent weaknesses.1 While highly profitable in the short term against specific player types 1, this offensive posture makes them, by definition, predictable and exploitable themselves.2A. Node A1: The "Chart-Based" Agent (The NIT/TAG)Architecture: This is the most primitive agent, built as a simple Finite-State Machine (FSM) or a series of if/then heuristics. Its strategy is static, hard-coded, and transparent.Implementation:Preflop Logic: The agent's preflop decisions are governed by a hard-coded set of "Raise First In" (RFI) charts, which vary by table position.41 These charts are defined using standard poker hand notation 42 (e.g., JJ+ = {JJ, QQ, KK, AA}; AKs = Ace-King suited).if (position == 'UTG'): RFI_range = { '99+', 'AQs+', 'AKo' }if (my_hand in RFI_range): return raise(3bb)else: return fold()Postflop Logic: The agent employs a "fit-or-fold" strategy, characteristic of a "NIT" (a very tight player).45 It has no concept of pot odds, equity, or opponent modeling.if (my_hand_strength > 'Two Pair'): return bet(pot)if (my_hand_strength < 'Top Pair'): return check() or fold()Role in DAG: This node is the baseline training dummy. It is a "bad player" 45 or a "NIT" 45 whose rigid, rule-based logic is trivially exploitable.46 Its purpose in the DAG is to serve as the "Level 1" player 47—a stationary target that Node A2 is designed to exploit and Node A3 is trained to defeat.B. Node A2: The "Statistician" (Opponent-Modeling Agent)Architecture: This is a model-based agent that dynamically builds a statistical profile of each opponent and deploys a specific, pre-defined counter-strategy. This architecture is the foundation of early high-performance poker bots like Loki 48 and is the first true "exploitative" agent.49Implementation:This agent is built from three distinct modules:Module 1: Data Parser & Statistician: This agent observes 100% of the hand histories at the table, even those it is not involved in. It parses these logs to calculate a vector of key statistics for each opponent. The two most critical stats are VPIP (Voluntarily Put Money In Pot) and PFR (Pre-Flop Raise).50 Other key stats include 3-Bet % (Preflop aggression) and C-Bet % (Flop aggression).Module 2: Opponent Classifier: After a sufficient sample size (e.g., 100 hands 50), this module uses the statistical vector to assign an "archetype" label to the opponent.Heuristic-Based: A simple if/then structure based on known benchmarks.52if (vpip < 10) and (pfr < 8): return 'NIT'if (vpip > 40) and (pfr < 15): return 'LOOSE-PASSIVE (FISH)'if (vpip > 40) and (pfr > 30): return 'MANIAC'ML-Based: A more advanced approach involves using unsupervised clustering algorithms (e.g., k-means) on opponent action frequencies to "discover" distinct player types.53Module 3: Counter-Strategy Library: This is the agent's "brain." It is a hard-coded mapping that links [Archetype] ->. This is the implementation of the "Adjustment Game" 47—using logic to select the maximal-exploit action.vs. NIT (Over-folder): increase_bluff_frequency() 1, use_smaller_bluff_sizing().10vs. LOOSE-PASSIVE (Calling Station): decrease_bluff_frequency() 1, increase_value_bet_sizing() 1, value_bet_thinner() (e.g., with middle pair).vs. MANIAC (Over-aggressive): widen_bluff_catching_range(), slow_play_nutted_hands() (check/raise).10This agent's logic is encapsulated in the following table, which serves as its primary knowledge base.Table 1: Player Archetype Taxonomy and Exploitative Counter-StrategiesArchetypeVPIP/PFR (6-max)Primary Leak / Imbalance Exploitative Counter-Strategy NIT (Nit)<15% / <10%Over-folds. Plays only premium hands.45 Betting is heavily weighted to value (High Polarity Imbalance).Bluff relentlessly. Steal blinds, 3-bet light. Fold immediately to their aggression.1TAG (Tight-Aggressive)~19% / ~17%Balanced. The "good player" default.45 Leaks are subtle (e.g., fit-or-fold on Turn).Default to GTO. Exploit specific, minor frequency errors (e.g., if C-Bet < 50%, bluff Turn).LAG (Loose-Aggressive)~27% / ~22%Over-bluffs. Plays too many hands aggressively.45 (Betting Volume Imbalance).Play tight, let them bluff. Widen calling range (bluff-catch). Slow-play premium hands to trap.10Loose-Passive (Fish)>30% / <15%Over-calls. Wants to "see the flop".52 (Betting Volume Imbalance - Call).Never bluff. Value bet relentlessly.1 Use large bet sizings with strong hands.10Maniac>40% / >30%Over-bets / Over-bluffs. Hyper-aggressive.45 (Betting Volume Imbalance - Bet).Wait for a monster hand. Let them build the pot. Trap and check-raise. (High-variance strategy).This node is the classic "exploitative" player.57 It will be extremely profitable against Nodes A1 and the general population of human players.11 However, its hard-coded, rule-based logic makes it predictable. It is vulnerable to a "Level 3" player 47 who models the modeler, and it will be systematically dismantled by a GTO agent (Phylum B).C. Node A3: The "Deep-Learner" (DQN Agent)Architecture: A model-free Deep Reinforcement Learning (DRL) agent. Unlike Node A2, which uses hard-coded logic, this agent learns the optimal exploitative policy through trial and error.19 It typically uses a Deep Q-Network (DQN) 23 or a policy gradient method like Proximal Policy Optimization (PPO).19Implementation (based on DQN / PyPokerEngine studies 23):State Representation: This is the most critical design choice. The engine's round_state 23 must be "flattened" into a fixed-size vector (tensor) to be fed into the neural network. This state vector must include:Card Information: Player's hole cards and all community cards (vectorized/embedded).Game Information: Current pot size, player stack sizes (self and opponents), and position.Betting History: A fixed-length queue representing the last N actions (e.g., 10 actions), encoding the action type and size.23Action Space: Handling NLHE's "infinite" action space (any bet size) is a major challenge. A hybrid approach is most effective 23:The network has two output heads.Head 1 (Q-Values): Predicts the Q-value for a set of discrete actions (e.g., Fold, Call, Raise).Head 2 (Probabilities): Predicts a probability distribution over a set of discretized bet amounts (e.g., {25% Pot, 50% Pot, 75% Pot, 100% Pot, All-in}).The agent first selects the action with the highest Q-value. If that action is "Raise," it then selects the bet size with the highest probability from the second head.Training Loop (Fictitious Self-Play):A DQN cannot be trained against a single, static opponent (like A1); it will overfit and learn a trivial, non-general policy. It must be trained against a pool of opponents.61Training Pool: This pool should contain Node A1 (The NIT), multiple copies of Node A2 (Statistician) configured to play different archetypes (LAG, Fish), and, critically, past snapshots of the Node A3 agent itself.Algorithm: The "gold standard" algorithm for this is Neural Fictitious Self-Play (NFSP).63 Standard DQN and other common RL methods can diverge (fail to learn) in imperfect-information games. NFSP solves this by combining a DRL agent (learning the best response) with a supervised learning agent (learning the average policy over time). This dual-network approach has been shown to converge toward a Nash Equilibrium.63This agent is more powerful and general than Node A2. It does not "know" its opponent is a "NIT." It simply learns that "in this state, against this pool of opponents, this action has the highest long-term EV".23 This makes it more robust but potentially less adaptive in the short term to a specific opponent it has just met. It learns the average best exploit for the entire population.III. Phylum B: The GTO Lineage (Game-Theoretic Optimal Agents)Phylum Goal: This lineage has a fundamentally different objective from Phylum A. The goal is not to maximize profit, but to minimize exploitability.64 This is achieved by developing a "Game Theory Optimal" (GTO) strategy.3 A GTO strategy is a defensive one 6 that seeks a Nash Equilibrium.5 In a Nash Equilibrium, no player can unilaterally change their strategy to increase their profit.67 Therefore, an agent playing a perfect GTO strategy cannot lose money in the long run, regardless of what the opponent does.2A. Node B1: The "Theorist" (Tabular CFR Agent)Architecture: This is a "toy" implementation of the foundational GTO algorithm: Counterfactual Regret Minimization (CFR).68 This algorithm is the theoretical basis for all modern superhuman poker AI.Implementation:Game Scope: This implementation must not be for full NLHE. The state space of NLHE is computationally intractable (estimated at $10^{161}$ states 25). This agent must be built for a "toy game" with a small, solvable game tree, such as:Kuhn Poker: A 3-card, 1-bet-round game.Leduc Poker: A 6-card, 2-street game.24 The RLCard framework provides an excellent example, leduc_holdem_cfr.18Core Logic (Tabular CFR): The algorithm works by iterating through self-play millions of times to converge on an equilibrium.70Information Sets (Infosets): The algorithm stores data in "infosets." An infoset is a collection of all game states that are indistinguishable to the current player 69 (e.g., "I have a Queen, I am first to act, the opponent bet $1").Regret Calculation: For every infoset, the algorithm maintains a table of cumulative "counterfactual regrets." The regret for an action is defined as the difference in EV between what-if-I-had-taken-this-action and the EV-of-my-current-strategy.71 Regret(a) = EV(a) - EV(current_strategy).Strategy Update: After each iteration, the agent updates its strategy for the next one. The new strategy is to play actions in proportion to their positive cumulative regret.72 This is "Regret Matching." Prob(action_a) = max(0, Cumulative_Regret(a)) / SUM(all_positive_regrets).Convergence: As the number of iterations approaches infinity, the average strategy (the average of all strategies played over all iterations) provably converges to a Nash Equilibrium.6Role in DAG: This node is a prerequisite learning node. It produces no playable NLHE agent. Its purpose is to force the developer to master the complex, non-intuitive mechanics of CFR and regret matching in a simple, tabular environment. It is impossible to build the superhuman Node B3 without first understanding the core logic of Node B1.B. Node B2: The "Blueprint" (Offline Abstraction + MCCFR)Architecture: This is the offline computation stage that creates the "Blueprint Strategy" used by superhuman AI like Libratus 25 and Pluribus.73 This node solves the problem of NLHE's intractable game tree by first solving a simpler, smaller, abstracted version of the game.The imperative for this node is Abstraction.74 The game must be shrunk to a solvable size.76 This is a lossy compression, and it happens in two dimensions:Implementation - Component 1: Abstraction:Action Abstraction: The infinite set of possible bet sizes in "no-limit" 14 is discretized into a small, fixed set of legal actions.77Example: At any decision point, the agent is only allowed to bet {50% Pot, 100% Pot, or All-in}.Vulnerability: This is a known source of weakness. If the opponent uses a bet size not in this abstract set (e.g., a 25% "min-bet"), the agent is "off-tree" and does not have a pre-computed response. This vulnerability must be solved by Node B3.77Hand Abstraction (Bucketing): The 1,326 unique preflop hands 79 and millions of postflop hand-plus-board combinations are grouped into a manageable number of "buckets".76 Hands within a bucket are treated as strategically identical.Method 1: K-Means Clustering 79: This is the simplest approach.Metric: Define a distance metric for hands, such as raw, all-in equity against a random hand (e.g., value = wins - losses + draws/2 79).Algorithm: Use k-means to cluster the 1,326 preflop hands into k buckets (e.g., k=15).79Method 2: Potential-Aware Abstraction 81: This is a vastly superior and more modern approach.84Logic: Raw hand strength is a poor metric. A hand like 7h 8h on a Kh 9h 2c board has low current strength but enormous potential to become a flush or straight. A hand like Ac Kc has high strength but low potential (it's unlikely to improve).Algorithm: This method clusters hands based on their future win/loss distribution, not just their current strength. This results in far more strategically coherent buckets.81Implementation - Component 2: Solving the Abstract Game:Once the new, smaller, abstracted game tree is built, it is solved offline.Because the game is still too large for tabular CFR (Node B1), this node uses Monte Carlo CFR (MCCFR).29MCCFR is a sampling-based variant. Instead of traversing the entire game tree on each iteration, it only samples a few paths, making it practical for large (but abstracted) games.72Output: The output of this (weeks- or months-long) computation is a single, massive "Blueprint Strategy" file. This file is a lookup table that maps every abstracted infoset to a mixed strategy (i.t., a probability distribution over the allowed abstract actions).25C. Node B3: The "Libratus" (Blueprint + Real-Time Subgame Solving)Architecture: This is the complete, superhuman Heads-Up (2-player) GTO agent. It is a hybrid system that recognizes the "Blueprint" from Node B2 is a necessary but insufficient component. The blueprint is a coarse approximation, and its abstractions are its weaknesses.29 Node B3 "patches" these weaknesses in real-time.25Implementation (The 3-Module System of Libratus 25):Module 1: Blueprint Strategy (Node B2):The agent uses the static, pre-computed Blueprint from Node B2 to play the early betting rounds (e.g., Preflop and Flop). In these parts of the game, the blueprint's abstraction can be very detailed and is highly accurate.25Module 2: Nested Subgame Solving (Real-Time):When a later, more complex street is reached (e.g., the Turn or River), the agent discards the coarse blueprint strategy for the rest of the hand.25It then launches a new CFR computation in real-time (in the seconds it has to think). This computation solves only the "subgame" from the current game state to the end of the hand.87Key Detail: This real-time subgame solve uses a much finer-grained abstraction (e.g., more bet sizes) or, in Libratus's case, no card abstraction at all.25 This "patches" the holes in the blueprint, allowing the agent to play the complex later streets with near-perfect precision.25Module 3: Self-Improvement (Handling "Off-Tree" Actions):This module solves the abstraction vulnerability identified in Node B2.25Problem: What happens when an opponent uses a bet size (e.g., 25% pot) that was not in the blueprint's {50%, 100%, All-in} abstraction?.77Solution: Libratus logs this "off-tree" action. In the background (e.g., overnight), it runs a new, intensive subgame computation to find the perfect GTO response to that specific bet size. It then "patches" this new branch and its solution into the master blueprint.25This "self-improvement" module allows the agent to progressively perfect its blueprint by solving for the exact exploits its opponents try to use against it.This hybrid "Blueprint + Real-Time Solve" model is the fundamental breakthrough that allowed Libratus to achieve superhuman GTO play.25 It perfectly balances the impossibility of a full-game real-time solve with the inherent weakness of a purely static, abstracted blueprint.IV. Phylum C: The Hybrid & Next-Generation LineagePhylum Goal: This lineage explores alternative, state-of-the-art architectures that challenge the Phylum B (CFR-centric) model. These agents use different core algorithms (MCTS, NNs) or entirely new paradigms (LLMs) to achieve or surpass superhuman play, often with different performance trade-offs (e.g., speed, scalability, or memory).A. Node C1: The "DeepStack" (Continual Re-solver)Architecture: DeepStack is the other superhuman AI that defeated professional players alongside Libratus.7 It is a direct competitor to Node B3 (Libratus) but features a fundamentally different and, in many ways, more elegant architecture.Key Difference: DeepStack has no full-game blueprint.64Implementation 64:DeepStack's design is based on "continual re-solving" and a learned "intuition."Continual Re-solving: At every decision point (even preflop), DeepStack re-solves the game from the current state forward. However, unlike Libratus's full subgame solve, DeepStack's search is depth-limited (e.g., it only looks 2-3 actions ahead).The "Intuition" (NN as a Value Function): This is the core of the breakthrough. How does DeepStack evaluate the "leaf" nodes of its shallow search?It uses a deep neural network 64 that has been pre-trained on millions of self-play hands.64This NN acts as a value function. It takes any game state (cards, pot, ranges) as input and outputs the Expected Value (EV) of that state.64This NN is DeepStack's "intuition".64 It provides the "gut feeling" of a grandmaster, allowing the agent to terminate its search early but with a highly accurate value estimation.Libratus (B3) vs. DeepStack (C1) - The Core Architectural Debate:This is the central strategic debate in GTO AI development.Node B3 (Libratus): "CFR-centric."Pro: More theoretically pure GTO. The blueprint is a true equilibrium (for the abstraction).Con: Requires massive offline computation (months) to build the blueprint.25Node C1 (DeepStack): "RL-centric."Pro: No blueprint required. Can be deployed "from scratch".64 Computation is all real-time.Con: The strategy's "GTO-ness" is dependent on the accuracy of the NN's value function.DeepStack is essentially a heuristic search algorithm (like in chess) that was provably sound for imperfect-information games, a major theoretical achievement.7B. Node C2: The "Alpha" (End-to-End Self-Play RL)Architecture: This node represents an adaptation of DeepMind's "AlphaZero" 90 for poker, as exemplified by projects like AlphaHoldem.8Implementation:Core Model: A (pseudo-siamese) neural network 8 that takes the game state as input and outputs two heads:Policy Head: A probability distribution over all legal actions (e.g., P(fold) = 10%, P(call) = 60%, P(raise_50%) = 30%).Value Head: A single scalar value representing the Expected Value (EV) of the current state.Algorithm: Monte Carlo Tree Search (MCTS).90At each decision, the agent runs thousands of MCTS "simulations."The Policy Head guides the MCTS, telling it which branches of the tree are more promising to explore.The Value Head evaluates the leaf nodes of the MCTS search.Training: This is pure, end-to-end self-play.8 The results of the MCTS (which is a "smarter" policy than the NN's raw output) are used as the new training target for the neural network. The NN gets smarter, which makes the MCTS smarter, and the loop repeats.This is the "dream" architecture. It is an elegant, end-to-end learning system that bypasses the explicit, manual, and domain-specific work of CFR (Node B1) and Abstraction (Node B2).8 The NN learns these GTO concepts implicitly.However, a critical distinction remains: CFR (Phylum B) is provably guaranteed to converge to a Nash Equilibrium.6 For MCTS/RL in imperfect-information games, this convergence is an empirical result, not a guaranteed one. General RL methods like PPO are known to struggle with imperfect information.60 This node is lightweight 8 and fast 8, but its theoretical soundness is less robust than Phylum B.C. Node C3: The "ChatBot" (LLM-Based Solver)Architecture: This is the newest, bleeding-edge paradigm. It leverages Large Language Models (LLMs) to play poker.9 Examples include PokerGPT 9 and SpinGPT.92Implementation:Data Acquisition: The process begins by scraping massive volumes of textual hand histories from online poker platforms.93 These logs contain the blinds, stacks, cards, and a natural language description of the action (e.g., "Player A bets $10," "Player B raises to $30").93Prompt Engineering: The core of the system is a prompt that converts the current game state (player stacks, blinds, action history, board cards) into a single, comprehensive natural language string.9Training (SFT + RL):Supervised Fine-Tuning (SFT): A lightweight, pre-trained LLM (e.g., Llama) 9 is fine-tuned on a dataset of (prompt_state, expert_action) pairs, where the "expert action" comes from the scraped data of high-winning players.96Reinforcement Learning (RL): The SFT model is then refined using reinforcement learning (similar to RLHF).9 The model plays hands, and its actions are given a "reward" based on their EV, which can be generated by a GTO solver or from human expert feedback.93The "killer feature" of this architecture is scalability to multi-player games.Phylum B (CFR) and Phylum C (DeepStack) are fundamentally 2-player (Heads-Up) architectures.In multi-player games, the game tree's complexity grows exponentially, and the concept of a single Nash Equilibrium breaks down.9 This makes CFR-based models (like Pluribus, the 6-player bot) extraordinarily complex.73LLMs, however, scale natively. Handling 6 players instead of 2 is simply a matter of a longer prompt.9This node represents the future path for multi-player and interpretable AI (it can explain its decision in natural language 93). However, current LLMs are less precise than pure solvers, as they are trained on human data and can make "deep-stack errors" (like limping) that a solver never would.96Table 2: Comparison of Superhuman AI ArchitecturesNodeArchitectureCore AlgorithmAbstraction MethodBlueprint?Computation ModelPrimary StrengthB3LibratusCounterfactual Regret Minimization (CFR) 25Manual (Hand/Action Bucketing) 99Yes (Massive)Massive Offline (Blueprint) + Real-time (Subgame Solve) 25GTO-Pure (2-Player)C1DeepStackContinual Re-solving + Heuristic SearchLearned (NN Value Function) 64No 64High Real-time Solve (for every action) 64Fast, Blueprint-Free GTO (2-Player)C2AlphaHoldemMonte Carlo Tree Search (MCTS) 90Learned (NN Policy/Value Net) 8NoEnd-to-End Self-Play (RL) 8Elegant, Lightweight, Fast (2-Player)C3PokerGPTTransformer (LLM) 9Learned (Text Embeddings)NoSFT (Human Data) + RLHF 93Multi-Player Scalable 9, InterpretableV. The Iteration Engine: The Tournament & Evaluation FrameworkThis is the final and most critical component, designed to satisfy the user's primary goal: "to iterate and improve" by "seeing which players work and don't work." This framework implements the edges of the DAG. It is the "Arena" where all agents (Nodes A1..C3) compete, and the "Scorecard" that defines what it means to "win."A. The "Arena": A Multi-Agent Tournament FrameworkDirective: Build a server application (the "Arena") that can programmatically load, instantiate, and run any two or more agents from the DAG against each other in a high-speed tournament.Implementation:Agent Pool: The Arena server must maintain a registry of all compiled agents (A1, A2, A3, B3, C1, C2, C3, etc.).61 This is the "pool" used for training (e.g., for Node A3) and for evaluation.100Matchmaking: The server must have an API to launch matches, such as run_match(agent_a='B3', agent_b='A2_fish_config', num_hands=10000). This allows for head-to-head (2-player) or full-ring (6-player) games.101Game Environment: The Arena will instantiate the Gen-0 Game Engine (I.A) and pass actions and states between it and the competing agents.Logging: The Arena must log every single state, action, and outcome to a database for analysis.102B. The "Scorecard": Quantifying PerformanceDirective: Implement the two distinct and separate metrics for "winning." A critical failure in AI development is using the wrong metric for the wrong agent.The research clearly separates two different goals: Phylum A (Exploitative) is measured by its profitability (win rate) 1, while Phylum B (GTO) is measured by its defensive soundness (exploitability).3Implementation:Metric 1: Win Rate (mbb/g):Definition: "milli-big-blinds per game" (mbb/g) or "big blinds per 100 hands" (bb/100).103 This is the standard metric for professional players. 10 mbb/g = 1 bb/100.7Use: This is the only metric that matters for Phylum A (Exploitative). A win rate of 50 mbb/g (5 bb/100) is considered a very strong, professional margin.7Statistical Note: Poker has enormous variance. A result over 10,000 hands may not be statistically significant. The implementation must incorporate a variance reduction tool like AIVAT.105 AIVAT is a low-variance assessment tool that was used to prove the statistical significance of AI victories against pros, requiring 44x fewer games to draw the same conclusion.105Metric 2: Exploitability (mbb/g):Definition: The theoretical maximum win rate (in mbb/g) that a perfect, omniscient opponent (a "Best Response" agent) could achieve against our strategy.64Use: This is the only metric that matters for Phylum B (GTO). The goal is to minimize this value to 0 mbb/g.64How to Calculate: Calculating true exploitability is computationally intractable.64 This must be approximated by building a Best Response (BR) Agent.62Local Best Response (LBR): An approximation that calculates a lower bound on exploitability by assuming no more bets will be placed.64 DeepStack, for example, achieved an LBR of 0 mbb/g, meaning this simple check could not find a flaw.64RL Best Response (RL-BR): This is the gold standard for large games, as implemented in the PokerRL framework.62 The methodology is as follows:Take the "frozen" GTO agent (e.g., Node B3).Train a new DQN agent (like Node A3) from scratch, where its only opponent is the frozen B3 agent.Let this DQN train for millions of hands, learning every possible weakness and leak.The final, converged win rate of this specialized DQN is the exploitability of the GTO agent.62C. The Feedback Loop: The Path to the "Ultimate" PlayerThis section defines the iterative R&D plan—the "edges" of the DAG—that leads to the final, winning node.Path 1 (GTO Purity): The Quest for 0 ExploitabilityThis is the research path for Phylum B/C.Build: Node B3 (Libratus) or C1 (DeepStack).Build: An RL-BR (Best Response) agent to test it (V.B).Measure: Run the RL-BR agent and measure its final win rate. This is B3's exploitability.Analyze: If exploitability is > 0 mbb/g, analyze the RL-BR agent's policy. It will highlight the exact leak (e.g., "B3 under-bluffs on this river card").Iterate: Fix the leak (e.g., patch the blueprint (B2) or retrain the value-net (C1)) and go back to step 3. Repeat until exploitability is ~0.Path 2 (Exploitative Power): The Quest for Max ProfitThis is the research path for Phylum A.Build: A "population" of "bad" agents (A1, A2-NIT, A2-Fish).61Build: Node A3 (DQN).Train: Train A3 against this population using NFSP.63Measure: Run A3 in the Arena (V.A) against the population and measure its win rate (mbb/g) (V.B).Iterate: Add new, "bad" agents to the population (e.g., an A2-Maniac). This makes the population more diverse and robust. Go back to step 3 and retrain A3.Path 3 (The Grand Final): The Ultimate Node (D1) "Adaptive GTO"This path provides the final, nuanced answer. The research clearly indicates that a pure GTO agent (B3) is not the "winningest" player, because it leaves money on the table.2 It plays a "perfectly balanced" (e.g., 50% bluff / 50% value) strategy even against an opponent (A1) who folds 100% of the time. This is "sound" but unprofitable.106The "ultimate" player is a hybrid.10Architecture: Create a new agent, Node D1 (Adaptive GTO).Default Strategy: D1's default, baseline strategy is a pure-GTO agent (Node B3 or C1).Parallel Modeling: In the background, D1 runs the opponent-modeling module from Node A2 (Statistician) on the current opponent.The "Nodelock":The agent plays GTO until the A2 module reports a high-confidence leak in the opponent (e.g., opponent.fold_vs_3bet_stat > 80% over 200 hands).When this threshold is met, the agent "nodelocks".109 It deviates from its GTO default to play a pre-computed, maximal-exploit counter-strategy 1 (e.g., "3-bet 100% of hands").If the opponent adjusts, their stats will change, the confidence will drop, and D1 will revert to its default GTO strategy.This "Adaptive GTO" agent (D1) is the ultimate winner of the DAG. It is unexploitable (GTO) against unknown or strong players, but it transforms into a maximally-profitable (exploitative) agent against weak, known players. It achieves both Phylum's goals simultaneously.
