# Ultimate Implementation Plan: A Directed Acyclic Graph for "Random Number Texas Hold'Em"

## Executive Overview: The Directed Acyclic Graph of Agents

This document presents a comprehensive, expert-level implementation plan for creating a winning poker bot for the "Random Number Texas Hold'Em" variant. It synthesizes multiple research paths into a single, structured Directed Acyclic Graph (DAG).

Each "Node" in this graph represents a distinct, buildable, and testable AI agent. The "Edges" represent dependencies, with each level building upon the last. The plan is organized into "Phylums"—evolutionary lineages of strategy that must be developed in parallel and integrated at the end.

- **Phylum A (GTO):** The defensive lineage. Focuses on unexploitable, balanced, and mathematically sound strategies (GHI-Core).
- **Phylum B (Exploitative):** The offensive lineage. Focuses on maximizing win rate by identifying and countering opponent weaknesses (Opponent Modeling).
- **Phylum C (Advanced):** The optimization lineage. Focuses on game-specific mathematical advantages (Bet Sizing, Score Awareness) that are critical for this specific variant.

The "Ultimate Player" is a hybrid agent (Phylum D) that integrates all three lineages—playing an unexploitable GTO default, switching to exploitative play when confident, and applying advanced risk/betting math to every decision.

---

## I. Gen-0: Foundational Infrastructure

This root node provides the environment, rules, and mathematical "language" that all subsequent agents will depend on.

### A. Core Game Mechanics (The Environment)

This is a **continuous Kuhn poker variant** with the following unique properties:

1.  **Card Distribution:** Each player receives a single card, `x`, uniformly distributed on `[0, 1]`.
2.  **Showdown:** The card value `x` represents the _exact win probability_ at showdown. Showdown is deterministic: the higher card always wins.
3.  **Betting Structure:**
    - Small Blind: 1 point (acts first).
    - Big Blind: 2 points.
    - Players alternate roles.
    - Minimum bet doubles every 100 hands.
    - Maximum bet = `min(player1_score, player2_score)`.
    - All bets must be multiples of `minbet`.
4.  **Game Termination:** One player accumulates all 200 points.

### B. Core Mathematical Principles (The Lexicon)

This module implements the foundational logic required for all rational agents.

- **Pot Odds:** `pot_odds = call_amount / (pot + call_amount)`
  - The reward-to-risk ratio for making a call.
- **Required Equity:** `required_equity = call_amount / (pot + call_amount)`
  - The minimum win probability (card value) needed for a call to be profitable. An agent should only call if `card > required_equity`.
- **Optimal Bluffing Frequency:** `bluff_freq = call_amount / (pot + call_amount)`
  - The theoretically unexploitable frequency to bluff. Example: To make a 1-point bet into a 4-point pot, the bettor must be bluffing `1 / (4 + 1) = 20%` of the time.
- **Expected Value (EV):** `EV = P(win) * winnings - P(lose) * loss`
  - The core metric for all decisions. A rational agent compares the EV of folding, calling, and raising, then selects the action with the highest EV.

### C. Baseline Agents (The Benchmarks)

These simple, non-learning agents establish the performance floor and are used for testing.

- **B0.1: AllInPlayer:** Bets entire stack every hand. (Expected Win Rate: \~30%)
- **B0.2: FoldBot:** Always folds unless Big Blind with card \> 0.9. (Expected Win Rate: \~10%)
- **B0.3: CallBot:** Always calls, never raises. (Expected Win Rate: \~45-50%)
- **B0.4: John1:** A known baseline using simple card-strength and pot-size thresholds. (Expected Win Rate: \~59%)

---

## II. Phylum A: The GTO Lineage (Balanced Strategies)

**Goal:** To create a defensively sound, unexploitable "Game Theory Optimal" (GTO) agent. This agent makes decisions based on mathematically balanced principles, position, and mixed strategies to prevent exploitation.

### A1. SimpleThreshold Player

- **Dependencies:** Gen-0
- **Core Concept:** Basic threshold strategy.
- **Strategy:**
  - Fold if card \< 0.3
  - Call if 0.3 \<= card \< 0.7
  - Raise if card \>= 0.7
- **Weakness:** Highly predictable and exploitable.

### A2. PositionAware Player

- **Dependencies:** A1
- **Core Concept:** Exploit positional advantage. The Big Blind (BB) has already invested 2x and acts last, while the Small Blind (SB) acts first.
- **Strategy:** Adjust thresholds based on position.
  - **Small Blind (tighter):** Fold \< 0.35, Call 0.35-0.75, Raise \> 0.75
  - **Big Blind (wider/defensive):** Fold \< 0.25, Call 0.25-0.70, Raise \> 0.70

### A3. MixedStrategy Player

- **Dependencies:** A2

- **Core Concept:** Introduce randomization and polarization to prevent exploitation.

- **Strategy:**

  - **Polarize Ranges:** Only raise with very strong hands (value) or a select few weak hands (bluffs). Call/Fold with medium-strength hands.
  - **Implement GTO Bluffing:** Use the optimal bluffing frequency from the Gen-0 Lexicon.

- **Implementation Logic:**

  ```python
  import random

  def should_bluff(card, pot, minbet):
      # Bluff with bottom 15% of range
      if card < 0.15:
          # Bluff frequency should match pot odds offered
          bluff_frequency = minbet / (pot + minbet)
          return random.random() < bluff_frequency
      return False

  def bet_decision(card, pot, minbet):
      if card > 0.75:  # Strong value hands
          return pot + minbet  # Always raise
      elif card < 0.15 and should_bluff(card, pot, minbet):
          return pot + minbet  # Bluff raise
      elif card < 0.30:
          return 0  # Fold weak non-bluffs
      else:
          return pot  # Call with medium hands
  ```

### A4. OptimalThreshold Player

- **Dependencies:** A3

- **Core Concept:** A full GTO approximation using mathematically derived thresholds. This is the "final boss" of the GTO lineage and serves as the baseline strategy for the Ultimate Hybrid.

- **Strategy:** Use a refined, balanced set of thresholds derived from Kuhn poker theory.

- **Implementation Logic:**

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

---

## III. Phylum B: The Exploitative Lineage (Opponent Modeling)

**Goal:** To maximize win rate by identifying and exploiting opponent tendencies. This agent builds a statistical profile of the opponent and deploys a specific counter-strategy.

### B1. StatisticalTracker

- **Dependencies:** Gen-0
- **Core Concept:** Collect and store opponent statistics after each hand.
- **Tracked Metrics:**
  - `hands_played`: Total hands.
  - `vpip`: (Voluntarily Put In Pot) % of hands played (called or raised).
  - `pfr`: (Pre-Flop Raise) % of hands raised.
  - `folds`: % of hands folded to a bet.
  - `calls`: % of hands called.
  - `raises`: % of hands raised.
  - `aggression_factor`: `(bets + raises) / calls`.
  - `showdowns`: A list of `(their_card, their_bet, result)` tuples.

### B2. Bayesian Opponent Classifier

- **Dependencies:** B1

- **Core Concept:** Use Bayesian inference to classify the opponent into one of several known archetypes based on their tracked stats.

- **Opponent Archetypes:**

  - **Tight-Passive (Nit):** High fold %, low VPIP, low PFR. (Leaks: Over-folds).
  - **Loose-Passive (Calling Station):** High VPIP, low PFR, high call %. (Leaks: Over-calls).
  - **Tight-Aggressive (TAG):** Low VPIP, high PFR (close to VPIP). (Leaks: Predictable, plays GTO).
  - **Loose-Aggressive (Maniac):** High VPIP, high PFR, high aggression. (Leaks: Over-bluffs).

- **Implementation Logic:**

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

### B3. ExploitationEngine

- **Dependencies:** B2

- **Core Concept:** A library of hard-coded counter-strategies. The engine selects the correct counter based on the classifier's output.

- **Exploitation Strategies:**

  **1. Exploit Tight-Passive (Folders):**

  - **Strategy:** Bluff relentlessly with a high frequency and wide range.
  - **Logic:**
    ```python
    def exploit_folder(self, opponent_stats):
        if opponent_stats.fold_to_raise_pct > 0.60:
            self.bluff_threshold = 0.35  # Bluff with bottom 35%
            self.min_bluff_size = minbet  # Small bluffs work
    ```

  **2. Exploit Loose-Passive (Calling Stations):**

  - **Strategy:** Never bluff. Value bet with a much wider (thinner) range. Use larger bet sizes.
  - **Logic:**
    ```python
    def exploit_caller(self, opponent_stats):
        if opponent_stats.call_pct > 0.70 and opponent_stats.raise_pct < 0.15:
            self.bluff_threshold = 0.0  # Never bluff
            self.value_threshold = 0.55  # Value bet much wider
    ```

  **3. Exploit Loose-Aggressive (Maniacs):**

  - **Strategy:** Stop bluffing. Tighten up, wait for strong hands, and "trap" (call them down or check-raise).
  - **Logic:**
    ```python
    def exploit_maniac(self, opponent_stats):
        if opponent_stats.raise_pct > 0.50:
            self.slow_play_threshold = 0.85  # Trap with top 15%
            self.fold_threshold = 0.45  # Fold medium hands
    ```

---

## IV. Phylum C: Advanced & Game-Specific Strategies

**Goal:** To implement high-leverage mathematical optimizations specific to this game's unique rules (known probability and tournament format). These are not independent strategies but "multipliers" that improve all other agents.

### C1. Kelly-Based Bet Sizing

- **Dependencies:** Gen-0

- **Core Concept:** This is the single most powerful concept for this game. Because the card value `p` is the _exact win probability_, the **Kelly Criterion** can be used to determine the mathematically optimal bet size to maximize long-term bankroll growth.

- **Strategy:**

  - **Full Kelly Formula:** `f* = 2p - 1`, where `p` is your card value (win prob) and `f*` is the fraction of your stack to bet.
  - **Problem:** Full Kelly has extremely high variance and can lead to ruin.
  - **Solution: Fractional Kelly:** Use a fraction (e.g., 0.25x to 0.5x) of the Kelly bet. This retains most of the growth rate while dramatically reducing variance.

- **Implementation Logic:**

  ```python
  def fractional_kelly(card_value, stack, kelly_multiplier=0.4):
      # Kelly formula for even-money bets: f* = 2p - 1
      kelly_fraction = 2 * card_value - 1

      if kelly_fraction <= 0:
          return 0  # Fold or check

      # Use 0.4x Kelly for reduced variance
      conservative_fraction = kelly_fraction * kelly_multiplier
      optimal_bet = conservative_fraction * stack

      return min(optimal_bet, stack)
  ```

### C2. ICM & Score-Aware Meta-Strategy

- **Dependencies:** Gen-0
- **Core Concept:** The game is a "winner-take-all" tournament. Chips have non-linear value. The agent's strategy must change based on the score and the blind level.
- **Strategy:**
  - **Score-Differential Awareness (ICM):**
    - **When Leading (e.g., 150 vs 50):** Play **risk-averse**. Avoid high-variance, all-in situations unless you are a huge favorite. Protect your lead.
    - **When Trailing (e.g., 50 vs 150):** Play **risk-seeking**. Increase variance. You must take risks (e.g., bluff more, call lighter) to catch up.
  - **M-Ratio Awareness (Blind Levels):**
    - **M-Ratio:** `stack / (small_blind + big_blind)`
    - As the `minbet` doubles, the M-Ratio drops.
    - **High M (Early Game):** Play deep-stacked, nuanced poker.
    - **Low M (Late Game):** Shift to a simpler, more aggressive "push/fold" strategy, as the blinds are too large to play small pots.

---

## V. Phylum D: The Ultimate Hybrid Player

**Goal:** To integrate all three phylums into a single, elite agent that is unexploitable by default but maximally exploitative when possible, all while using optimal bet sizing and risk management.

### D1. AdaptiveHybrid Player

- **Dependencies:** A4, B3, C1, C2

- **Core Concept:** An "Adaptive GTO" agent that uses GTO as a baseline, but "nodelocks" onto an exploitative counter-strategy once its opponent model reaches a high confidence threshold.

- **Decision-Making Flow:**

  1.  **Start Hand:** Update game state (blinds, scores).
  2.  **Get GTO Decision:** The **GTO Core (A4)** provides the default, unexploitable action (e.g., "Fold, 35%").
  3.  **Get Opponent Model:** The **Classifier (B2)** provides the opponent's likely archetype and a confidence score (e.g., "Maniac, 80% confidence").
  4.  **Strategy Selection:**
      - `if confidence < 0.7:`
        - `strategy = GTO`
      - `else:`
        - `strategy = ExploitationEngine.get_counter(opponent_type)`
  5.  **Get Base Action:** The selected strategy (GTO or Exploit) provides a base decision (e.g., "Raise").
  6.  **Apply Bet Sizing:** The **Kelly Sizing (C1)** module calculates the _size_ of that raise (e.g., "Raise 30 points").
  7.  **Apply Risk Adjustment:** The **ICM/Score (C2)** module reviews the decision.
      - _Example:_ The Kelly bet is 30 points, but we are leading 180-20. The C2 module overrides and reduces the bet to 10 points to minimize risk.
  8.  **Execute Final Action.**
  9.  **End Hand:** Update the **StatisticalTracker (B1)** with the results.

### D2. Multi-Armed Bandit (Strategy Selection)

- **Dependencies:** D1
- **Core Concept:** A more advanced method for strategy selection. Instead of a simple `if confidence > 0.7` check, the agent uses a Multi-Armed Bandit (MAB) algorithm to _learn_ which counter-strategy (GTO, Exploit-Folder, Exploit-Caller) is most profitable against the _current_ opponent.
- **Implementation:**
  - Each counter-strategy is an "arm" of the bandit.
  - The "reward" is the EV won from the hand.
  - The agent uses an algorithm (like UCB1) to balance **exploration** (trying a new strategy) and **exploitation** (using the strategy that has worked best so far).

---

## VI. The Iteration Engine (Testing & Evaluation)

A structured framework for testing, benchmarking, and iterating on every agent in the DAG.

### A. The "Arena" (Testing Framework)

A script that programmatically pits agents against each other.

- **Quick Test (2-3 min):**
  - `play(MyNewPlayer, training_opponents[0:5], 200, 1)`
  - **Target:** Get quick feedback. Must beat baselines.
- **Full Training Test (30-40 min):**
  - `play(MyNewPlayer, training_opponents, 200, 0)`
  - **Target:** Official performance metric against all 90+ opponents. Target 71%+.
- **Detailed Analysis Test:**
  - `play(MyNewPlayer, training_opponents, 200, 2)`
  - **Target:** Get a per-opponent win rate to identify weak matchups.
- **Specific Opponent Deep Dive:**
  - `pokerTest(MyNewPlayer, John1, ngames=1000, verbosity=1)`
  - **Target:** Debug specific interactions.

### B. The "Scorecard" (Performance Tracking)

Maintain a spreadsheet to track progress and prevent regressions.

| Player Name      | Phylum | Quick Test (5 opps) | Full Test (90 opps) | Notes                   |
| :--------------- | :----- | :------------------ | :------------------ | :---------------------- |
| AllIn            | Gen-0  | 35%                 | 30%                 | Baseline                |
| John1            | Gen-0  | 60%                 | 59%                 | Heuristic Baseline      |
| PositionAware    | A2     | 62%                 | 60%                 | GTO base                |
| OptimalThreshold | A4     | 68%                 | 66-69%              | Solid GTO Core          |
| ...              | ...    | ...                 | ...                 | ...                     |
| KellyPlayer      | C1     | 70%                 | 71%                 | Kelly bet sizing is key |
| UltimateHybrid   | D1     | **?**               | **?**               | Target 75%+             |

### C. Implementation Roadmap

1.  **Phase 1: Foundation (Days 1-2)**
    - **Implement:** Gen-0 (Engine, Math, Baselines), Phylum A (A1, A2).
    - **Goal:** Beat John1 (59%) with a position-aware agent.
2.  **Phase 2: GTO Core (Days 3-4)**
    - **Implement:** Phylum A (A3, A4 - MixedStrategy, OptimalThreshold).
    - **Goal:** Create an unexploitable GTO agent with a 68-71% win rate.
3.  **Phase 3: Advanced Core (Days 5-6)**
    - **Implement:** Phylum C (C1 Kelly Sizing, C2 ICM/Score).
    - **Goal:** Integrate Kelly and ICM to break 72-74%.
4.  **Phase 4: Exploitation (Days 7-8)**
    - **Implement:** Phylum B (B1, B2, B3 - Full Opponent Modeling).
    - **Goal:** Develop the exploitative counters.
5.  **Phase 5: Elite Integration (Days 9-10)**
    - **Implement:** Phylum D (D1/D2 - The Ultimate Hybrid).
    - **Goal:** Combine all phylums. GTO baseline + Exploitative overlays + Kelly/ICM optimization. **Target: 75-78%+ win rate.**
