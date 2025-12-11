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
ballot = myfile.read()
ballot = ballot.split("\n")
for i in range(len(ballot)):
    ballot[i] = ballot[i][84:]
    ballot[i] = ballot[i].split(", ")

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

for i in range(len(ballot)):
    ballot[i] = {"currpos": 0, "currvalue": 1, "order": ballot[i]}


candidates = {i: 0 for i in candidates}

votes_total = len(ballot)

threshold = votes_total / SIZE

print(threshold)

seed = int(input("Please provide with a seed: "))
rand.seed(seed)

# Round

round = 0
rounds = []

while True:
    print("\nRound " + str(round))
    if len(candidates) - len(eliminated) <= SIZE:
        print("As there are only " + str(len(candidates) - len(eliminated) - len(elected)) + " candidates left and still " + str(SIZE - len(elected)) + " mandates, all remaining candidates will receive a mandate.")
        for i in candidates.keys():
            if i not in elected and i not in eliminated:
                elected.append(i)
                print("Candidate " + i + " was elected.")
        break
    
    for i, j in candidates.items():
        candidates[i] = 0
    for i in ballot:
        if i["currpos"] != -1:
            candidates[i["order"][i["currpos"]]] += i["currvalue"]
    
    temp = copy.deepcopy(candidates)
    rounds.append(temp)
    del temp
    
    flag = 0
    for i, j in candidates.items():
        if j >= votes_total/SIZE:
            elected.append(i)
            flag = 1
            print("The candidate " + i + " has attained " + str(j) + " / " + str(votes_total/SIZE) + " votes.")
            print(str(j - votes_total/SIZE) + " votes are now transferred.")
            for k in ballot:
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

    for i in ballot:
        j = 0
        while (i["order"][i["currpos"] + j] in elected or i["order"][i["currpos"] + j] in eliminated):
            j += 1
            if i["currpos"] + j >= len(i["order"]):
                break
        if i["currpos"] + j >= len(i["order"]):
            i["currpos"] = -1
        else:
            i["currpos"] += j

    round += 1


# Result

print("\nThe following candidates have been elected:")
print(elected)

input()
