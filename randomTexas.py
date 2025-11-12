import sys
import time
import random

def RandomNumberTexasHoldem(p1, p2, points, rng):
    playerScore1 = float(points)
    playerScore2 = float(points)
    SmallBlind = rng.random()<.5
    count = 0
    minbet = 1.0
    while playerScore1 > 0 and playerScore2 > 0 :
        minscore = min(playerScore1, playerScore2)
        card1=rng.random()
        card2=rng.random()
        if SmallBlind:
            p1.start(True, card1, playerScore1, playerScore2, minbet, minbet)
            p2.start(False, card2, playerScore2, playerScore1, minbet, 0)
        else:
            p1.start(False, card1, playerScore1, playerScore2, minbet, 0)
            p2.start(True, card2, playerScore2, playerScore1, minbet, minbet)
        oldBetPot = min(minbet, minscore)
        betPot = min(2*minbet, minscore)
        turn = SmallBlind
        firstbet = True
        ongoing = True
        while ongoing:
            if turn:
                bet = p2.bet(card2, playerScore2, playerScore1, minbet, betPot)
            else:
                bet = p1.bet(card1, playerScore1, playerScore2, minbet, betPot)
            if bet%minbet != 0 and bet < minscore and bet != betPot:
                # Fix the bet by rounding down to the nearest minbet multiple
                fix = float(int(bet / minbet) * minbet)
                who = p2 if turn else p1
                print(f"{who.__class__.__name__} did not bet a multiple of the minimum bet: bet={bet} minbet={minbet} fix={fix}")
                bet = fix
            bet = min(bet, minscore)
            #print(card1, card2, turn, bet)
            if bet < betPot:
                # fold
                result = 0
                betPot = oldBetPot
                turn = not(turn)
                ongoing=False
            elif bet == betPot and not(firstbet):
                # call
                betPot = bet
                turn = card2 > card1
                result=1
                ongoing=False
            else:
                # raise (or call on small-blind's first bet)
                firstbet = False
                oldBetPot = betPot
                betPot = bet
                turn = not(turn)
        if turn:
            playerScore1 = playerScore1 - betPot
            playerScore2 = playerScore2 + betPot
            if result==0:
                p1.end(False, None, playerScore1, playerScore2, minbet, betPot)
                p2.end(True, None, playerScore2, playerScore1, minbet, betPot)
            else:
                p1.end(False, card2, playerScore1, playerScore2, minbet, betPot)
                p2.end(True, card1, playerScore2, playerScore1, minbet, betPot)
        else:
            playerScore1 = playerScore1 + betPot
            playerScore2 = playerScore2 - betPot
            if result==0:
                p1.end(True, None, playerScore1, playerScore2, minbet, betPot)
                p2.end(False, None, playerScore2, playerScore1, minbet, betPot)
            else:
                p1.end(True, card2, playerScore1, playerScore2, minbet, betPot)
                p2.end(False, card1, playerScore2, playerScore1, minbet, betPot)
        SmallBlind = not(SmallBlind)
        count = count + 1
        if count == 100:
            minbet = 2*minbet
            count = 0
    if playerScore1==0.0:
        return 2
    else:
        return 1

def pokerTest(p1_class, p2_class, n, verbosity=0, seed=None):
    rng = random.Random(seed)
    names = [p1_class.__name__, p2_class.__name__]
    wins = [0,0]
    for i in range(n):
        # Reset the players for each game.
        p1 = p1_class()
        p2 = p2_class()
        if verbosity > 1:
            sys.stdout.write(f'\r{names[0]:>5s} won {int(wins[0]/(i+1)*100):3d}% against {names[1]}  {i+1}/{n}')
            sys.stdout.flush()
        result = RandomNumberTexasHoldem(p1, p2,
                                         points=100,
                                         rng=rng)
        wins[result-1] += 1
    if verbosity > 1:
        sys.stdout.write('\r' + ' ' * 100 + '\r')
    if verbosity > 0:
        print(f'{names[0]:>5s} won {int(wins[0]/n*100):3d}% against {names[1]}')
    return wins[0]/n

def play (p1_class, opps, ngames, verbosity=2):
    start = time.perf_counter()
    results=[]
    for o in opps:
        hold=pokerTest(p1_class, o, ngames, verbosity)
        results.append(hold)
    score=sum(results)/len(opps)
    end=time.perf_counter()
    print('Score is %.3f.' % score)
    print('Time to run is %.2f seconds.' % (end-start))
    return sum(results)/len(opps)
