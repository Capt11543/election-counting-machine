import random as rand
import copy



def backtrack_rounds(round, rounds, tied, votes_total):
    if round < 1:
        return ""
    
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
        return backtrack_rounds(round - 1, rounds, least_votes, votes_total)


def compare_preferences(tied, num_candidates, preferences):
    for preference in range(num_candidates):
        ordinal_num = preference + 1
        ordinal_str = str(ordinal_num) + ("st" if (ordinal_num) % 10 == 1 and not (ordinal_num) / 10 == 1 else "nd" if (ordinal_num) % 10 == 2 and not (ordinal_num) / 10 == 1 else "rd" if (ordinal_num) % 10 == 3 and not (ordinal_num) / 10 == 1 else "th")

        print("Comparing " + ordinal_str + " choice votes...")

        lowest_count = votes_total
        lowest_candidates = []

        tied_this_round = {tied[i]: preferences[tied[i]][preference] for i in range(len(tied))}
        print(tied_this_round)

        for candidate in tied_this_round:
            candidate_count = tied_this_round[candidate]
            if candidate_count < lowest_count:
                lowest_count = candidate_count
                lowest_candidates = [candidate]
            elif candidate_count == lowest_count:
                lowest_candidates.append(candidate)

        if len(lowest_candidates) == 1:
            print("Tie broken after comparing " + ordinal_str  + " choice votes")
            return lowest_candidates[0]
        
        for candidate in tied_this_round:
            if candidate not in lowest_candidates:
                print(candidate + " is no longer tied.")
                tied.remove(candidate)
    
    return ""

def break_tie(round, rounds, tied, votes_total, num_candidates, preferences):
    result = backtrack_rounds(round, rounds, tied, votes_total)
    if result == "":
        result = compare_preferences(tied, num_candidates, preferences)
    if result == "":
        print("As the tie could not be resolved through other means, a candidate will be randomly eliminated.")
        result = rand.choice(tied)
    
    return result


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

candidate_preferences = {name: [0] * len(candidates) for name in candidates}
for ballot in ballots:
    ballot_order = ballot["order"]
    for position in range(len(ballot_order)):
        name = ballot_order[position]
        candidate_preferences[name][position] += 1

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


while len(elected) + len(eliminated) < len(candidates):
    print("\nRound " + str(round))
    
    for name in candidates:
        if not should_freeze_score(name):
            candidates[name] = 0
    
    for ballot in ballots:
        ballot_position = ballot["currpos"]
        ballot_order = ballot["order"]
        ballot_value = ballot["currvalue"]
        
        if not ballot_position == -1:
            check_name = ballot_order[ballot_position]
            if not should_freeze_score(check_name):
                candidates[check_name] += ballot_value
    
    elected = {name: candidates[name] for name in candidates if name in elected}
    
    print(candidates)
    
    temp = copy.deepcopy(candidates)
    rounds.append(temp)
    del temp
    
    quota_this_round = False
    for name, votes in candidates.items():
        if votes >= threshold:
            if name not in elected:
                elected[name] = votes
                
                quota_this_round = True
                print("The candidate " + name + " has been elected with " + str(votes) + " / " + str(threshold) + " votes.")

                if "(IND)" in name:
                    transfer_value = (votes - threshold) / votes
                    print(str(transfer_value * votes) + " votes are now transferred.")

                    for ballot in ballots:
                        ballot_order = ballot["order"]
                        ballot_position = ballot["currpos"]
                        
                        check_name = ballot_order[ballot_position]
                        if check_name == name:
                            ballot["currvalue"] *= transfer_value
    
    if not quota_this_round:
        least_votes = []
        least_votes_count = votes_total
        for name, votes in candidates.items():
            if not (name in elected or name in eliminated):
                if votes < least_votes_count:
                    least_votes = [name]
                    least_votes_count = votes
                elif votes == least_votes_count:
                    least_votes.append(name)
        
        if len(least_votes) == 1:
            print("The candidate " + least_votes[0] + " has been eliminated with " + str(least_votes_count) + " votes.")
            eliminated.append(least_votes[0])
        else:
            print("A tie has to be broken between " + str(least_votes) + ".")
            resolved = break_tie(round, rounds, least_votes, votes_total, len(candidates), candidate_preferences)
            print("The candidate " + resolved + " has been eliminated with " + str(least_votes_count) + " votes.")
            eliminated.append(resolved)

    for ballot in ballots:
        ballot_order = ballot["order"]
        ballot_position = ballot["currpos"]
        
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
        
        ballot["currpos"] = ballot_position

    round += 1


# Tally votes by party
for name in elected:
    for party in parties:
        if f"({party})" in name:
            parties[party] += elected[name]


# Result

print("\nThe following candidates have been elected:")
print(elected)

print("\n---\n")

print("The following votes have been won by each party:")
print(parties)


party_seats = {party: 0 for party in parties}
party_quotients = {party: parties[party] / (2 * party_seats[party] + 1) for party in parties}

seats_for_parties = SIZE
for name in elected:
    if "(IND)" in name:
        seats_for_parties -= 1

print(str(seats_for_parties) + " seats are to be apportioned among the parties.")

round = 0
while round < seats_for_parties:
    print("\nRound " + str(round))
    print("Party Seats:" + str(party_seats))
    print("Party Quotients:" + str(party_quotients))
    
    highest_quotient = 0
    highest_parties = []
    for party in parties:
        if party_quotients[party] > highest_quotient:
            highest_quotient = party_quotients[party]
            highest_parties = [party]
        elif party_quotients[party] == highest_quotient:
            highest_parties.append(party)
    
    if len(highest_parties) == 1:
        winning_party = highest_parties[0]
    else:
        winning_party = max(highest_parties, key=lambda x: parties[x])
    
    print(winning_party + " wins a seat this round.")
    
    party_seats[winning_party] += 1
    party_quotients[winning_party] = parties[winning_party] / (2 * party_seats[winning_party] + 1)
    
    round += 1

print("\nThe parties have been apportioned the following number of seats:")
print(party_seats)
