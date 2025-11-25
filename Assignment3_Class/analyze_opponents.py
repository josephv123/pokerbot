"""
Analyze opponent behavior to categorize them for adaptive strategy.
Enhanced version: Extracts 5-dimensional feature vectors and performs k-means clustering
to derive archetype centroids for the poker bot.

Features extracted:
1. fold_rate: How often opponent folds to our bets
2. call_rate: How often opponent calls our bets
3. raise_rate: How often opponent raises our bets  
4. bet_card_mean: Average card strength when opponent bets (showdown data)
5. aggression: How often opponent bets when checked to
"""

import sys
import random
import math
from opponents import training_opponents, John3
from randomTexas import RandomNumberTexasHoldem


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
        
        # NEW: Track when we check to opponent
        self.we_checked_to_opp = 0  # Times we checked to opponent
        self.opp_bet_when_checked = 0  # Times opponent bet when we checked
        
        # Hand tracking
        self.we_bet_this_hand = False
        self.we_checked_this_hand = False
        self.opp_bet_this_hand = False
        self.opp_raised_this_hand = False
        self.last_action = None
        
    def start(self, bigblind, card, myscore, oppscore, minbet, pot):
        self.role = 'BB' if bigblind else 'SB'
        self.hand_strength = card
        self.minbet = minbet
        self.initial_bb_pot = 2 * minbet
        self.we_bet_this_hand = False
        self.we_checked_this_hand = False
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
                self.we_checked_this_hand = True
                self.we_checked_to_opp += 1
                return self.initial_bb_pot
        else:
            if self.last_action == 'check':
                self.opp_bet_this_hand = True
                self.opp_bet_when_checked += 1
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
                self.we_checked_this_hand = True
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


def analyze_opponent(opp_class, ngames=200, seed=None):
    """Run analysis games against a single opponent and extract feature vector."""
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
        'we_checked_to_opp': 0,
        'opp_bet_when_checked': 0,
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
        total_stats['we_checked_to_opp'] += p1.we_checked_to_opp
        total_stats['opp_bet_when_checked'] += p1.opp_bet_when_checked
    
    # Calculate 5-dimensional feature vector
    features = {}
    
    # Feature 1: fold_rate
    features['fold_rate'] = total_stats['our_bet_gets_fold'] / max(1, total_stats['our_bet_count'])
    
    # Feature 2: call_rate
    features['call_rate'] = total_stats['our_bet_gets_call'] / max(1, total_stats['our_bet_count'])
    
    # Feature 3: raise_rate
    features['raise_rate'] = total_stats['our_bet_gets_raise'] / max(1, total_stats['our_bet_count'])
    
    # Feature 4: bet_card_mean (average card when opponent bets at showdown)
    if total_stats['opp_bet_cards']:
        features['bet_card_mean'] = sum(total_stats['opp_bet_cards']) / len(total_stats['opp_bet_cards'])
    else:
        features['bet_card_mean'] = 0.5  # Default neutral value
    
    # Feature 5: aggression (how often opponent bets when checked to)
    features['aggression'] = total_stats['opp_bet_when_checked'] / max(1, total_stats['we_checked_to_opp'])
    
    # Additional stats for debugging
    features['win_rate'] = total_stats['wins'] / ngames
    features['hands_per_game'] = total_stats['hands_played'] / ngames
    features['opp_bet_freq'] = total_stats['opp_bet_count'] / max(1, 
        total_stats['opp_bet_count'] + total_stats['opp_check_count'] + 
        total_stats['opp_fold_count'] + total_stats['opp_call_count'])
    
    return features


def extract_feature_vector(features):
    """Extract 5D feature vector as a list."""
    return [
        features['fold_rate'],
        features['call_rate'],
        features['raise_rate'],
        features['bet_card_mean'],
        features['aggression']
    ]


def kmeans_clustering(data, k=5, max_iters=100, seed=42):
    """
    Simple k-means clustering implementation.
    data: list of (name, feature_vector) tuples
    Returns: dict mapping cluster_id to (centroid, member_names)
    """
    rng = random.Random(seed)
    
    # Extract just the vectors
    names = [d[0] for d in data]
    vectors = [d[1] for d in data]
    n = len(vectors)
    dim = len(vectors[0])
    
    # Initialize centroids randomly from data points
    indices = list(range(n))
    rng.shuffle(indices)
    centroids = [vectors[i][:] for i in indices[:k]]
    
    assignments = [0] * n
    
    for iteration in range(max_iters):
        # Assign each point to nearest centroid
        new_assignments = []
        for vec in vectors:
            min_dist = float('inf')
            best_cluster = 0
            for c_idx, centroid in enumerate(centroids):
                dist = sum((v - c) ** 2 for v, c in zip(vec, centroid))
                if dist < min_dist:
                    min_dist = dist
                    best_cluster = c_idx
            new_assignments.append(best_cluster)
        
        # Check for convergence
        if new_assignments == assignments:
            break
        assignments = new_assignments
        
        # Update centroids
        for c_idx in range(k):
            members = [vectors[i] for i in range(n) if assignments[i] == c_idx]
            if members:
                centroids[c_idx] = [
                    sum(m[d] for m in members) / len(members)
                    for d in range(dim)
                ]
    
    # Build result
    clusters = {}
    for c_idx in range(k):
        member_names = [names[i] for i in range(n) if assignments[i] == c_idx]
        clusters[c_idx] = {
            'centroid': centroids[c_idx],
            'members': member_names,
            'size': len(member_names)
        }
    
    return clusters


def name_archetype(centroid, features_by_name):
    """Assign a descriptive name to a cluster based on its centroid."""
    fold_rate, call_rate, raise_rate, bet_card_mean, aggression = centroid
    
    # Classification logic
    if fold_rate > 0.50:
        return 'passive_folder'
    elif fold_rate < 0.25 and call_rate > 0.40:
        return 'calling_station'
    elif raise_rate > 0.30 or aggression > 0.50:
        return 'aggressor'
    elif bet_card_mean > 0.55 and fold_rate < 0.40:
        return 'tight_value'
    else:
        return 'gto_balanced'


def compute_optimal_strategy(cluster_members, features_by_name):
    """
    Compute optimal strategy parameters for a cluster based on member characteristics.
    """
    if not cluster_members:
        return {'bet_mult': 3, 'bluff_mult': 1.0, 'value_mult': 1.0, 'call_mult': 1.0}
    
    # Get average features for this cluster
    avg_fold = sum(features_by_name[m]['fold_rate'] for m in cluster_members) / len(cluster_members)
    avg_call = sum(features_by_name[m]['call_rate'] for m in cluster_members) / len(cluster_members)
    avg_raise = sum(features_by_name[m]['raise_rate'] for m in cluster_members) / len(cluster_members)
    avg_aggression = sum(features_by_name[m]['aggression'] for m in cluster_members) / len(cluster_members)
    
    # Compute strategy based on opponent tendencies
    strategy = {}
    
    # bet_mult: Higher vs folders, lower vs callers/aggressors
    if avg_fold > 0.45:
        strategy['bet_mult'] = 5  # Overbet vs folders
    elif avg_call > 0.40 or avg_raise > 0.25:
        strategy['bet_mult'] = 2  # Smaller bets vs calling stations/aggressors
    else:
        strategy['bet_mult'] = 3  # Standard
    
    # bluff_mult: Higher vs folders, lower vs callers
    if avg_fold > 0.50:
        strategy['bluff_mult'] = 2.5  # Bluff lots vs folders
    elif avg_fold < 0.30:
        strategy['bluff_mult'] = 0.3  # Never bluff vs calling stations
    elif avg_raise > 0.25:
        strategy['bluff_mult'] = 0.5  # Minimal bluffs vs aggressors
    else:
        strategy['bluff_mult'] = 1.0  # Balanced
    
    # value_mult: Tighter vs aggressors (they pay off), wider vs folders
    if avg_raise > 0.25:
        strategy['value_mult'] = 1.15  # Wider value vs aggressors
    elif avg_fold > 0.50:
        strategy['value_mult'] = 1.10  # Slightly wider vs folders
    else:
        strategy['value_mult'] = 1.0  # Standard
    
    # call_mult: Wider vs aggressors (they bluff more), tighter vs tight players
    if avg_raise > 0.25 or avg_aggression > 0.45:
        strategy['call_mult'] = 0.85  # Call wider vs aggressors
    elif avg_fold > 0.50:
        strategy['call_mult'] = 1.15  # Tighter calls vs passive players
    else:
        strategy['call_mult'] = 1.0  # Standard
    
    return strategy


def main():
    """Run analysis on all training opponents and perform clustering."""
    print("=" * 80)
    print("OPPONENT CLUSTERING ANALYSIS")
    print("5-Dimensional Feature Extraction + K-Means Clustering")
    print("=" * 80)
    print()
    
    # Get opponent classes by name
    opp_dict = {opp.__name__: opp for opp in training_opponents}
    opp_dict['John3'] = John3
    
    # Analyze ALL training opponents
    features_by_name = {}
    data_for_clustering = []
    
    print(f"Analyzing {len(opp_dict)} opponents...")
    print()
    
    for i, (opp_name, opp_class) in enumerate(opp_dict.items()):
        sys.stdout.write(f'\r  Analyzing {i+1}/{len(opp_dict)}: {opp_name}...          ')
        sys.stdout.flush()
        
        features = analyze_opponent(opp_class, ngames=200, seed=42)
        features_by_name[opp_name] = features
        
        vector = extract_feature_vector(features)
        data_for_clustering.append((opp_name, vector))
    
    print()
    print()
    
    # Run k-means clustering
    print("Running k-means clustering (k=5)...")
    clusters = kmeans_clustering(data_for_clustering, k=5, seed=42)
    
    # Name the archetypes and compute strategies
    print()
    print("=" * 80)
    print("ARCHETYPE ANALYSIS")
    print("=" * 80)
    
    archetype_centroids = {}
    archetype_strategies = {}
    
    for c_idx, cluster in clusters.items():
        centroid = cluster['centroid']
        members = cluster['members']
        
        # Name this archetype
        archetype_name = name_archetype(centroid, features_by_name)
        
        # Handle duplicate names by appending index
        base_name = archetype_name
        suffix = 1
        while archetype_name in archetype_centroids:
            suffix += 1
            archetype_name = f"{base_name}_{suffix}"
        
        # Compute optimal strategy
        strategy = compute_optimal_strategy(members, features_by_name)
        
        archetype_centroids[archetype_name] = centroid
        archetype_strategies[archetype_name] = strategy
        
        print(f"\n{archetype_name.upper()} (n={len(members)}):")
        print(f"  Centroid: fold={centroid[0]:.2f}, call={centroid[1]:.2f}, "
              f"raise={centroid[2]:.2f}, bet_card={centroid[3]:.2f}, aggr={centroid[4]:.2f}")
        print(f"  Strategy: bet_mult={strategy['bet_mult']}, bluff_mult={strategy['bluff_mult']}, "
              f"value_mult={strategy['value_mult']}, call_mult={strategy['call_mult']}")
        print(f"  Members: {', '.join(sorted(members)[:10])}" + 
              (f"... (+{len(members)-10} more)" if len(members) > 10 else ""))
        
        # Show win rates for this cluster
        win_rates = [features_by_name[m]['win_rate'] for m in members]
        avg_win = sum(win_rates) / len(win_rates) if win_rates else 0
        print(f"  Avg win rate vs cluster: {avg_win*100:.1f}%")
    
    # Output Python code for embedding
    print()
    print("=" * 80)
    print("PYTHON CODE FOR pokerplayer.py")
    print("=" * 80)
    print()
    print("# Derived offline from training opponents - embedded as constants")
    print("ARCHETYPE_CENTROIDS = {")
    for name, centroid in archetype_centroids.items():
        print(f"    '{name}': [{centroid[0]:.3f}, {centroid[1]:.3f}, {centroid[2]:.3f}, "
              f"{centroid[3]:.3f}, {centroid[4]:.3f}],")
    print("}")
    print()
    print("ARCHETYPE_STRATEGIES = {")
    for name, strategy in archetype_strategies.items():
        print(f"    '{name}': {{'bet_mult': {strategy['bet_mult']}, "
              f"'bluff_mult': {strategy['bluff_mult']}, "
              f"'value_mult': {strategy['value_mult']}, "
              f"'call_mult': {strategy['call_mult']}}},")
    print("}")
    
    # Save detailed results
    print()
    print("=" * 80)
    print("FULL OPPONENT FEATURE DATA")
    print("=" * 80)
    print()
    print("Name        | Fold  | Call  | Raise | BetCard | Aggr  | WinRate")
    print("-" * 70)
    for name in sorted(features_by_name.keys()):
        f = features_by_name[name]
        print(f"{name:11s} | {f['fold_rate']:.3f} | {f['call_rate']:.3f} | "
              f"{f['raise_rate']:.3f} | {f['bet_card_mean']:.3f}   | {f['aggression']:.3f} | "
              f"{f['win_rate']*100:.0f}%")
    
    return archetype_centroids, archetype_strategies, features_by_name


if __name__ == '__main__':
    main()
