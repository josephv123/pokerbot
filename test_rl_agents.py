"""
Test script to evaluate all RL agents (DQN, PPO, CFR, Hybrid) against John3 and the 90 training opponents.

This script:
1. Creates PokerPlayer wrappers for each RL agent type
2. Tests each agent against John3 and all training opponents
3. Reports win rates and summary statistics
"""

from __future__ import annotations

import json
import os
import random
from pathlib import Path
from typing import Optional

import numpy as np
import torch

# Try to import opponents, handling version incompatibility
TRAINING_OPPONENTS_AVAILABLE = False
John3 = None
training_opponents = []

try:
    from opponents import John3, training_opponents
    TRAINING_OPPONENTS_AVAILABLE = True
except (ImportError, SystemExit):
    # SystemExit happens when Python version is incompatible
    print("Warning: Training opponents not available (Python version may be incompatible)")
    print("Will test against basic opponents only")
    try:
        from opponents.basic_players import John1, AllIn
        training_opponents = [John1, AllIn]  # Fallback to basic opponents
    except ImportError:
        pass

from randomTexas import pokerTest

try:
    from rl_training import utils as rl_utils
    from rl_training.cfr_agent import CFRTrainer, bucketize, ACTION_LIST
    from rl_training.dqn_agent import QNetwork
    from rl_training.ppo_agent import ActorCritic
    from rl_training.hybrid_agent import HybridAgent, HybridPolicy, OpponentProfile
except ImportError as e:
    print(f"Warning: Could not import RL modules: {e}")
    rl_utils = None
    CFRTrainer = None
    QNetwork = None
    ActorCritic = None
    HybridAgent = None


# ============================================================================
# Wrapper Classes for RL Agents
# ============================================================================

class DQNPlayer:
    """Wrapper for DQN agent as PokerPlayer."""
    
    def __init__(self, model_path: str = "rl_training/models/dqn.pt"):
        self.model_path = model_path
        self.model: Optional[QNetwork] = None
        self.enabled = False
        
        if QNetwork is not None and rl_utils is not None and os.path.exists(model_path):
            try:
                self.model = QNetwork()
                state_dict = torch.load(model_path, map_location="cpu")
                self.model.load_state_dict(state_dict)
                self.model.eval()
                self.enabled = True
            except Exception as e:
                print(f"Warning: Could not load DQN model from {model_path}: {e}")
        
        self.opp_stats = rl_utils.OpponentStats() if rl_utils else None
        self.current_card = 0.0
        self.is_big_blind = False
        self.bet_round = 0
        self.myscore = 100.0
        self.oppscore = 100.0
        self.last_minbet = 1.0
    
    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        self.is_big_blind = bigblind
        self.current_card = card
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round = 0
    
    def bet(self, card, myscore, oppscore, minbet, pot):
        self.current_card = card
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round += 1
        
        if self.enabled and self.model is not None and rl_utils is not None:
            obs = rl_utils.encode_state(
                card=self.current_card,
                pot=pot,
                myscore=self.myscore,
                oppscore=self.oppscore,
                minbet=self.last_minbet,
                is_big_blind=self.is_big_blind,
                bet_round=self.bet_round,
                opponent_stats=self.opp_stats,
            )
            with torch.no_grad():
                tensor = torch.from_numpy(obs).float().unsqueeze(0)
                logits = self.model(tensor)
                action = int(torch.argmax(logits, dim=1).item())
            return rl_utils.decode_action(
                action,
                pot=pot,
                minbet=minbet,
                myscore=myscore,
                oppscore=oppscore,
            )
        # Fallback: fold if model not available
        return 0
    
    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        if self.opp_stats:
            if oppcard is None and iwon:
                self.opp_stats.update("fold")
            elif oppcard is None and not iwon:
                self.opp_stats.update("raise")
            else:
                self.opp_stats.update("call")
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round = 0


class PPOPlayer:
    """Wrapper for PPO agent as PokerPlayer."""
    
    def __init__(self, model_path: str = "rl_training/models/ppo.pt"):
        self.model_path = model_path
        self.model: Optional[ActorCritic] = None
        self.enabled = False
        
        if ActorCritic is not None and rl_utils is not None and os.path.exists(model_path):
            try:
                self.model = ActorCritic()
                state_dict = torch.load(model_path, map_location="cpu")
                self.model.load_state_dict(state_dict)
                self.model.eval()
                self.enabled = True
            except Exception as e:
                print(f"Warning: Could not load PPO model from {model_path}: {e}")
        
        self.opp_stats = rl_utils.OpponentStats() if rl_utils else None
        self.current_card = 0.0
        self.is_big_blind = False
        self.bet_round = 0
        self.myscore = 100.0
        self.oppscore = 100.0
        self.last_minbet = 1.0
    
    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        self.is_big_blind = bigblind
        self.current_card = card
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round = 0
    
    def bet(self, card, myscore, oppscore, minbet, pot):
        self.current_card = card
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round += 1
        
        if self.enabled and self.model is not None and rl_utils is not None:
            obs = rl_utils.encode_state(
                card=self.current_card,
                pot=pot,
                myscore=self.myscore,
                oppscore=self.oppscore,
                minbet=self.last_minbet,
                is_big_blind=self.is_big_blind,
                bet_round=self.bet_round,
                opponent_stats=self.opp_stats,
            )
            with torch.no_grad():
                tensor = torch.from_numpy(obs).float()
                logits, _ = self.model(tensor)
                dist = torch.distributions.Categorical(logits=logits)
                action = int(torch.argmax(dist.probs).item())
            return rl_utils.decode_action(
                action,
                pot=pot,
                minbet=minbet,
                myscore=myscore,
                oppscore=oppscore,
            )
        # Fallback: fold if model not available
        return 0
    
    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        if self.opp_stats:
            if oppcard is None and iwon:
                self.opp_stats.update("fold")
            elif oppcard is None and not iwon:
                self.opp_stats.update("raise")
            else:
                self.opp_stats.update("call")
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round = 0


class CFRPlayer:
    """Wrapper for CFR agent as PokerPlayer."""
    
    def __init__(self, strategy_path: str = "rl_training/models/cfr_strategy.json"):
        self.strategy_path = strategy_path
        self.strategy: Optional[dict] = None
        self.enabled = False
        
        if CFRTrainer is not None and os.path.exists(strategy_path):
            try:
                with open(strategy_path, 'r') as f:
                    strategy_data = json.load(f)
                self.strategy = strategy_data
                self.enabled = True
            except Exception as e:
                print(f"Warning: Could not load CFR strategy from {strategy_path}: {e}")
        
        self.current_card = 0.0
        self.is_big_blind = False
        self.bet_round = 0
        self.myscore = 100.0
        self.oppscore = 100.0
        self.last_minbet = 1.0
        self.history = ""
    
    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        self.is_big_blind = bigblind
        self.current_card = card
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round = 0
        self.history = ""
    
    def _get_info_set(self, pot: float) -> str:
        """Construct CFR info set string."""
        import math
        bucket = bucketize(self.current_card)
        role = "B" if self.is_big_blind else "O"
        pot_state = int(math.log2(max(pot, 1)))
        return f"{role}|b{bucket}|p{pot_state}|h{self.history}"
    
    def bet(self, card, myscore, oppscore, minbet, pot):
        self.current_card = card
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round += 1
        
        if self.enabled and self.strategy is not None:
            info_set = self._get_info_set(pot)
            if info_set in self.strategy:
                probs = self.strategy[info_set]
                action_idx = np.random.choice(len(ACTION_LIST), p=probs)
            else:
                # Default uniform strategy if info set not found
                action_idx = np.random.choice(len(ACTION_LIST))
            
            action = ACTION_LIST[action_idx]
            
            # Map CFR actions to bet amounts
            max_bet = min(myscore, oppscore)
            if action == "fold":
                return 0
            elif action == "call":
                return pot
            elif action == "raise":
                bet_amount = pot + minbet
                return min(bet_amount, max_bet)
        
        # Fallback: fold if strategy not available
        return 0
    
    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        # Update history based on outcome
        if oppcard is None:
            if iwon:
                self.history += "f"  # opponent folded
            else:
                self.history += "r"  # we folded (opponent raised)
        else:
            self.history += "c"  # call/showdown
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round = 0


class HybridPlayer:
    """Wrapper for Hybrid agent as PokerPlayer.
    
    Note: Hybrid agent requires opponent profiling, so we use a simplified version
    that tracks opponent stats and uses the hybrid policy to adjust thresholds.
    """
    
    def __init__(self, model_path: str = "rl_training/models/hybrid.pt"):
        self.model_path = model_path
        self.model: Optional[HybridPolicy] = None
        self.enabled = False
        
        if HybridAgent is not None and rl_utils is not None and os.path.exists(model_path):
            try:
                from rl_training.hybrid_agent import HybridConfig
                config = HybridConfig()
                self.model = HybridPolicy(config)
                state_dict = torch.load(model_path, map_location="cpu")
                self.model.load_state_dict(state_dict)
                self.model.eval()
                self.enabled = True
            except Exception as e:
                print(f"Warning: Could not load Hybrid model from {model_path}: {e}")
        
        # Fallback to OptimalThresholdPlayer strategy
        self.BLUFF_THRESHOLD = 0.18
        self.FOLD_THRESHOLD = 0.35
        self.VALUE_THRESHOLD = 0.72
        
        self.opp_stats = rl_utils.OpponentStats() if rl_utils else None
        self.current_card = 0.0
        self.is_big_blind = False
        self.bet_round = 0
        self.myscore = 100.0
        self.oppscore = 100.0
        self.last_minbet = 1.0
    
    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        self.is_big_blind = bigblind
        self.current_card = card
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round = 0
    
    def bet(self, card, myscore, oppscore, minbet, pot):
        self.current_card = card
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round += 1
        
        max_bet = min(myscore, oppscore)
        pot_odds = minbet / (pot + minbet) if (pot + minbet) > 0 else 0
        
        # Get multipliers from hybrid model if available
        bluff_mult = 1.0
        value_mult = 1.0
        call_mult = 1.0
        bet_mult = 1.0
        
        if self.enabled and self.model is not None and self.opp_stats is not None:
            try:
                # Create opponent profile from stats
                total = max(self.opp_stats.folds + self.opp_stats.calls + self.opp_stats.raises, 1)
                profile = OpponentProfile(
                    fold_rate=self.opp_stats.folds / total,
                    call_rate=self.opp_stats.calls / total,
                    raise_rate=self.opp_stats.raises / total,
                    aggression=self.opp_stats.raises / max(self.opp_stats.calls, 1),
                    bet_card_mean=0.5,  # Approximate
                )
                
                with torch.no_grad():
                    obs = torch.from_numpy(profile.as_array()).float().unsqueeze(0)
                    mean, _ = self.model.forward(obs)
                    multipliers = mean.squeeze(0).cpu().numpy()
                    
                    # Scale multipliers to ranges
                    from rl_training.hybrid_agent import PARAM_RANGES
                    for idx, (low, high) in enumerate(PARAM_RANGES):
                        mult = multipliers[idx]
                        scaled = (mult + 1) / 2 * (high - low) + low
                        if idx == 0:
                            bluff_mult = scaled
                        elif idx == 1:
                            value_mult = scaled
                        elif idx == 2:
                            call_mult = scaled
                        elif idx == 3:
                            bet_mult = scaled
            except Exception as e:
                pass  # Use defaults if model fails
        
        # Apply multipliers to thresholds
        bluff_thresh = self.BLUFF_THRESHOLD * (2.0 - bluff_mult)  # Higher mult = lower threshold
        fold_thresh = self.FOLD_THRESHOLD * call_mult
        value_thresh = self.VALUE_THRESHOLD * value_mult
        
        # Value betting range
        if card > value_thresh:
            bet_multiplier = 1 + int((card - 0.7) / 0.1) * bet_mult
            bet_size = pot + minbet * bet_multiplier
            return min(bet_size, max_bet)
        
        # Bluffing range
        elif card < bluff_thresh:
            if random.random() < pot_odds * bluff_mult:
                bet_amount = pot + minbet
                return min(bet_amount, max_bet)
            else:
                return 0
        
        # Folding range
        elif card < fold_thresh:
            return 0
        
        # Calling range
        else:
            if card >= pot_odds * call_mult:
                return pot
            else:
                return 0
    
    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        if self.opp_stats:
            if oppcard is None and iwon:
                self.opp_stats.update("fold")
            elif oppcard is None and not iwon:
                self.opp_stats.update("raise")
            else:
                self.opp_stats.update("call")
        self.myscore = myscore
        self.oppscore = oppscore
        self.last_minbet = minbet
        self.bet_round = 0


# ============================================================================
# Testing Functions
# ============================================================================

def test_agent(agent_class, agent_name: str, opponents, ngames: int = 200, verbosity: int = 1):
    """Test an agent against a list of opponents."""
    print(f"\n{'='*60}")
    print(f"Testing {agent_name}")
    print(f"{'='*60}")
    
    results = []
    total_wins = 0
    total_games = 0
    
    for i, opponent in enumerate(opponents):
        try:
            win_rate = pokerTest(agent_class, opponent, ngames, verbosity=0)
            results.append((opponent.__name__, win_rate))
            total_wins += win_rate * ngames
            total_games += ngames
            
            if verbosity >= 1:
                print(f"{opponent.__name__:<20s}: {win_rate*100:5.1f}%")
        except Exception as e:
            print(f"Error testing against {opponent.__name__}: {e}")
            results.append((opponent.__name__, 0.0))
    
    avg_win_rate = total_wins / total_games if total_games > 0 else 0.0
    print(f"\n{agent_name} Average Win Rate: {avg_win_rate*100:.2f}%")
    print(f"Total Games: {total_games}")
    
    return results, avg_win_rate


def main():
    """Main testing function."""
    print("RL Agent Testing Script")
    print("="*60)
    
    # Check which models exist
    models_dir = Path("rl_training/models")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    dqn_path = models_dir / "dqn.pt"
    ppo_path = models_dir / "ppo.pt"
    cfr_path = models_dir / "cfr_strategy.json"
    hybrid_path = models_dir / "hybrid.pt"
    
    print("\nModel Availability:")
    print(f"  DQN:    {dqn_path.exists()}")
    print(f"  PPO:    {ppo_path.exists()}")
    print(f"  CFR:    {cfr_path.exists()}")
    print(f"  Hybrid: {hybrid_path.exists()}")
    
    # Prepare opponents: John3 + all training opponents (if available)
    all_opponents = []
    if John3 is not None:
        all_opponents.append(John3)
    if training_opponents:
        all_opponents.extend(list(training_opponents))
    
    if not all_opponents:
        print("\nERROR: No opponents available for testing!")
        print("Please ensure you have Python 3.11-3.13 and the training opponents module.")
        return
    
    print(f"\nTesting against {len(all_opponents)} opponents")
    if John3 is not None:
        print(f"  - John3 (reference solution)")
    if TRAINING_OPPONENTS_AVAILABLE:
        print(f"  - {len(training_opponents)} training opponents")
    else:
        print(f"  - {len(training_opponents)} basic opponents (training opponents not available)")
    
    # Test each agent
    all_results = {}
    ngames = 200
    
    # Test DQN
    if dqn_path.exists():
        results, avg = test_agent(DQNPlayer, "DQN", all_opponents, ngames=ngames)
        all_results["DQN"] = {"results": results, "avg_win_rate": avg}
    else:
        print("\nDQN model not found. Skipping DQN tests.")
        all_results["DQN"] = {"results": [], "avg_win_rate": 0.0, "status": "model_not_found"}
    
    # Test PPO
    if ppo_path.exists():
        results, avg = test_agent(PPOPlayer, "PPO", all_opponents, ngames=ngames)
        all_results["PPO"] = {"results": results, "avg_win_rate": avg}
    else:
        print("\nPPO model not found. Skipping PPO tests.")
        all_results["PPO"] = {"results": [], "avg_win_rate": 0.0, "status": "model_not_found"}
    
    # Test CFR
    if cfr_path.exists():
        results, avg = test_agent(CFRPlayer, "CFR", all_opponents, ngames=ngames)
        all_results["CFR"] = {"results": results, "avg_win_rate": avg}
    else:
        print("\nCFR strategy not found. Skipping CFR tests.")
        all_results["CFR"] = {"results": [], "avg_win_rate": 0.0, "status": "model_not_found"}
    
    # Test Hybrid
    if hybrid_path.exists():
        results, avg = test_agent(HybridPlayer, "Hybrid", all_opponents, ngames=ngames)
        all_results["Hybrid"] = {"results": results, "avg_win_rate": avg}
    else:
        print("\nHybrid model not found. Skipping Hybrid tests.")
        all_results["Hybrid"] = {"results": [], "avg_win_rate": 0.0, "status": "model_not_found"}
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for agent_name, data in all_results.items():
        if "status" in data:
            print(f"{agent_name:<10s}: {data['status']}")
        else:
            print(f"{agent_name:<10s}: {data['avg_win_rate']*100:5.2f}% average win rate")
    
    # Save results to file
    output_file = "rl_agent_test_results.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nDetailed results saved to {output_file}")


if __name__ == "__main__":
    main()

