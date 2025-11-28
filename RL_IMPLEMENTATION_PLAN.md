# Reinforcement Learning Poker Player - Implementation Plan

## Executive Summary

Build a Deep Q-Network (DQN) agent that learns optimal poker strategy through self-play against 90 diverse training opponents. The agent will learn opponent modeling features to generalize to unseen opponents.

**Target Performance**: ≥70% win rate against training set, with generalization to test set
**Training Time**: 5-10 hours on laptop CPU
**Key Innovation**: Opponent-conditioned Q-learning with online feature extraction

---

## 1. Algorithm Choice: Double DQN with Dueling Architecture

### Why DQN?
- **Sample Efficiency**: Experience replay allows learning from past experiences multiple times
- **Stability**: Target network prevents moving target problem
- **Proven**: Works well for discrete action spaces
- **CPU-Friendly**: Smaller networks than policy gradient methods

### Enhancements:
- **Double DQN**: Reduces Q-value overestimation by decoupling action selection from evaluation
- **Dueling Architecture**: Separates state value V(s) from action advantages A(s,a), helpful when many actions have similar value
- **Prioritized Experience Replay** (optional): Sample important transitions more frequently

---

## 2. State Representation (18-20 Features)

### A. Hand State (6 features)
```python
- card_strength: float [0, 1]           # My card value
- myscore_norm: float [0, 1]            # myscore / 200
- oppscore_norm: float [0, 1]           # oppscore / 200
- pot_norm: float [0, ~5]               # pot / (myscore + oppscore)
- minbet_level: float [0, ~10]          # log2(minbet / initial_minbet)
- role: binary {0, 1}                   # 0=SB, 1=BB
```

### B. Opponent Features (10 features)
Computed online during gameplay, updated after each hand:
```python
- fold_rate: float [0, 1]               # Opponent folds to our bets
- call_rate: float [0, 1]               # Opponent calls our bets
- raise_rate: float [0, 1]              # Opponent raises our bets
- aggression: float [0, 1]              # Opponent bets when we check
- bet_card_mean: float [0, 1]           # Avg card when opponent bets (from showdowns)
- bet_card_confidence: float [0, 1]     # min(showdown_count / 10, 1)
- allin_frequency: float [0, 1]         # Opponent all-in rate
- hands_played_norm: float [0, 1]       # hands_played / 200 (game phase)
- recent_fold_rate: float [0, 1]        # Last 20 decisions (adaptation detection)
- drift_magnitude: float [0, 1]         # |recent_fold_rate - early_fold_rate|
```

### C. Hand Context (3 features)
```python
- first_action: binary {0, 1}           # 1 if we haven't acted yet this hand
- we_checked: binary {0, 1}             # 1 if we checked to opponent
- opp_raised: binary {0, 1}             # 1 if opponent raised this hand
```

**Total Input Dimension**: 19 features

### Key Design Decisions:
1. **Normalize all features** to [0, 1] or [-1, 1] for stable neural network training
2. **Include opponent features** to enable opponent modeling and generalization
3. **Track adaptation** (drift) to handle opponents who change strategy mid-game
4. **Game phase** (hands_played) helps agent learn time-dependent strategies

---

## 3. Action Space (7 Discrete Actions)

```python
0. FOLD        → return 0
1. CALL        → return pot
2. MIN_RAISE   → return pot + minbet
3. SMALL_RAISE → return pot + 2*minbet
4. MED_RAISE   → return pot + 3*minbet
5. POT_RAISE   → return pot + pot_size
6. ALLIN       → return min(myscore, oppscore)
```

### Action Masking:
- Mask invalid actions (e.g., can't fold if pot == initial_pot and we're SB)
- Set Q-values of invalid actions to -inf
- Select argmax over valid actions only

### Why This Action Space?
- **Discrete**: Easier to learn than continuous betting
- **Expressive**: Covers key betting strategies (min-raise, pot-sized, all-in)
- **Simple**: 7 actions is manageable for Q-learning
- **GTO-Inspired**: Includes both small (bluff) and large (value) bets

---

## 4. Network Architecture

### Dueling DQN Architecture:
```
Input (19 features)
    ↓
Shared: Dense(128, ReLU) → Dense(128, ReLU)
    ↓
    ├─→ Value Stream: Dense(64, ReLU) → Dense(1)          [V(s)]
    └─→ Advantage Stream: Dense(64, ReLU) → Dense(7)      [A(s,a)]
                            ↓
                Q(s,a) = V(s) + (A(s,a) - mean(A(s,a)))
```

### Architecture Details:
- **Parameters**: ~35K (very lightweight for CPU training)
- **Activation**: ReLU for hidden layers
- **Output**: Linear (Q-values can be negative)
- **Initialization**: He initialization for ReLU layers

### Why Dueling?
- Learns which states are valuable independent of actions
- Helpful when action choice doesn't matter much (e.g., strong hand vs weak opponent)
- Improves learning efficiency

---

## 5. Training Strategy

### A. Hyperparameters
```python
BUFFER_SIZE = 100_000           # Experience replay buffer
BATCH_SIZE = 128                # Training batch size
GAMMA = 0.99                    # Discount factor
LR = 0.0001                     # Learning rate
TAU = 0.001                     # Soft target network update
EPSILON_START = 1.0             # Initial exploration
EPSILON_END = 0.05              # Final exploration
EPSILON_DECAY = 0.995           # Decay per episode
TARGET_UPDATE_FREQ = 1000       # Steps between target network updates
TRAIN_FREQ = 4                  # Train every N steps
```

### B. Training Loop
```
For each training epoch (1-3 epochs):
    For each opponent in training_opponents (90 opponents):
        For each game (20-50 games per opponent):
            Reset opponent features
            While game not over:
                Observe state s
                Select action a (ε-greedy)
                Execute action, observe reward r, next state s'
                Store (s, a, r, s', done) in replay buffer
                Update opponent features

                If len(buffer) > BATCH_SIZE and step % TRAIN_FREQ == 0:
                    Sample batch from buffer
                    Compute Double DQN loss
                    Backprop and update network

                If step % TARGET_UPDATE_FREQ == 0:
                    Update target network (soft update)

            Decay epsilon
            Log win rate, avg reward
```

### C. Curriculum Learning (Optional)
Train in 3 phases with increasing difficulty:
1. **Phase 1**: Easy folders (opponents we beat >65%)
2. **Phase 2**: Medium opponents (50-65% win rate)
3. **Phase 3**: Hard opponents (P113, P117, P173, <50% win rate)

Start with easy opponents to learn basics, gradually increase difficulty.

---

## 6. Reward Shaping

### Primary Reward (Terminal)
```python
if iwon:
    reward = +1.0 * (winnings / (myscore + oppscore))  # Scale by pot size
else:
    reward = -1.0 * (winnings / (myscore + oppscore))
```

### Intermediate Rewards (Optional, tune carefully)
```python
# Small reward for making opponent fold with bluff
if opp_folded and my_card < 0.5:
    reward += 0.05

# Small penalty for folding too easily
if i_folded and my_card > 0.7:
    reward -= 0.05
```

### Why This Reward Structure?
- **Sparse terminal reward** is primary signal (win/loss)
- **Scaled by pot size** to reflect magnitude of win/loss
- **Minimal intermediate rewards** to avoid shaping bias
- Agent learns from cumulative game reward, not just final result

---

## 7. Opponent Modeling Strategy

### Online Feature Extraction
During each game, maintain running statistics:
```python
class OpponentTracker:
    def __init__(self):
        self.our_bet_count = 0
        self.our_bet_gets_fold = 0
        self.our_bet_gets_call = 0
        self.our_bet_gets_raise = 0
        self.we_checked_count = 0
        self.opp_bet_when_checked = 0
        self.opp_bet_card_sum = 0.0
        self.opp_bet_card_count = 0
        self.hands_played = 0
        self.recent_folds = deque(maxlen=20)
        self.early_fold_rate = None

    def update(self, hand_result):
        # Update after each hand
        # Compute fold_rate, aggression, bet_card_mean, etc.

    def get_features(self):
        # Return 10-dim opponent feature vector
```

### Generalization Mechanism
- Network sees opponent features as part of state
- Learns to map feature patterns → optimal actions
- New opponents will have features similar to training opponents
- **Key insight**: We're not learning 90 separate policies, we're learning a single policy conditioned on opponent features

### Why This Works:
- Current GTO-based bot achieves 71.6% by classifying into 5-6 archetypes
- RL agent learns continuous interpolation over opponent feature space
- Can handle novel opponents if their features fall within training distribution

---

## 8. Implementation Plan

### Phase 1: Core Infrastructure (Day 1, ~4 hours)
**Files to create:**
1. `rl_poker_env.py`: Poker environment wrapper
   - `PokerEnv` class implementing gym-like interface
   - `reset()`, `step(action)`, `_get_state()`, `_compute_reward()`
   - Wrapper around `RandomNumberTexasHoldem`

2. `opponent_tracker.py`: Online opponent feature extraction
   - `OpponentTracker` class with `update()` and `get_features()`
   - Implements same statistics as current PokerPlayer

3. `dqn_agent.py`: DQN agent implementation
   - `DuelingQNetwork(nn.Module)`: Neural network definition
   - `ReplayBuffer`: Experience replay with uniform sampling
   - `DQNAgent`: Agent with `act()`, `step()`, `learn()` methods

4. `utils.py`: Helper functions
   - Action masking, state normalization, logging

**Tests:**
- Verify environment can run a complete game
- Verify opponent features match current implementation
- Verify network forward pass and backprop

### Phase 2: Training Pipeline (Day 2, ~4 hours)
**Files to create:**
5. `train_rl_agent.py`: Main training script
   - Load all 90 training opponents
   - Training loop with logging
   - Checkpoint saving every N episodes
   - Tensorboard/wandb logging (optional)

6. `config.py`: Hyperparameter configuration
   - All hyperparameters in one place
   - Easy to experiment with different settings

**Training:**
- Initial training run: 10-20 games per opponent (quick test)
- Monitor: win rate, average reward, epsilon, loss
- Debug: Check if agent is learning, verify rewards make sense

### Phase 3: Hyperparameter Tuning (Day 2-3, ~6 hours)
**Experiments:**
- Tune learning rate, batch size, epsilon decay
- Try different reward shaping
- Test with/without curriculum learning
- Add prioritized experience replay if needed

**Evaluation:**
- Run `evaluate_rl_agent.py` after training
- Test against all 90 opponents (200 games each)
- Target: ≥70% win rate
- Check for overfitting: variance across opponents

### Phase 4: Integration (Day 3, ~2 hours)
**Files to create:**
7. `rl_pokerplayer.py`: Final PokerPlayer implementation
   - Load trained model weights in `__init__()`
   - Implement inference-only `bet()` method
   - Maintain opponent tracking for feature extraction
   - No training, just forward pass

**Deliverable:**
- Copy `rl_pokerplayer.py` → `Assignment3_Class/pokerplayer.py`
- Package model weights (save as `.pt` file, ~140KB)
- Ensure no external dependencies beyond numpy, torch (or just numpy if we export to numpy weights)

---

## 9. Technical Implementation Details

### A. Environment Wrapper (`rl_poker_env.py`)
```python
class PokerEnv:
    def __init__(self, opponent_class, rng_seed=None):
        self.opponent = opponent_class()
        self.our_player = AgentPlayer()  # Placeholder
        self.tracker = OpponentTracker()
        self.game = None

    def reset(self):
        """Start new game, return initial state"""
        self.tracker.reset()
        self.game = RandomNumberTexasHoldem(
            self.our_player, self.opponent, 100, rng_seed
        )
        # Play until it's our turn
        state = self._get_state()
        return state

    def step(self, action):
        """Execute action, return (next_state, reward, done, info)"""
        # Convert action index to bet amount
        bet = self._action_to_bet(action)
        # Execute in game engine
        # Get reward, next state
        # Update opponent tracker
        return next_state, reward, done, info
```

### B. DQN Agent (`dqn_agent.py`)
```python
class DuelingQNetwork(nn.Module):
    def __init__(self, state_dim=19, action_dim=7):
        super().__init__()
        self.feature = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU()
        )
        self.value_stream = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        self.advantage_stream = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )

    def forward(self, state):
        features = self.feature(state)
        value = self.value_stream(features)
        advantages = self.advantage_stream(features)
        # Dueling aggregation
        q_values = value + (advantages - advantages.mean(dim=1, keepdim=True))
        return q_values

class DQNAgent:
    def __init__(self, state_dim, action_dim, lr=0.0001):
        self.q_network = DuelingQNetwork(state_dim, action_dim)
        self.target_network = DuelingQNetwork(state_dim, action_dim)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.optimizer = torch.optim.Adam(self.q_network.parameters(), lr=lr)
        self.buffer = ReplayBuffer(100000)
        self.epsilon = 1.0

    def act(self, state, valid_actions, epsilon=None):
        """Epsilon-greedy action selection with action masking"""
        if epsilon is None:
            epsilon = self.epsilon

        if random.random() < epsilon:
            return random.choice(valid_actions)
        else:
            with torch.no_grad():
                q_values = self.q_network(state)
                # Mask invalid actions
                q_values[~valid_actions] = -float('inf')
                return q_values.argmax().item()

    def learn(self, batch_size=128):
        """Sample batch and update Q-network using Double DQN"""
        if len(self.buffer) < batch_size:
            return

        states, actions, rewards, next_states, dones = self.buffer.sample(batch_size)

        # Current Q values
        q_values = self.q_network(states).gather(1, actions)

        # Double DQN: use online network to select action, target network to evaluate
        with torch.no_grad():
            next_actions = self.q_network(next_states).argmax(1, keepdim=True)
            next_q_values = self.target_network(next_states).gather(1, next_actions)
            target_q_values = rewards + (1 - dones) * GAMMA * next_q_values

        # Huber loss (less sensitive to outliers than MSE)
        loss = F.smooth_l1_loss(q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), 10)
        self.optimizer.step()

        return loss.item()

    def update_target_network(self, tau=0.001):
        """Soft update: target = tau * online + (1-tau) * target"""
        for target_param, param in zip(
            self.target_network.parameters(),
            self.q_network.parameters()
        ):
            target_param.data.copy_(tau * param.data + (1-tau) * target_param.data)
```

### C. Training Script (`train_rl_agent.py`)
```python
def train(agent, opponents, num_epochs=2, games_per_opponent=30):
    total_steps = 0
    win_rates = []

    for epoch in range(num_epochs):
        print(f"\n=== Epoch {epoch+1}/{num_epochs} ===")

        for opp_idx, opponent_class in enumerate(opponents):
            wins = 0

            for game_num in range(games_per_opponent):
                env = PokerEnv(opponent_class, rng_seed=None)
                state = env.reset()
                done = False

                while not done:
                    # Get valid actions
                    valid_actions = env.get_valid_actions()

                    # Select action
                    action = agent.act(state, valid_actions, agent.epsilon)

                    # Step
                    next_state, reward, done, info = env.step(action)

                    # Store transition
                    agent.buffer.push(state, action, reward, next_state, done)

                    # Train
                    if total_steps % 4 == 0:  # Train every 4 steps
                        loss = agent.learn(batch_size=128)

                    # Update target network
                    if total_steps % 1000 == 0:
                        agent.update_target_network(tau=0.001)

                    state = next_state
                    total_steps += 1

                # Track win
                if info['won']:
                    wins += 1

                # Decay epsilon
                agent.epsilon = max(EPSILON_END, agent.epsilon * EPSILON_DECAY)

            # Log win rate vs this opponent
            win_rate = wins / games_per_opponent
            win_rates.append(win_rate)
            print(f"Opponent {opp_idx+1}/90: {win_rate:.1%} wins, ε={agent.epsilon:.3f}")

            # Save checkpoint every 10 opponents
            if (opp_idx + 1) % 10 == 0:
                torch.save(agent.q_network.state_dict(), f'checkpoint_ep{epoch}_opp{opp_idx+1}.pt')

    return agent, win_rates
```

---

## 10. Expected Training Timeline

### Quick Test (2-3 hours)
- 10 games per opponent × 90 opponents = 900 games
- ~150 hands per game = 135K hands
- ~5K training steps
- **Purpose**: Verify everything works, get baseline

### Full Training (8-12 hours)
- 30-50 games per opponent × 90 opponents × 2 epochs = 5400-9000 games
- ~1.35M hands
- ~50K training steps
- **Expected Result**: 68-72% win rate

### Extended Training (if needed, 20+ hours)
- 100 games per opponent × 90 opponents × 3 epochs = 27K games
- May overfit, monitor test performance

---

## 11. Generalization Strategy (Avoiding Overfitting)

### Techniques:
1. **Opponent feature conditioning**: Network learns general opponent → strategy mapping
2. **Regularization**: L2 weight decay (weight_decay=0.0001)
3. **Dropout**: 0.1-0.2 dropout in network (optional)
4. **Early stopping**: Monitor win rate variance, stop if increasing
5. **Data augmentation**: Vary RNG seeds, slight noise in opponent features
6. **Ensemble**: Train 3-5 networks, average Q-values at inference

### Validation:
- Hold out 10-15 training opponents as validation set
- Monitor validation win rate during training
- Stop if validation performance degrades

---

## 12. Deployment (Final PokerPlayer)

### Option A: PyTorch (if allowed)
```python
# pokerplayer.py
import torch
from opponent_tracker import OpponentTracker
from dqn_agent import DuelingQNetwork

class PokerPlayer:
    def __init__(self):
        self.network = DuelingQNetwork(state_dim=19, action_dim=7)
        self.network.load_state_dict(torch.load('trained_model.pt'))
        self.network.eval()
        self.tracker = OpponentTracker()

    def bet(self, card, myscore, oppscore, minbet, pot):
        state = self._get_state(card, myscore, oppscore, minbet, pot)
        state_tensor = torch.FloatTensor(state).unsqueeze(0)

        with torch.no_grad():
            q_values = self.network(state_tensor)

        valid_actions = self._get_valid_actions(pot, minbet, myscore, oppscore)
        q_values[~valid_actions] = -float('inf')
        action = q_values.argmax().item()

        return self._action_to_bet(action, pot, minbet, myscore, oppscore)
```

### Option B: Export to Numpy (if torch not allowed)
- Export network weights to numpy arrays
- Implement forward pass in pure numpy
- ~50 lines of numpy code for inference

---

## 13. Fallback Plan (if RL struggles)

If after 10-15 hours RL doesn't reach 70%:

### Hybrid Approach:
- Use RL for action selection
- Use current GTO thresholds as a prior
- Combine: `action = argmax(0.7 * Q_RL + 0.3 * Q_GTO)`

### Imitation Learning:
- Pre-train RL agent by imitating current GTO bot
- Then fine-tune with RL
- Faster convergence, higher final performance

---

## 14. Success Metrics

### During Training:
- [ ] Win rate increasing over time
- [ ] Loss decreasing and stabilizing
- [ ] Epsilon decaying smoothly
- [ ] Agent uses diverse actions (not always fold/all-in)

### Final Evaluation:
- [ ] ≥70% win rate against training opponents (200 games each)
- [ ] Win rate variance <20% (no catastrophic failures)
- [ ] Reasonable win rate against hard opponents (P113, P117, P173) - aim for 40%+
- [ ] Training time <12 hours on laptop CPU
- [ ] Model size <10MB

---

## 15. Dependencies

```
torch>=2.0.0
numpy>=1.24.0
tqdm>=4.65.0
matplotlib>=3.7.0 (for plotting)
```

Optional:
```
tensorboard>=2.13.0 (logging)
wandb>=0.15.0 (experiment tracking)
```

---

## 16. File Structure

```
pokerbot/
├── Assignment3_Class/
│   ├── pokerplayer.py          # Final RL agent (to submit)
│   └── trained_model.pt         # Trained weights
├── rl_implementation/
│   ├── config.py                # Hyperparameters
│   ├── rl_poker_env.py          # Environment wrapper
│   ├── opponent_tracker.py      # Opponent feature extraction
│   ├── dqn_agent.py             # DQN agent + network
│   ├── replay_buffer.py         # Experience replay
│   ├── train_rl_agent.py        # Training script
│   ├── evaluate_rl_agent.py     # Evaluation script
│   ├── utils.py                 # Helper functions
│   └── checkpoints/             # Saved models
│       ├── checkpoint_ep1_opp30.pt
│       └── final_model.pt
└── RL_IMPLEMENTATION_PLAN.md    # This document
```

---

## 17. Key Insights from Current Implementation (to preserve)

From the current 71.6% bot, we know:
1. **Opponent fold rate** is the #1 signal (70% of opponents are folders)
2. **Aggression** (betting when checked to) identifies dangerous opponents
3. **Bet-card-mean** from showdowns is reliable for calibrating call thresholds
4. **Adaptation detection** matters for ~10% of opponents who change strategy
5. **GTO thresholds** provide a strong baseline
6. **Strategy modes** work: aggressive vs folders, tight vs callers, trapping vs aggressors

The RL agent should learn these patterns automatically from the opponent features.

---

## 18. Why This Will Work

1. **Small, tractable problem**: 19-dim state, 7 actions, deterministic transitions (given cards)
2. **Clear reward signal**: Win/loss at game end
3. **Sample efficiency**: Experience replay + target network
4. **Opponent modeling**: Features enable generalization
5. **Proven approach**: DQN has solved similar problems (Atari, board games)
6. **Fast training**: Small network, CPU-friendly
7. **Leverages domain knowledge**: Opponent features inspired by successful GTO bot

---

## Next Steps

1. ✅ Complete implementation plan
2. → Implement core infrastructure (Phase 1)
3. → Run initial training experiment
4. → Evaluate and iterate
5. → Deploy final model

---

**Estimated Total Time**: 15-20 hours (10 hours implementation + 8 hours training + 2 hours tuning)
**Expected Final Performance**: 70-73% win rate (matching or exceeding current GTO bot)
**Risk**: Low - if RL struggles, can hybrid with current GTO approach
