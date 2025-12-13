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
parties = ['LPS', 'GREENS'] # List of all Parties

elected = {}
eliminated = []


# Initialising

for i in range(len(ballots)):
    ballots[i] = {"currpos": 0, "currvalue": 1, "order": ballots[i]}


candidates = {name: 0 for name in candidates}
parties = {party: 0 for party in parties}

votes_total = len(ballots)

threshold = votes_total / SIZE

print("Threshold for Election: " + str(threshold))

seed = int(input("Please provide with a seed: "))
rand.seed(seed)

# Round

round = 0
rounds = []


def should_freeze_score(check_name):
    return check_name in elected and "(IND)" in check_name


while len(elected) + len(eliminated) >= len(candidates):
    print("\nRound " + str(round))
    
    for name in candidates:
        if not should_freeze_score(name):
            candidates[name] = 0
    
    for i in ballots:
        ballot_position = i["currpos"]
        ballot_order = i["order"]
        
        if not i["currpos"] == -1:
            check_name = candidates[ballot_order[ballot_position]]
            if not should_freeze_score(ballot_order[ballot_position]):
                candidates[i["order"][i["currpos"]]] += i["currvalue"]
    
    elected = {name: candidates[name] for name in candidates if name in elected}
    
    print(candidates)
    
    temp = copy.deepcopy(candidates)
    rounds.append(temp)
    del temp
    
    quota_this_round = False
    for i, j in candidates.items():
        if j >= votes_total/SIZE:
            if i not in elected:
                elected[i] = j
                quota_this_round = True
                print("The candidate " + i + " has been elected with " + str(j) + " / " + str(votes_total/SIZE) + " votes.")

                if "(IND)" in i:
                    print(str(j - votes_total/SIZE) + " votes are now transferred.")

                    for k in ballots:
                        if k["order"][k["currpos"]] == i:
                            k["currvalue"] *= (j - votes_total/SIZE) / j
    
    if not quota_this_round:
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
        ballot_order = i["order"]
        ballot_position = i["currpos"]
        
        delta_pos = 0
        check_name = ballot_order[ballot_position + delta_pos]
        while (check_name in elected and "(IND)" in check_name) or check_name in eliminated:
            delta_pos += 1
            if ballot_position + delta_pos >= len(ballot_order):
                break

            check_name = ballot_order[ballot_position + delta_pos]
        
        if ballot_position + delta_pos >= len(ballot_order):
            ballot_position = -1
        else:
            ballot_position += delta_pos
        
        i["currpos"] = ballot_position

    round += 1


# Tally votes by party
for name in elected:
    for party in parties:
        if f"({party})" in name:
            parties[party] += elected[name]


# Result

print("\nThe following candidates have been elected:")
print(elected)

print("---")

print("The following votes have been won by each party:")
print(parties)
