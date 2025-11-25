# Poker Bot Improvement Plan: Target 60%+ Win Rate

## Current Status

- Current: 43.4% vs training opponents
- John3: ~70% vs training opponents
- Target: 60%+

## Key Insights from Analysis

### John3's Winning Strategy

- Almost never bets (3% SB, 2.3% BB)
- Checks back 97.7% as BB
- Only bets with near-nuts (avg card 0.988)
- Folds weak hands as SB (cards < 0.17)
- Calls 60% when facing raises

### Worst Opponents (P131, P071, P159)

- P131/P071: Aggressive (58% raise), tight value (avg 0.704), fold 42% to raises
- P159: Extremely passive (7% raise), folds 66% to raises

### Key Problem

Our GTO bluffing (~11% SB, ~17% BB) is being exploited by calling stations.
John3 succeeds by almost never bluffing and only betting with near-nuts.

---

## Phase 1: Adopt John3-like Passive Strategy

### Step 1.1: Reduce bluff frequency dramatically

- Change SB bluff threshold from ~11% to ~3% (a = 0.03)
- Change BB bluff threshold from ~17% to ~2% (e = 0.02)
- Rationale: John3 almost never bluffs and wins 70%

### Step 1.2: Tighten value betting range

- Change SB value threshold from ~56% to ~75% (c = 0.75)
- Change BB value threshold from ~67% to ~80% (f = 0.80)
- Rationale: John3 only bets with avg card 0.988

### Step 1.3: Fold weak hands as SB

- Add SB fold logic for cards < 0.15
- John3 folds 24% of hands as SB
- This avoids bleeding chips with weak hands

### Step 1.4: Call wider when facing bets

- Lower call threshold from 0.50 to 0.40
- John3 calls 60% when facing raises
- Catches more bluffs from aggressive opponents

### Step 1.5: Test Phase 1

- Run against John3 and all 90 opponents
- Target: 50%+ overall

---

## Phase 2: Opponent-Adaptive Adjustments

### Step 2.1: Track opponent aggression in real-time

- Calculate bet_frequency = bets / total_actions
- Classify: passive (<20%), neutral (20-50%), aggressive (>50%)

### Step 2.2: Exploit passive opponents (like P159)

- When opponent bet_freq < 20%: increase bluff to 10%
- They fold 66% to raises, so bluffing is profitable

### Step 2.3: Exploit aggressive opponents (like P131)

- When opponent bet_freq > 50%: call threshold to 0.35
- They bluff more, so calling wider is profitable
- Reduce our bluffs to 0% (they never fold)

### Step 2.4: Exploit tight-value opponents

- Track avg_bet_card from showdowns
- When avg_bet_card > 0.65: fold to their bets with cards < 0.55
- They only bet with strong hands

### Step 2.5: Test Phase 2

- Run against worst opponents first (P131, P159, P071)
- Then full test against all 90
- Target: 55%+ overall

---

## Phase 3: Advanced Adaptations

### Step 3.1: Dynamic threshold adjustment

- Track win rate over last 30 hands
- If losing: tighten value range by 5%
- If winning: maintain current strategy

### Step 3.2: Showdown-based learning

- Use revealed cards to estimate opponent's betting range
- Adjust call thresholds based on observed bluff frequency

### Step 3.3: Position-aware sizing

- As SB: prefer smaller raises (less risk)
- As BB: pot-sized when betting (more value)

### Step 3.4: Test Phase 3

- Full 500-game test per opponent
- Target: 60%+ overall

---

## Phase 4: Final Validation

### Step 4.1: Debug worst matchups

- Verbose logging against <30% win rate opponents
- Identify specific exploits being used

### Step 4.2: Fine-tune thresholds

- Iterate on exact values based on test results
- A/B test different configurations

### Step 4.3: Final verification

- 1000 games against John3
- 500 games per training opponent
- Document final win rates
