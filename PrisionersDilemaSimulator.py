import random
import math

botsGlobal = []
names = ["id", "name", "strat", "population", "extinct", "timeserved", "matches Played", "populationDelta"]

defaultPopulation = 100
defaultMatchRounds = 10


# ----------Strats----------- #
def jesusStrategy(history, hash=""):
    # Cooperate w/ opponent
    return 0


def luciferStrategy(history, hash=""):
    # Defect
    return 1


def tftGenerousStrategy(history, hash=""):
    if len(history) < 1 or history[-1] == 0:
        return 0
    if random.randrange(100) <= 10:
        return 0
    return 1


def titForTatStrategy(history, hash=""):
    # Do what they did last time and assume they cooperated on first turn
    if len(history) < 1 or history[-1] == 0:
        return 0
    return 1


def massiveRetaliationStrategy(history, hash=""):
    if len(history) == 0:
        return 0
    if 1 in history:
        return 1
    return 0


def gaugeOpponentStrategy(history, hash=""):
    if len(history) == 0:
        return 0
    if (sum(history) / len(history)) < 1:
        return 0
    return 1


def testerStrategy(history, hash=""):
    if len(history) == 0:
        return 0
    x = (sum(history) / len(history))
    if x >= .01:
        return 1
    return history[-1]


def randomStrategy(history, hash=""):
    return random.randrange(2)


def middleManStrategy(history, hash=""):
    if len(history) == 0:
        return 0
    rep = sum(history) / len(history)
    if rep > .8:
        return 1
    if rep < .1:
        return 1
    return 0


def trustBreakerStrategy(history, hash=""):
    if len(history) == 0:
        return 0
    if history[-1] == 0:
        return 1
    return 0


def bestCaseStrategy(history, hash=""):
    if len(history) == 0:
        return 1
    if sum(history) / len(history) == 0 or sum(history) / len(history) == 1:
        return 1
    return 0


# ------Initilize/Distribute-------#
def testRun(rounds=1, roundsPerMatch=10, debug=0, startingPopulation=100):
    x = 1
    if getTotalPopulation() == 0:
        lotteryDistribution(startingPopulation)
    while x <= rounds:
        adjustPopulation()
        clearStats()
        playTournement(roundsPerMatch, debug)
        if x == rounds:
            stats()
        x += 1


def getTotalPopulation():
    pop = 0
    for bot in strategies:
        pop += bot[3]
    return pop


def generateBots():
    for bot in strategies:
        sets = bot[3]
        while sets > 0:
            # (id,  strategy,  wins,  loses, draws,  birth order, time served, matches played, games)
            bots.append([len(bots), bot[0], 0, 0, 0, 1, 0, 0, 0])
            sets -= 1
    return bots


def pulseCheck():
    survivors = 0
    for bot in strategies:
        if bot[4] == 0:
            survivors += 1
    return survivors


def evenDistribution(population, debug=0, lottoExtras=0):
    candidates = pulseCheck()
    fairShare = math.trunc(population / candidates)
    fairPile = fairShare * candidates
    lotteryPile = math.trunc(population - fairPile)

    for bot in strategies:
        if bot[4] == 0:
            bot[3] += fairShare

    if lottoExtras:
        lotteryDistribution(lotteryPile)


def lotteryDistribution(population, debug=0):
    p = population
    while p > 0:
        winner = random.randrange(len(strategies))
        strategies[winner][3] += 1
        p -= 1


def randomExecutions(number, safe=-1, ):
    n = number
    while n > 0:
        loser = random.randrange(len(strategies))
        if strategies[loser][4] == 0 and loser != safe:
            strategies[loser][3] -= 1
            n -= 1
            if strategies[loser][3] < 1:
                extinct(loser)


def birth(strategy, number=1, parent=0):
    strategies[strategy][3] += number
    strategies[strategy][4] = 0
    for x in range(number):
        bots.append([len(bots), strategy, 0, 0, 0, 1 + parent, 0, 0, 0])


def extinctionEvent():
    x = (((getTotalPopulation() - defaultPopulation) / defaultPopulation) % 10) * 10
    if x == 0:
        x = 1
    if x == 100:
        x = 99
    y = 100 - math.trunc(x)
    z = ((random.randrange(10) * 10.0) / 100) * getTotalPopulation()
    if random.randrange(y) == 1:
        print("------------------------------------------------------------------------")
        print("Massive Extenction Event: " + str(z) + " killed " + "1/" + str(y) + " chance")
        print("------------------------------------------------------------------------")
        randomExecutions(z)
        stats()


def extinct(victim):
    strategies[victim][4] = 1
    strategies[victim][3] = 0
    print(strategies[victim][1] + " has gone extinct!")


def clearStats():
    for bot in strategies:
        bot[5] = 0
        bot[6] = 0
        bot[7] = 0
        bot[8] = 0
        bot[9] = 0

# --------Initilize/Distribute----------##

# --------Simulate Logic-----------   #

punishments = [10, 2, 2, -5]


def judge(p1, p2):
    if p1 and p2:
        return [punishments[2], punishments[2]]
    if p1 and (not p2):
        return [punishments[0], punishments[3]]
    if not p1 and p2:
        return [punishments[3], punishments[0]]
    if not p1 and not p2:
        return [punishments[1], punishments[1]]


def playMatch(p1, p2, rounds=1, debug=0):
    p1History = []
    p2History = []
    p1TimeServed = 0.0
    p2TimeServed = 0.0

    for r in range(1, rounds):
        p1Play = strategies[p1[1]][2](p2History, p1[0])
        p2Play = strategies[p2[1]][2](p1History, p2[0])

        result = judge(p1Play, p2Play)

        p1History.append(p1Play)
        p2History.append(p2Play)

        p1TimeServed += result[0]
        p2TimeServed += result[1]

    return [p1TimeServed, p2TimeServed]


def playTournement(rounds=defaultMatchRounds, debug=0, ):
    tournementResults = []
    b = len(bots)
    for bot in range(b):
        for o in range(b - bot - 1):
            opponent = o + bot + 1
            if bot != opponent:
                matchResult = playMatch(bots[bot], bots[opponent], rounds, debug)
                recordScores(bots[bot][1], bots[opponent][1], matchResult, rounds, bots[bot][0], bots[opponent][0])
                tournementResults.append([bots[bot][1], bots[opponent][1], matchResult, rounds])
    extinctionEvent()
    return tournementResults


def adjustPopulation():
    adj = 0

    for bot in strategies:
        score = bot[5] - bot[6]
        rounds = bot[8]
        if rounds == 0:
            babies = 0
            draws = 0
        else:
            draws = abs(bot[9] - rounds) / 2
            points = bot[7] - draws
            babies = math.trunc(round((score + points) / rounds, 0))
        currentPop = bot[3]
        if (currentPop + babies) > 0:
            birth(bot[0], parent=generation)
            adj += babies
        elif bot[4] == 0 and bot[8] != 0:
            #extinct(bot[0])
            print("check")
        adj += 1
    return adj


def recordScores(s1, s2, results, rounds, p1, p2):
    if results[0] == results[1]:
        strategies[s1][9] += 1
        strategies[s2][9] += 1
        bots[p1][4] += 1
        bots[p2][4] += 1
    if results[0] > results[1]:
        # wins
        strategies[s1][5] += 1
        bots[p1][2] += 1
        # loss
        strategies[s2][6] += 1
        bots[p2][3] += 1
    if results[0] < results[1]:
        # win
        strategies[s2][5] += 1
        bots[p2][2] += 1
        # loss
        strategies[s1][6] += 1
        bots[p1][3] += 1
    # points
    strategies[s1][7] += results[0] / rounds
    strategies[s2][7] += results[1] / rounds
    bots[p1][6] += results[0]
    bots[p2][6] += results[1]

    # rounds
    strategies[s1][8] += rounds / defaultMatchRounds
    strategies[s2][8] += rounds / defaultMatchRounds
    bots[p1][7] += 1
    bots[p2][7] += 1
    bots[p1][8] += defaultMatchRounds
    bots[p2][8] += defaultMatchRounds


def stats(debug=0):
    currentPopulation = 0
    populationAdjustment = 0

    for bot in strategies:
        if bot[4] == 0:
            wins = str(bot[5])
            loses = str(bot[6])
            score = bot[5] - bot[6]
            rounds = bot[8]
            draws = bot[9]
            points = bot[7] - abs(draws - rounds) / 2
            pop = bot[3]

            if (rounds < 1):
                rounds = 1
            babies = round((score + points) / rounds, 0)

            print(bot[1])
            print("\tPopulation: " + str(pop) +
                  "\t\tWins: " + wins +
                  "\t\tLosses: " + loses +
                  "\t\tDraws:" + str(draws) +
                  "\t\tScore: " + str(score) +
                  "\t\tPoints: " + str(math.trunc(points)) +
                  "\t\tBabies: " + str(babies) +
                  "\t\tRounds: " + str(rounds))
            print("")
            currentPopulation += bot[3]
            populationAdjustment += math.trunc(babies)

    print("Total Population: " + str(currentPopulation) + " (" + str(populationAdjustment) + ")")


# -------------Stats--------------- #
bots = []
generation = 1
strategies = [[0, "Jesus", jesusStrategy, 0, 0, 0, 0, 0, 0, 0],
              [1, "Lucifer", luciferStrategy, 0, 0, 0, 0, 0, 0, 0],
              [2, "Tit For Tat", titForTatStrategy, 0, 0, 0, 0, 0, 0, 0],
              [3, "G-Unit", tftGenerousStrategy, 0, 0, 0, 0, 0, 0, 0],
              [4, "Massive Retaliation", massiveRetaliationStrategy, 0, 0, 0, 0, 0, 0, 0],
              [5, "Guage Oppenent", gaugeOpponentStrategy, 0, 0, 0, 0, 0, 0, 0],
              [6, "Tester", testerStrategy, 0, 0, 0, 0, 0, 0, 0],
              [7, "Trust Breaker", trustBreakerStrategy, 0, 0, 0, 0, 0, 0, 0],
              [8, "Best Case", bestCaseStrategy, 0, 0, 0, 0, 0, 0, 0],
              [9, "Middle Man Strategy", middleManStrategy, 0, 0, 0, 0, 0, 0, 0],
              [10, "Random", randomStrategy, 0, 0, 0, 0, 0, 0, 0]]

