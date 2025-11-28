"""
Configuration file for RL Poker Player
Contains all hyperparameters and constants
"""

# ============================================================================
# Network Architecture
# ============================================================================
STATE_DIM = 19          # Input dimension (hand state + opponent features + context)
ACTION_DIM = 7          # Number of discrete actions
HIDDEN_DIM = 128        # Hidden layer size for shared feature extraction
VALUE_HIDDEN = 64       # Hidden layer size for value stream
ADVANTAGE_HIDDEN = 64   # Hidden layer size for advantage stream

# ============================================================================
# Training Hyperparameters
# ============================================================================
BUFFER_SIZE = 100_000   # Experience replay buffer size
BATCH_SIZE = 128        # Training batch size
GAMMA = 0.99            # Discount factor for future rewards
LR = 0.0001             # Learning rate
WEIGHT_DECAY = 0.0001   # L2 regularization
TAU = 0.001             # Soft target network update rate

# Exploration
EPSILON_START = 1.0     # Initial exploration rate
EPSILON_END = 0.05      # Final exploration rate
EPSILON_DECAY = 0.995   # Decay rate per episode

# Update frequencies
TARGET_UPDATE_FREQ = 1000   # Steps between target network updates
TRAIN_FREQ = 4              # Train every N steps

# ============================================================================
# Training Loop
# ============================================================================
NUM_EPOCHS = 2              # Number of passes through all opponents
GAMES_PER_OPPONENT = 30     # Games to play against each opponent per epoch
QUICK_TEST_GAMES = 10       # For quick testing

# Checkpointing
CHECKPOINT_EVERY_N_OPPONENTS = 10  # Save checkpoint every N opponents
SAVE_DIR = 'rl_implementation/checkpoints'

# ============================================================================
# Environment Settings
# ============================================================================
INITIAL_POINTS = 100    # Starting points for each player
TOTAL_POINTS = 200      # Game ends when one player has this many points

# ============================================================================
# Action Space Definition
# ============================================================================
# Actions are indices 0-6
ACTION_FOLD = 0
ACTION_CALL = 1
ACTION_MIN_RAISE = 2
ACTION_SMALL_RAISE = 3
ACTION_MED_RAISE = 4
ACTION_POT_RAISE = 5
ACTION_ALLIN = 6

ACTION_NAMES = [
    'FOLD',
    'CALL',
    'MIN_RAISE',
    'SMALL_RAISE',
    'MED_RAISE',
    'POT_RAISE',
    'ALLIN'
]

# ============================================================================
# Reward Shaping
# ============================================================================
# Terminal rewards (scaled by pot size)
REWARD_WIN_SCALE = 1.0
REWARD_LOSS_SCALE = 1.0

# Optional intermediate rewards (set to 0 to disable)
REWARD_BLUFF_SUCCESS = 0.0     # Bonus for making opponent fold with bad card
REWARD_BAD_FOLD_PENALTY = 0.0  # Penalty for folding with strong card

# ============================================================================
# Evaluation Settings
# ============================================================================
EVAL_GAMES_PER_OPPONENT = 200   # Games for final evaluation
EVAL_EPSILON = 0.0               # No exploration during evaluation

# ============================================================================
# Logging
# ============================================================================
LOG_EVERY_N_GAMES = 10          # Log progress every N games
VERBOSE = True                   # Print training progress
