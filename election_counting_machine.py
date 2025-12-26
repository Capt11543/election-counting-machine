from candidate import Candidate
import parser as Parser
import stv as STV
import seat_allocation as SeatAllocation
import seat_election as SeatElection

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

elected = SeatElection.run(parties, achieved_quota, eliminated, True)

print("\nThe following candidates have been elected to Parliament:")
print(Candidate.names_in_list(elected, True, False))
print("Congratulations to the elected candidates!  Thank you for voting!")