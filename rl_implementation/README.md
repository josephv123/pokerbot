# RL Poker Player Implementation

Complete Deep Q-Network (DQN) implementation for learning optimal poker strategy through reinforcement learning.

## Quick Start

### 1. Install Dependencies

```bash
pip install numpy torch tqdm
```

### 2. Test Components

Verify all components work correctly:

```bash
cd rl_implementation
python3 test_components.py
```

Expected output: `ALL TESTS PASSED! ✓`

### 3. Train Agent

Train the RL agent against opponents:

```bash
python3 train_rl_agent.py
```

**Training Time**:
- Quick test (10 games/opponent × 10 opponents): ~20-30 minutes
- Full training (30 games/opponent × 90 opponents × 2 epochs): ~8-12 hours
- Extended training (100 games/opponent × 90 opponents × 3 epochs): ~20+ hours

**Note**: Training opponents (P001-P179) require compiled .so/.pyd files. If not available, the script will use basic opponents (John1, AllIn) for demonstration.

### 4. Evaluate Agent

Test the trained agent:

```bash
python3 evaluate_rl_agent.py --model checkpoints/final_model.pt --games 200 --detailed
```

Options:
- `--model PATH`: Path to trained model checkpoint
- `--games N`: Number of games per opponent (default: 200)
- `--epsilon E`: Exploration rate (default: 0.0 for greedy)
- `--detailed`: Print per-opponent results

---

## Architecture Overview

### State Space (19 features)

**Hand State (6):**
- `card_strength`: Our card value [0, 1]
- `myscore_norm`: Our score / 200
- `oppscore_norm`: Opponent score / 200
- `pot_norm`: Pot / (total points)
- `minbet_level`: log₂(minbet / initial_minbet)
- `role`: 0=SmallBlind, 1=BigBlind

**Opponent Features (10):**
- `fold_rate`: Opponent folds to our bets
- `call_rate`: Opponent calls our bets
- `raise_rate`: Opponent raises our bets
- `aggression`: Opponent bets when we check
- `bet_card_mean`: Avg card when opponent bets (from showdowns)
- `bet_card_confidence`: Confidence in bet_card_mean
- `allin_frequency`: Opponent all-in rate
- `hands_played_norm`: Game phase indicator
- `recent_fold_rate`: Last 20 decisions
- `drift_magnitude`: Adaptation detection

**Hand Context (3):**
- `first_action`: Whether it's our first action this hand
- `we_checked`: Whether we checked to opponent
- `opp_raised`: Whether opponent raised this hand

### Action Space (7 discrete actions)

0. **FOLD**: Return 0 (forfeit hand)
1. **CALL**: Match pot (pot)
2. **MIN_RAISE**: Pot + minbet
3. **SMALL_RAISE**: Pot + 2×minbet
4. **MED_RAISE**: Pot + 3×minbet
5. **POT_RAISE**: Pot + pot_size
6. **ALLIN**: Bet entire stack

Actions are masked to prevent invalid moves.

### Network Architecture

**Dueling DQN:**
```
Input (19) → Shared (128 → 128) ─┬─→ Value (64 → 1)
                                   └─→ Advantage (64 → 7)
                                         ↓
                            Q(s,a) = V(s) + [A(s,a) - mean(A)]
```

**Parameters**: ~35,000 (very lightweight for CPU training)

### Training Algorithm: Double DQN

1. **Experience Replay**: Store (s, a, r, s', done) transitions
2. **Target Network**: Separate network for stable Q-targets
3. **Double DQN**: Decouple action selection from evaluation
4. **Soft Updates**: θ_target ← τ×θ_online + (1-τ)×θ_target
5. **Epsilon Decay**: Gradual reduction from 1.0 → 0.05

---

## File Structure

```
rl_implementation/
├── config.py                  # Hyperparameters and constants
├── opponent_tracker.py        # Extract opponent behavioral features
├── replay_buffer.py           # Experience replay buffer
├── dqn_agent.py              # DQN network and agent
├── rl_poker_env.py           # Poker environment wrapper
├── utils.py                   # Helper functions
├── train_rl_agent.py         # Main training script
├── evaluate_rl_agent.py      # Evaluation script
├── test_components.py        # Component tests
├── checkpoints/              # Saved models
│   ├── checkpoint_ep1_opp10.pt
│   ├── final_model.pt
│   └── training_stats.json
└── README.md                 # This file
```

---

## Hyperparameter Tuning

Edit `config.py` to adjust training parameters:

### Key Hyperparameters

```python
# Network
HIDDEN_DIM = 128              # Increase for more capacity
LR = 0.0001                   # Learning rate

# Training
BATCH_SIZE = 128              # Larger = more stable
GAMMA = 0.99                  # Discount factor
EPSILON_DECAY = 0.995         # Slower = more exploration

# Experience Replay
BUFFER_SIZE = 100_000         # More transitions = better sampling
TRAIN_FREQ = 4                # Train every N steps
TARGET_UPDATE_FREQ = 1000     # Update target network

# Training Loop
NUM_EPOCHS = 2                # Passes through opponents
GAMES_PER_OPPONENT = 30       # Games per opponent per epoch
```

### Training Strategies

**Fast iteration (debugging):**
```python
GAMES_PER_OPPONENT = 10
NUM_EPOCHS = 1
```

**Balanced (recommended):**
```python
GAMES_PER_OPPONENT = 30
NUM_EPOCHS = 2
```

**Maximum performance:**
```python
GAMES_PER_OPPONENT = 100
NUM_EPOCHS = 3
EPSILON_DECAY = 0.998  # Slower decay
```

---

## Monitoring Training

### Progress Output

Training shows real-time progress:
```
[Ep1] vs          John1: 100%|████████| 30/30 [00:45<00:00] WR: 65.00%, ε: 0.892, buf: 1250
```

- **WR**: Win rate against current opponent
- **ε**: Current exploration rate
- **buf**: Replay buffer size

### Checkpoints

Models are saved every 10 opponents:
- `checkpoints/checkpoint_ep1_opp10.pt`
- `checkpoints/checkpoint_ep1_opp20.pt`
- ...
- `checkpoints/final_model.pt`

### Training Statistics

After training, check `checkpoints/training_stats.json`:
```json
{
  "total_games": 5400,
  "total_wins": 3780,
  "overall_win_rate": 0.70,
  "win_rates_per_opponent": [0.67, 0.83, ...],
  "opponent_names": ["P001", "P003", ...]
}
```

---

## Deployment to PokerPlayer

Once trained, create the final `pokerplayer.py`:

```python
import torch
import numpy as np
from rl_implementation.dqn_agent import DuelingQNetwork
from rl_implementation.opponent_tracker import OpponentTracker
from rl_implementation.utils import normalize_state, get_valid_actions_mask, action_to_bet

class PokerPlayer:
    def __init__(self):
        # Load trained network
        self.network = DuelingQNetwork()
        self.network.load_state_dict(torch.load('rl_implementation/checkpoints/final_model.pt')['q_network'])
        self.network.eval()

        # Opponent tracker
        self.tracker = OpponentTracker()
        self.initial_minbet = 1.0

    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        self.card = card
        self.myscore = myscore
        self.oppscore = oppscore
        self.minbet = minbet
        self.pot = pot
        self.bigblind = bigblind
        self.first_action = True
        self.we_checked = False
        self.opp_raised = False

    def bet(self, card, myscore, oppscore, minbet, pot):
        # Get state
        state = normalize_state(
            card, myscore, oppscore, pot, minbet,
            role=(1 if self.bigblind else 0),
            opponent_features=self.tracker.get_features(),
            first_action=self.first_action,
            we_checked=self.we_checked,
            opp_raised=self.opp_raised,
            initial_minbet=self.initial_minbet
        )

        # Get Q-values
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.network(state_tensor).numpy()[0]

        # Mask invalid actions
        valid_mask = get_valid_actions_mask(
            pot, minbet, myscore, oppscore,
            self.bigblind, (1 if self.bigblind else 0)
        )
        q_values[~valid_mask] = -float('inf')

        # Select action
        action = int(np.argmax(q_values))

        # Convert to bet
        bet = action_to_bet(action, pot, minbet, myscore, oppscore,
                            (1 if self.bigblind else 0))

        self.first_action = False
        if bet == pot:
            self.we_checked = True

        return bet

    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        # Update opponent tracker
        self.tracker.update_hand_end()
```

---

## Troubleshooting

### Issue: "Failed to import training opponents"

**Solution**: This is expected if you don't have the compiled `.so` files for Linux. The code will use basic opponents (John1, AllIn) for testing. To get full training opponents:
1. Ensure you're on Windows (has `.pyd` files) OR
2. Request the Linux `.so` files from the course instructor

### Issue: Training is slow

**Solutions**:
- Reduce `GAMES_PER_OPPONENT` (e.g., 10-20)
- Reduce `NUM_EPOCHS` (e.g., 1)
- Use fewer opponents for quick testing
- The code is CPU-optimized; GPU won't help much for this small network

### Issue: Win rate not improving

**Solutions**:
- Train longer (more games/epochs)
- Increase network capacity (`HIDDEN_DIM = 256`)
- Adjust learning rate (`LR = 0.0005`)
- Check opponent diversity (need varied opponents)
- Review reward function in `utils.py`

### Issue: Agent learns to always fold/all-in

**Solutions**:
- This indicates insufficient exploration or poor reward shaping
- Increase initial epsilon or slow down decay
- Ensure action masking is working correctly
- Check that rewards are properly scaled

---

## Expected Performance

**Target**: ≥70% win rate against 90 training opponents

**Baseline Comparisons**:
- **AllIn** (always all-in): ~30%
- **John1** (simple heuristic): ~59%
- **Current GTO bot**: ~71.6%
- **John3** (reference): ~72%

**RL Agent Goals**:
- Match or exceed current GTO bot (70%+)
- Generalize to unseen test opponents
- Learn opponent adaptation automatically

---

## Advanced Features (Optional)

### Prioritized Experience Replay

Replace `ReplayBuffer` with `PrioritizedReplayBuffer` in `dqn_agent.py`:

```python
from replay_buffer import PrioritizedReplayBuffer
self.buffer = PrioritizedReplayBuffer(buffer_size, alpha=0.6)
```

### Curriculum Learning

Train on easy opponents first, gradually increase difficulty:

```python
# In train_rl_agent.py
easy_opponents = [opp for opp in opponents if opp.difficulty == 'easy']
medium_opponents = [opp for opp in opponents if opp.difficulty == 'medium']
hard_opponents = [opp for opp in opponents if opp.difficulty == 'hard']

train(agent, easy_opponents, epochs=1)
train(agent, medium_opponents, epochs=1)
train(agent, hard_opponents, epochs=2)
```

### Reward Shaping

Adjust in `config.py`:

```python
REWARD_BLUFF_SUCCESS = 0.05     # Bonus for successful bluffs
REWARD_BAD_FOLD_PENALTY = 0.05  # Penalty for folding strong hands
```

---

## Citation

Based on the RL implementation plan in `RL_IMPLEMENTATION_PLAN.md`. Uses Double DQN with Dueling architecture for sample-efficient learning with opponent modeling.
