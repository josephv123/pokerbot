# Poker Bot Improvement Plan v3: 66.7% Win Rate

## Current Result: 66.7% Win Rate (Target: 70%+)

## Phase 3: Adaptive Strategy with Opponent Detection

### Key Improvement: 3-Mode Strategy System

Added opponent detection that classifies opponents based on their response to our bets:

| Mode | Trigger | Bet Size | Bluff Freq | Target Opponents |
|------|---------|----------|------------|------------------|
| **Aggressive** | fold_rate > 55% | 4x pot | 2.5x GTO | Folders |
| **Balanced** | 30-55% fold rate | 3x pot | 1.5x GTO | GTO-like |
| **Tight** | fold_rate < 30% | 2x pot | 0.3x GTO | Calling stations |
| **Trapping** | raise_rate > 30% | 2x pot | 0.5x GTO | Aggressors |

### Opponent Classification Analysis

Created `analyze_opponents.py` to profile problem opponents:

**Categories Identified:**
- **FOLDER (11 opponents)**: P003, P019, P043, P065, P117, P129, P139, P145, P151, P173, John3
- **TIGHT_CALLER (10 opponents)**: P001, P011, P031, P049, P059, P089, P093, P097, P101, P113
- **AGGRESSOR (2 opponents)**: P133, P153
- **GTO_LIKE (1 opponent)**: P109

### Win Rate Improvements

Key opponents where detection helped:

| Opponent | Before (62%) | After (66.7%) | Change |
|----------|--------------|---------------|--------|
| P011 | 6% | 38% | +32% |
| P031 | 8% | 65% | +57% |
| P089 | 8% | 69% | +61% |
| P059 | 21% | 74% | +53% |
| P093 | 30% | 52% | +22% |
| P101 | 9% | 50% | +41% |
| John3 | 16% | 24% | +8% |

### Remaining Problem Opponents (<30% win rate)

Still struggling against:
- P113: 17%, P117: 7%, P173: 16%
- P097: 23%, P145: 28%, P151: 28%

These opponents appear to have sophisticated counter-strategies.

## Configuration Details

### Detection Thresholds
```python
early_detection_threshold = 15  # Minimum bets to classify
folder_threshold = 0.55         # >55% fold rate = folder
caller_threshold = 0.30         # <30% fold rate = caller
aggressor_raise_threshold = 0.30  # >30% raise rate = aggressor
```

### Strategy Parameters by Mode
```python
# Aggressive (default for folders)
{'bet_mult': 5, 'bluff_mult': 2.5, 'value_mult': 1.10, 'call_mult': 1.15}

# Tight (for calling stations)
{'bet_mult': 2, 'bluff_mult': 0.3, 'value_mult': 1.0, 'call_mult': 1.0}

# Trapping (for aggressors)
{'bet_mult': 2, 'bluff_mult': 0.5, 'value_mult': 1.15, 'call_mult': 0.85}

# Balanced (for GTO-like/unknown)
{'bet_mult': 3, 'bluff_mult': 1.5, 'value_mult': 1.05, 'call_mult': 1.05}
```

## What Worked

1. **Early opponent detection**: Classifying opponents within 15 bet responses
2. **Mode-specific strategies**: Different bet sizes and bluff frequencies per type
3. **Tight mode for callers**: Drastically reduced bluffing against calling stations
4. **Trapping mode for aggressors**: Smaller bets, let them bet, call wider

## What Didn't Work

1. **Very aggressive bluffing (3x+)**: Hurt performance even against folders
2. **Zero bluffing in tight mode**: Slightly worse than 0.3x bluffing
3. **Fast detection (10 hands)**: Too noisy, mis-classified opponents
4. **Extreme value thresholds (1.25x)**: Too tight, missed value

## Next Steps to Reach 70%

1. Fine-tune detection thresholds for remaining problem opponents
2. Add more sophisticated opponent modeling (Bayesian updates)
3. Consider per-opponent learned adjustments
4. Investigate check-raise strategies against specific opponent types

## Files Modified

- `pokerplayer.py`: Added 3-mode strategy system with opponent detection
- `analyze_opponents.py`: New debug script for opponent profiling
