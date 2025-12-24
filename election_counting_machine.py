from candidate import Candidate
import parser as Parser
import stv as STV

import random


# Get input from the user
SIZE = int(input("Please enter the number of seats: ")) # Number of Winners
filename = input("Please enter the path to the raw ballots: ")
seed = int(input("Please provide with a seed: "))
random.seed(seed)

# Parse ballots
ballots, candidates, parties = Parser.parse_raw_ballots(filename)

# Run the STV process
achieved_quota, eliminated = STV.run(SIZE, ballots, candidates)
print("\nThe following candidates have achieved a quota after transfers: ")
print(Candidate.names_in_list(achieved_quota, False, True))


# Tally votes by party
parties = {party: 0 for party in parties}

for candidate in achieved_quota:
    for party in parties:
        if candidate.party_affiliation == party:
            parties[party] += candidate.votes

print("\n---\n")

print("The following votes have been won by each party:")
print(parties)

party_seats = {party: 0 for party in parties}
party_quotients = {party: parties[party] / (2 * party_seats[party] + 1) for party in parties}

seats_for_parties = SIZE
for candidate in achieved_quota:
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

for candidate in achieved_quota:
    if candidate.party_affiliation == "IND" and candidate not in elected:
        elected.append(candidate)

for party in parties:
    for _ in range(party_seats[party]):
        for candidate in achieved_quota:
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
print(Candidate.names_in_list(elected, True, False))
print("Congratulations to the elected candidates!  Thank you for voting!")