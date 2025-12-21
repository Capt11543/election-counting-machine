import random as rand
import copy

import parser as Parser


def lowest_scoring(tied: dict[str, int]) -> list[str]:
    least_votes: list[str] = []
    least_votes_count = sum(tied.values())
    for name in tied:
        votes = tied[name]
        if votes < least_votes_count:
            least_votes = [name]
            least_votes_count = votes
        elif votes == least_votes_count:
            least_votes.append(name)
    
    return least_votes


def backtrack_rounds(round: int, rounds: list[dict[str, int]], tied: list[str], votes_total: int) -> str:
    if round < 1:
        return ""
    
    tied_this_round = {name: rounds[round - 1][name] for name in tied}
    print("Backtracking to round " + str(round - 1) + ": " + str(tied_this_round))

    least_votes = lowest_scoring(tied_this_round)
    
    if len(least_votes) == 1:
        print("The tie could be resolved by the totals of the previous round.")
        return least_votes[0]

    for candidate in tied_this_round:
        if candidate not in least_votes:
            print(candidate + " is no longer tied.")
            tied.remove(candidate)

    return backtrack_rounds(round - 1, rounds, tied, votes_total)


def compare_preferences(tied: list[str], votes_total: int, num_candidates: int, preferences: dict[str, list[int]]) -> str:
    for preference in range(num_candidates):
        ordinal_num = preference + 1
        ordinal_str = str(ordinal_num) + ("st" if (ordinal_num) % 10 == 1 and not (ordinal_num) / 10 == 1 else "nd" if (ordinal_num) % 10 == 2 and not (ordinal_num) / 10 == 1 else "rd" if (ordinal_num) % 10 == 3 and not (ordinal_num) / 10 == 1 else "th")

        print("Comparing " + ordinal_str + " choice votes...")

        tied_this_round = {tied[i]: preferences[tied[i]][preference] for i in range(len(tied))}
        print(tied_this_round)

        lowest_candidates = lowest_scoring(tied_this_round)

        if len(lowest_candidates) == 1:
            print("Tie broken after comparing " + ordinal_str  + " choice votes")
            return lowest_candidates[0]
        
        for candidate in tied_this_round:
            if candidate not in lowest_candidates:
                print(candidate + " is no longer tied.")
                tied.remove(candidate)
    
    return ""

def break_tie(round: int, rounds: list[dict[str, float]], tied: list[str], votes_total: int, num_candidates: int, preferences: dict[str, list[int]]) -> str:
    result = backtrack_rounds(round, rounds, tied, votes_total)
    if result == "":
        result = compare_preferences(tied, votes_total, num_candidates, preferences)
    if result == "":
        print("As the tie could not be resolved through other means, a candidate will be randomly eliminated.")
        result = rand.choice(tied)
    
    return result


# INPUT

SIZE = int(input("Please enter the number of seats: ")) # Number of Winners

filename = input("Please enter the path to the raw ballots: ")
ballots, candidates, parties, candidate_preferences = Parser.parse_raw_ballots(filename)

achieved_quorum = {}
eliminated = []

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
    return check_name in achieved_quorum and "(IND)" in check_name


def tally_candidate_votes():
    for name in candidates:
        if not should_freeze_score(name):
            candidates[name] = 0
    
    for ballot in ballots:
        if not ballot.exhausted():
            if not should_freeze_score(ballot.attributed_name()):
                candidates[ballot.attributed_name()] += ballot.value


while len(achieved_quorum) + len(eliminated) < len(candidates):
    print("\nRound " + str(round))
    
    tally_candidate_votes()
    achieved_quorum = {name: candidates[name] for name in candidates if name in achieved_quorum}
    
    print(candidates)
    
    temp = copy.deepcopy(candidates)
    rounds.append(temp)
    del temp
    
    quota_this_round = False
    for name, votes in candidates.items():
        if votes >= threshold:
            if name not in achieved_quorum:
                achieved_quorum[name] = votes
                
                quota_this_round = True
                print("The candidate " + name + " has been elected with " + str(votes) + " / " + str(threshold) + " votes.")

                if "(IND)" in name:
                    transfer_value = (votes - threshold) / votes
                    print(str(transfer_value * votes) + " votes are now transferred.")

                    for ballot in ballots:
                        if ballot.attributed_name() == name:
                            ballot.value *= transfer_value
    
    if not quota_this_round:
        least_votes = []
        least_votes_count = votes_total
        for name, votes in candidates.items():
            if not (name in achieved_quorum or name in eliminated):
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
        ballot.transfer(achieved_quorum, eliminated)

    round += 1
else:
    tally_candidate_votes()
    achieved_quorum = {name: candidates[name] for name in candidates if name in achieved_quorum}


# Tally votes by party
for name in achieved_quorum:
    for party in parties:
        if f"({party})" in name:
            parties[party] += achieved_quorum[name]


# Result

print("\nThe following candidates have achieved a quorum after transfers:")
print(achieved_quorum)

print("\n---\n")

print("The following votes have been won by each party:")
print(parties)


party_seats = {party: 0 for party in parties}
party_quotients = {party: parties[party] / (2 * party_seats[party] + 1) for party in parties}

seats_for_parties = SIZE
for name in achieved_quorum:
    if "(IND)" in name:
        seats_for_parties -= 1

print(str(seats_for_parties) + " seats are to be apportioned among the parties.")

round = 0
while round < seats_for_parties:
    print("\nRound " + str(round))
    print("Party Seats: " + str(party_seats))
    print("Party Quotients: " + str(party_quotients))
    
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


elected = []

for name in achieved_quorum:
    if "(IND)" in name:
        elected.append(name)

for party in parties:
    for _ in range(party_seats[party]):
        for name in achieved_quorum:
            if f"({party})" in name and name not in elected:
                elected.append(name)
                break
        else:
            for name in reversed(eliminated):
                if f"({party})" in name and name not in elected:
                    elected.append(name)
                    break
            else:
                elected.append(f"VACANT ({party})")

print("\nThe following candidates have been elected to Parliament:")
print(elected)
print("Congratulations to the elected candidates!  Thank you for voting!")