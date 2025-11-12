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
    “
Level 1 (Foundation)
    “
Level 2 (GTO Core)
    “
Level 3 (Opponent Modeling)
    “
Level 4 (Adaptive & Exploitative)
    “
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

| Player Name | Level | Quick Test (5 opps) | Full Test (90 opps) | Time (seconds) | Notes |
|------------|-------|---------------------|---------------------|----------------|-------|
| AllIn | B0.1 | 35% | 30% | 3.5s | Baseline |
| John1 | B0.4 | 60% | 59% | 10s | Simple heuristic |
| SimpleThreshold | F1.1 | ? | ? | ? | Position-aware thresholds |
| ... | ... | ... | ... | ... | ... |

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

---

**Document Version:** 1.0
**Last Updated:** 2025-11-11
**Author:** Claude Code Research Team
