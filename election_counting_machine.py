from candidate import Candidate
import parser as Parser
import stv as STV
import seat_allocation as SeatAllocation

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

print("\n---\n")

SeatAllocation.run(parties, SIZE, achieved_quota)


elected: list[Candidate] = []

for candidate in achieved_quota:
    if candidate.party_affiliation == "IND" and candidate not in elected:
        elected.append(candidate)

for party in parties:
    for _ in range(party.seats):
        for candidate in achieved_quota:
            if candidate.party_affiliation == party.name and candidate not in elected:
                elected.append(candidate)
                break
        else:
            for candidate in reversed(eliminated):
                if candidate.party_affiliation == party.name and candidate not in elected:
                    elected.append(candidate)
                    break
            else:
                elected.append(Candidate("VACANT", party.name, []))

print("\nThe following candidates have been elected to Parliament:")
print(Candidate.names_in_list(elected, True, False))
print("Congratulations to the elected candidates!  Thank you for voting!")