"""
Analyze opponent behavior to categorize them for adaptive strategy.
Profiles problem opponents by tracking:
- Fold frequency to our bets
- Bet frequency when checked to
- Showdown card ranges
- Response patterns
"""

import sys
import random
from opponents import training_opponents, John3
from randomTexas import RandomNumberTexasHoldem

# Problem opponents identified from testing (win rate < 30%)
PROBLEM_OPPONENTS = [
    'P001', 'P003', 'P011', 'P019', 'P031', 'P043', 'P049', 'P059', 'P065',
    'P089', 'P093', 'P097', 'P101', 'P109', 'P113', 'P117', 'P129', 'P133',
    'P139', 'P145', 'P151', 'P153', 'P173'
]


class AnalysisPlayer:
    """A player that tracks detailed opponent behavior for analysis."""
    
    def __init__(self):
        self.role = None
        self.hand_strength = None
        self.minbet = None
        self.initial_bb_pot = 0
        self.epsilon = 1e-9
        
        # Tracking for analysis
        self.hands_played = 0
        self.our_bet_count = 0
        self.our_bet_gets_fold = 0
        self.our_bet_gets_call = 0
        self.our_bet_gets_raise = 0
        
        self.opp_bet_count = 0
        self.opp_check_count = 0
        self.opp_fold_count = 0
        self.opp_call_count = 0
        
        # Showdown ranges
        self.opp_bet_cards = []
        self.opp_call_cards = []
        self.opp_check_cards = []
        
        # Hand tracking
        self.we_bet_this_hand = False
        self.opp_bet_this_hand = False
        self.opp_raised_this_hand = False
        self.last_action = None
        
    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        self.role = 'BB' if bigblind else 'SB'
        self.hand_strength = card
        self.minbet = minbet
        self.initial_bb_pot = 2 * minbet
        self.we_bet_this_hand = False
        self.opp_bet_this_hand = False
        self.opp_raised_this_hand = False
        self.last_action = None
        
    def bet(self, card, myscore, oppscore, minbet, pot):
        self.hand_strength = card
        max_bet = min(myscore, oppscore)
        
        def pot_equals(p1, p2):
            return abs(p1 - p2) < self.epsilon
        
        if self.role == 'SB':
            return self._bet_as_sb(pot, max_bet, minbet, pot_equals)
        else:
            return self._bet_as_bb(pot, max_bet, minbet, pot_equals)
    
    def _bet_as_sb(self, pot, max_bet, minbet, pot_equals):
        if self.last_action is None:
            # Opening action - use aggressive strategy to probe opponent
            if self.hand_strength < 0.15 or self.hand_strength >= 0.55:
                # Bet with bluffs and value
                bet = min(pot * 5, max_bet)
                bet = int(bet / minbet) * minbet
                bet = max(bet, pot + minbet)
                self.last_action = 'bet'
                self.we_bet_this_hand = True
                return bet
            else:
                # Check
                self.last_action = 'check'
                return self.initial_bb_pot
        else:
            if self.last_action == 'check':
                self.opp_bet_this_hand = True
                # Call with decent hands
                if self.hand_strength >= 0.5:
                    return pot
                else:
                    return 0
            else:
                # We bet, they raised
                self.opp_raised_this_hand = True
                if self.hand_strength >= 0.6:
                    return pot
                else:
                    return 0
    
    def _bet_as_bb(self, pot, max_bet, minbet, pot_equals):
        if pot_equals(pot, self.initial_bb_pot):
            # SB checked, we can bet or check
            if self.hand_strength < 0.15 or self.hand_strength >= 0.55:
                bet = min(pot * 5, max_bet)
                bet = int(bet / minbet) * minbet
                bet = max(bet, pot + minbet)
                self.last_action = 'bet'
                self.we_bet_this_hand = True
                return bet
            else:
                self.last_action = 'check'
                return pot
        else:
            # Facing a raise
            self.opp_bet_this_hand = True
            if self.hand_strength >= 0.5:
                return pot
            else:
                return 0
    
    def end(self, iwon, oppcard, myscore, oppscore, minbet, winnings):
        self.hands_played += 1
        
        if oppcard is None:
            # Someone folded
            if iwon:
                # Opponent folded
                self.opp_fold_count += 1
                if self.we_bet_this_hand:
                    self.our_bet_count += 1
                    self.our_bet_gets_fold += 1
            else:
                # We folded
                if self.opp_bet_this_hand or self.opp_raised_this_hand:
                    self.opp_bet_count += 1
        else:
            # Showdown
            if self.opp_bet_this_hand or self.opp_raised_this_hand:
                self.opp_bet_count += 1
                self.opp_bet_cards.append(oppcard)
                if self.we_bet_this_hand:
                    self.our_bet_count += 1
                    self.our_bet_gets_raise += 1
            elif self.we_bet_this_hand:
                self.opp_call_count += 1
                self.opp_call_cards.append(oppcard)
                self.our_bet_count += 1
                self.our_bet_gets_call += 1
            else:
                self.opp_check_count += 1
                self.opp_check_cards.append(oppcard)
    
    def get_stats(self):
        """Return analysis statistics."""
        stats = {
            'hands_played': self.hands_played,
            'our_bet_count': self.our_bet_count,
            'fold_rate': self.our_bet_gets_fold / max(1, self.our_bet_count),
            'call_rate': self.our_bet_gets_call / max(1, self.our_bet_count),
            'raise_rate': self.our_bet_gets_raise / max(1, self.our_bet_count),
            'opp_bet_count': self.opp_bet_count,
            'opp_check_count': self.opp_check_count,
            'opp_fold_count': self.opp_fold_count,
            'opp_call_count': self.opp_call_count,
        }
        
        # Calculate bet frequency
        total_opp_actions = self.opp_bet_count + self.opp_check_count + self.opp_fold_count + self.opp_call_count
        stats['opp_bet_freq'] = self.opp_bet_count / max(1, total_opp_actions)
        
        # Showdown ranges
        if self.opp_bet_cards:
            stats['opp_bet_avg'] = sum(self.opp_bet_cards) / len(self.opp_bet_cards)
            stats['opp_bet_min'] = min(self.opp_bet_cards)
        else:
            stats['opp_bet_avg'] = None
            stats['opp_bet_min'] = None
            
        if self.opp_call_cards:
            stats['opp_call_avg'] = sum(self.opp_call_cards) / len(self.opp_call_cards)
            stats['opp_call_min'] = min(self.opp_call_cards)
        else:
            stats['opp_call_avg'] = None
            stats['opp_call_min'] = None
            
        if self.opp_check_cards:
            stats['opp_check_avg'] = sum(self.opp_check_cards) / len(self.opp_check_cards)
        else:
            stats['opp_check_avg'] = None
            
        return stats


def analyze_opponent(opp_class, ngames=200, seed=None):
    """Run analysis games against a single opponent."""
    rng = random.Random(seed)
    
    # Aggregate stats from multiple games
    total_stats = {
        'hands_played': 0,
        'our_bet_count': 0,
        'our_bet_gets_fold': 0,
        'our_bet_gets_call': 0,
        'our_bet_gets_raise': 0,
        'opp_bet_count': 0,
        'opp_check_count': 0,
        'opp_fold_count': 0,
        'opp_call_count': 0,
        'opp_bet_cards': [],
        'opp_call_cards': [],
        'opp_check_cards': [],
        'wins': 0,
    }
    
    for i in range(ngames):
        p1 = AnalysisPlayer()
        p2 = opp_class()
        result = RandomNumberTexasHoldem(p1, p2, 100, rng)
        
        if result == 1:
            total_stats['wins'] += 1
        
        # Aggregate
        total_stats['hands_played'] += p1.hands_played
        total_stats['our_bet_count'] += p1.our_bet_count
        total_stats['our_bet_gets_fold'] += p1.our_bet_gets_fold
        total_stats['our_bet_gets_call'] += p1.our_bet_gets_call
        total_stats['our_bet_gets_raise'] += p1.our_bet_gets_raise
        total_stats['opp_bet_count'] += p1.opp_bet_count
        total_stats['opp_check_count'] += p1.opp_check_count
        total_stats['opp_fold_count'] += p1.opp_fold_count
        total_stats['opp_call_count'] += p1.opp_call_count
        total_stats['opp_bet_cards'].extend(p1.opp_bet_cards)
        total_stats['opp_call_cards'].extend(p1.opp_call_cards)
        total_stats['opp_check_cards'].extend(p1.opp_check_cards)
    
    # Calculate final stats
    result = {
        'win_rate': total_stats['wins'] / ngames,
        'hands_per_game': total_stats['hands_played'] / ngames,
        'fold_rate': total_stats['our_bet_gets_fold'] / max(1, total_stats['our_bet_count']),
        'call_rate': total_stats['our_bet_gets_call'] / max(1, total_stats['our_bet_count']),
        'raise_rate': total_stats['our_bet_gets_raise'] / max(1, total_stats['our_bet_count']),
    }
    
    # Opponent action frequencies
    total_actions = (total_stats['opp_bet_count'] + total_stats['opp_check_count'] + 
                    total_stats['opp_fold_count'] + total_stats['opp_call_count'])
    result['opp_bet_freq'] = total_stats['opp_bet_count'] / max(1, total_actions)
    result['opp_check_freq'] = total_stats['opp_check_count'] / max(1, total_actions)
    result['opp_fold_freq'] = total_stats['opp_fold_count'] / max(1, total_actions)
    result['opp_call_freq'] = total_stats['opp_call_count'] / max(1, total_actions)
    
    # Showdown ranges
    if total_stats['opp_bet_cards']:
        result['opp_bet_avg'] = sum(total_stats['opp_bet_cards']) / len(total_stats['opp_bet_cards'])
        result['opp_bet_min'] = min(total_stats['opp_bet_cards'])
    else:
        result['opp_bet_avg'] = None
        result['opp_bet_min'] = None
        
    if total_stats['opp_call_cards']:
        result['opp_call_avg'] = sum(total_stats['opp_call_cards']) / len(total_stats['opp_call_cards'])
        result['opp_call_min'] = min(total_stats['opp_call_cards'])
    else:
        result['opp_call_avg'] = None
        result['opp_call_min'] = None
    
    return result


def categorize_opponent(stats):
    """Categorize opponent based on their behavior patterns."""
    # Classification rules:
    # 1. Folder: fold_rate > 0.50
    # 2. Caller: fold_rate < 0.30 AND call_rate > 0.40
    # 3. Aggressor: raise_rate > 0.30 OR opp_bet_freq > 0.40
    # 4. GTO-like: balanced stats (fold 30-50%, bet 20-40%)
    # 5. Tight: opp_call_avg > 0.55 (only calls with strong hands)
    
    fold_rate = stats['fold_rate']
    call_rate = stats['call_rate']
    raise_rate = stats['raise_rate']
    opp_bet_freq = stats['opp_bet_freq']
    opp_call_avg = stats.get('opp_call_avg')
    
    if fold_rate > 0.55:
        return 'folder'
    elif fold_rate < 0.25 and call_rate > 0.45:
        return 'calling_station'
    elif raise_rate > 0.35 or opp_bet_freq > 0.45:
        return 'aggressor'
    elif opp_call_avg and opp_call_avg > 0.55:
        return 'tight_caller'
    elif 0.30 <= fold_rate <= 0.50 and 0.20 <= opp_bet_freq <= 0.40:
        return 'gto_like'
    else:
        return 'unknown'


def main():
    """Run analysis on all problem opponents."""
    print("=" * 80)
    print("OPPONENT BEHAVIOR ANALYSIS")
    print("=" * 80)
    print()
    
    # Get opponent classes by name
    opp_dict = {opp.__name__: opp for opp in training_opponents}
    opp_dict['John3'] = John3
    
    # Analyze each problem opponent
    results = []
    
    # Also include John3
    opponents_to_analyze = PROBLEM_OPPONENTS + ['John3']
    
    for opp_name in opponents_to_analyze:
        if opp_name not in opp_dict:
            print(f"Warning: {opp_name} not found in training opponents")
            continue
            
        opp_class = opp_dict[opp_name]
        print(f"Analyzing {opp_name}...", end=' ', flush=True)
        
        stats = analyze_opponent(opp_class, ngames=200, seed=42)
        category = categorize_opponent(stats)
        stats['name'] = opp_name
        stats['category'] = category
        results.append(stats)
        
        print(f"Win: {stats['win_rate']*100:.0f}% | "
              f"Fold: {stats['fold_rate']*100:.0f}% | "
              f"Call: {stats['call_rate']*100:.0f}% | "
              f"Raise: {stats['raise_rate']*100:.0f}% | "
              f"Category: {category}")
    
    # Group by category
    print()
    print("=" * 80)
    print("OPPONENTS GROUPED BY CATEGORY")
    print("=" * 80)
    
    categories = {}
    for r in results:
        cat = r['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(r['name'])
    
    for cat, opps in sorted(categories.items()):
        print(f"\n{cat.upper()} ({len(opps)} opponents):")
        print(f"  {', '.join(opps)}")
    
    # Summary statistics by category
    print()
    print("=" * 80)
    print("STRATEGY RECOMMENDATIONS BY CATEGORY")
    print("=" * 80)
    
    print("""
FOLDER (fold_rate > 55%):
  -> Use AGGRESSIVE mode: 4x pot bets, 2.5x bluff frequency
  -> Our current strategy is optimal for these
  
CALLING_STATION (fold_rate < 25%, call_rate > 45%):
  -> Use TIGHT mode: Never bluff, only value bet with strong hands
  -> Bet smaller for thin value extraction
  
AGGRESSOR (raise_rate > 35% or bet_freq > 45%):
  -> Use TRAPPING mode: Check strong hands, let them bet
  -> Call down lighter since they're bluffing more
  
TIGHT_CALLER (only calls with strong hands):
  -> Use BALANCED mode: Reduce bluffs, tighter value range
  -> They won't pay off bluffs anyway
  
GTO_LIKE (balanced frequencies):
  -> Use BALANCED mode: Standard GTO frequencies
  -> Don't try to exploit, just play solid
  
UNKNOWN:
  -> Use BALANCED mode as default
  -> Monitor for patterns during the match
""")
    
    return results


if __name__ == '__main__':
    main()

