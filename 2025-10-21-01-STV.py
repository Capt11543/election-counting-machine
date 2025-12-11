import random as rand
import copy



def BreakTie(round, rounds, tied, votes_total):
    if round < 1:
        print("As the tie could not be resolved through other means, a candidate will be randomly eliminated.")
        return rand.choice(tied)
    tied = {i: rounds[round - 1][i] for i in tied}
    print("Backtracking to round " + str(round - 1) + ": " + str(tied))
    
    least_votes = []
    least_votes_count = votes_total
    for i, j in tied.items():
        if j < least_votes_count:
            least_votes = [i]
            least_votes_count = j
        elif j == least_votes_count:
            least_votes.append(i)
    
    if len(least_votes) == 1:
        print("The tie could be resolved by the totals of the previous round.")
        return least_votes[0]
    else:
        return BreakTie(round - 1, rounds, least_votes, votes_total)
    
    print()


# INPUT

SIZE = 16 # Number of Winners

myfile = open("input.txt") # Name (or path) of input file.
ballots = myfile.read()
ballots = ballots.split("\n")
for i in range(len(ballots)):
    ballots[i] = ballots[i][84:]
    ballots[i] = ballots[i].split(", ")

candidates = ['Twiscet (IND)',
              'bloodyrebals (IND)',
              'Talion77 (GREENS)',
              'ItsStormcraft (GREENS)',
              'Capt11543 (LPS)',
              'tortenwashere (LPS)',
              'MrRoyaltys (LPS)',
              'ConsequencesInc (LPS)',
              'Dartanboy (IND)',
              'JamesTheSlay (IND)',
              'Ayatha (IND)',
              'AmityBlamity (IND)',
              'Pepecuu (IND)',
              'WackJap (IND)',
              'ameslap (IND)',
              'RealImza (GREENS)',
              'SoggehToast (LPS)',
              'ConsequencesInc (LPS)',
              'roryyy_ (LPS)',
              'ComplexKing (IND)',
              'CasualGreyKnight (LPS)',
              'Taelor (IND)'] # List of all Candidates

elected = []
eliminated = []


# Initialising

for i in range(len(ballots)):
    ballots[i] = {"currpos": 0, "currvalue": 1, "order": ballots[i]}


candidates = {i: 0 for i in candidates}

votes_total = len(ballots)

threshold = votes_total / SIZE

print("Threshold for Election: " + str(threshold))

seed = int(input("Please provide with a seed: "))
rand.seed(seed)

# Round

round = 0
rounds = []

while True:
    print("\nRound " + str(round))
    
    # if len(candidates) - len(eliminated) <= SIZE:
    #     print("As there are only " + str(len(candidates) - len(eliminated) - len(elected)) + " candidates left and still " + str(SIZE - len(elected)) + " mandates, all remaining candidates will receive a mandate.")
    #     for i in candidates.keys():
    #         if i not in elected and i not in eliminated:
    #             elected.append(i)
    #             print("Candidate " + i + " was elected.")
    #     break
    if len(elected) + len(eliminated) >= len(candidates):
        print("All candidates have been elected or eliminated.")
        break
    
    for i, j in candidates.items():
        candidates[i] = 0
    for i in ballots:
        if not i["currpos"] == -1:
            candidates[i["order"][i["currpos"]]] += i["currvalue"]
    
    print(candidates)
    
    temp = copy.deepcopy(candidates)
    rounds.append(temp)
    del temp
    
    flag = 0
    for i, j in candidates.items():
        if j >= votes_total/SIZE:
            if i not in elected:
                elected.append(i)
                flag = 1
                print("The candidate " + i + " has been elected with " + str(j) + " / " + str(votes_total/SIZE) + " votes.")

                if "(IND)" in i:
                    print(str(j - votes_total/SIZE) + " votes are now transferred.")

                    for k in ballots:
                        if k["order"][k["currpos"]] == i:
                            k["currvalue"] *= (j - votes_total/SIZE) / j
    if flag == 0:
        least_votes = []
        least_votes_count = votes_total
        for i, j in candidates.items():
            if not (i in elected or i in eliminated):
                if j < least_votes_count:
                    least_votes = [i]
                    least_votes_count = j
                elif j == least_votes_count:
                    least_votes.append(i)
        
        if len(least_votes) == 1:
            print("The candidate " + least_votes[0] + " has been eliminated with " + str(least_votes_count) + " votes.")
            eliminated.append(least_votes[0])
        else:
            print("A tie has to be broken between " + str(least_votes) + ".")
            resolved = BreakTie(round, rounds, least_votes, votes_total)
            print("The candidate " + resolved + " has been eliminated with " + str(least_votes_count) + " votes.")
            eliminated.append(resolved)

    for i in ballots:
        ballotOrder = i["order"]
        ballotPosition = i["currpos"]
        
        deltaPos = 0
        checkName = ballotOrder[ballotPosition + deltaPos]
        while (checkName in elected and "(IND)" in checkName) or checkName in eliminated:
            deltaPos += 1
            if ballotPosition + deltaPos >= len(ballotOrder):
                break

            checkName = ballotOrder[ballotPosition + deltaPos]
        
        if ballotPosition + deltaPos >= len(ballotOrder):
            ballotPosition = -1
        else:
            ballotPosition += deltaPos
        
        i["currpos"] = ballotPosition

    round += 1


# Result

print("\nThe following candidates have been elected:")
print(elected)

input()
