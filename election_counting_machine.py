import random as rand
import copy

from candidate import Candidate
import parser as Parser


def lowest_scoring(tied: list[Candidate], preference_level = -1):
    least_votes: list[Candidate] = []
    least_votes_count = sum(candidate.votes for candidate in tied)
    for candidate in tied:
        compare_num = candidate.votes if preference_level < 0 else candidate.preferences[preference_level]
        if compare_num < least_votes_count:
            least_votes = [candidate]
            least_votes_count = compare_num
        elif compare_num == least_votes_count:
            least_votes.append(candidate)
    
    return least_votes


def backtrack_rounds(round: int, rounds: list[list[Candidate]], tied: list[Candidate]) -> Candidate | None:
    if round < 1:
        return None

    tied_this_round = [candidate for candidate in rounds[round - 1] if candidate in tied]
    print("Backtracking to round " + str(round - 1) + ": " + str(tied_this_round))

    least_votes = lowest_scoring(tied_this_round)
    
    if len(least_votes) == 1:
        print("The tie could be resolved by the totals of the previous round.")
        return least_votes[0]

    for candidate in tied_this_round:
        if candidate not in least_votes:
            print(candidate.name + " is no longer tied.")
            tied.remove(candidate)

    return backtrack_rounds(round - 1, rounds, tied)


def compare_preferences(tied: list[Candidate], num_candidates: int):
    for preference in range(num_candidates):
        ordinal_num = preference + 1
        ordinal_str = str(ordinal_num) + ("st" if (ordinal_num) % 10 == 1 and not (ordinal_num) / 10 == 1 else "nd" if (ordinal_num) % 10 == 2 and not (ordinal_num) / 10 == 1 else "rd" if (ordinal_num) % 10 == 3 and not (ordinal_num) / 10 == 1 else "th")

        print("Comparing " + ordinal_str + " choice votes...")
        lowest_candidates = lowest_scoring(tied, preference)

        if len(lowest_candidates) == 1:
            print("Tie broken after comparing " + ordinal_str  + " choice votes")
            return lowest_candidates[0]

        for candidate in tied:
            if candidate not in lowest_candidates:
                print(candidate.name + " is no longer tied.")
                tied.remove(candidate)

    return None


def break_tie(round: int, rounds: list[list[Candidate]], tied: list[Candidate], num_candidates: int):
    result = backtrack_rounds(round, rounds, tied)
    if result is None:
        result = compare_preferences(tied, num_candidates)
    if result is None:
        print("As the tie could not be resolved through other means, a candidate will be randomly eliminated.")
        result = rand.choice(tied)
    
    return result


# INPUT

SIZE = int(input("Please enter the number of seats: ")) # Number of Winners

filename = input("Please enter the path to the raw ballots: ")
ballots, candidates, parties = Parser.parse_raw_ballots(filename)

achieved_quorum: list[Candidate] = []
eliminated: list[Candidate] = []

parties = {party: 0 for party in parties}

votes_total = len(ballots)

threshold = votes_total / SIZE

print("Threshold for Election: " + str(threshold))

seed = int(input("Please provide with a seed: "))
rand.seed(seed)

# Round

round = 0
rounds = []


def should_freeze_score(check_candidate: Candidate):
    return check_candidate in achieved_quorum and check_candidate.party_affiliation == "IND"


def tally_candidate_votes():
    for candidate in candidates:
        candidate.tally_votes(ballots, should_freeze_score(candidate))


def print_candidates_with_vote_counts(candidates):
    print({candidate.name: candidate.votes for candidate in candidates})


while len(achieved_quorum) + len(eliminated) < len(candidates):
    print("\nRound " + str(round))
    
    tally_candidate_votes()
    
    print_candidates_with_vote_counts(candidates)
    
    temp = copy.deepcopy(candidates)
    rounds.append(temp)
    del temp
    
    quota_this_round = False
    for candidate in candidates:
        if candidate.votes >= threshold:
            if candidate not in achieved_quorum:
                achieved_quorum.append(candidate)

                quota_this_round = True
                print("The candidate " + candidate.name + " has been elected with " + str(candidate.votes) + " / " + str(threshold) + " votes.")

                if candidate.party_affiliation == "IND":
                    print(str(candidate.votes - threshold) + " votes are now transferred.")
                    for ballot in ballots:
                        if not ballot.exhausted() and ballot.attributed_name().startswith(candidate.name):
                            ballot.reweight(candidate.votes, threshold)

    if not quota_this_round:
        least_votes = lowest_scoring([candidate for candidate in candidates if candidate not in achieved_quorum and candidate not in eliminated])

        if len(least_votes) == 1:
            print("The candidate " + least_votes[0].name + " has been eliminated with " + str(least_votes[0].votes) + " votes.")
            eliminated.append(least_votes[0])
        else:
            print("A tie has to be broken between " + str([candidate.name for candidate in least_votes]) + ".")
            resolved = break_tie(round, rounds, least_votes, len(candidates))
            print("The candidate " + resolved.name + " has been eliminated with " + str(resolved.votes) + " votes.")
            eliminated.append(resolved)

    for ballot in ballots:
        ballot.transfer(candidates, achieved_quorum, eliminated)

    round += 1
else:
    tally_candidate_votes()

print("\nThe following candidates have achieved a quorum after transfers:")
print_candidates_with_vote_counts(achieved_quorum)


# Tally votes by party
for candidate in achieved_quorum:
    for party in parties:
        if candidate.party_affiliation == party:
            parties[party] += candidate.votes

print("\n---\n")

print("The following votes have been won by each party:")
print(parties)


party_seats = {party: 0 for party in parties}
party_quotients = {party: parties[party] / (2 * party_seats[party] + 1) for party in parties}

seats_for_parties = SIZE
for candidate in achieved_quorum:
    if candidate.party_affiliation == "IND":
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


elected: list[Candidate] = []

for candidate in achieved_quorum:
    if candidate.party_affiliation == "IND" and candidate not in elected:
        elected.append(candidate)

for party in parties:
    for _ in range(party_seats[party]):
        for candidate in achieved_quorum:
            if candidate.party_affiliation == party and candidate not in elected:
                elected.append(candidate)
                break
        else:
            for candidate in reversed(eliminated):
                if candidate.party_affiliation == party and candidate not in elected:
                    elected.append(candidate)
                    break
            else:
                elected.append(Candidate("VACANT", party, []))

print("\nThe following candidates have been elected to Parliament:")
print([candidate.name + " (" + candidate.party_affiliation + ")" for candidate in elected])
print("Congratulations to the elected candidates!  Thank you for voting!")