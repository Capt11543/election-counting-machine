from candidate import Candidate
from party import Party
import parser as Parser
import stv as STV
import seat_allocation as SeatAllocation
import seat_election as SeatElection

import random


def input_integer(message: str):
    result = 0

    no_problem = False
    while not no_problem:
        no_problem = True

        try:
            result = int(input(message))
        except ValueError:
            print("Please enter a valid integer.")
            no_problem = False


def main():
    parties_are_candidates = False
    simulate_new_system = True and parties_are_candidates

    # Get input from the user
    total_seats = input_integer("Please enter the number of seats: ") # Number of Winners
    seed = input_integer("Please provide with a seed: ")
    random.seed(seed)

    # Parse ballots
    party_lists = {}
    if simulate_new_system:
        party_lists = Parser.parse_party_lists()
    ballots, candidates, parties = Parser.parse_ballots(party_lists, parties_are_candidates, simulate_new_system)

    # Run the STV process
    achieved_quota, eliminated = STV.run(total_seats, ballots, candidates)
    print("\nThe following candidates have achieved a quota after transfers: ")
    print(Candidate.names_in_list(achieved_quota, False, True))

    print("\n---\n")

    SeatAllocation.run(parties, total_seats, achieved_quota, len(candidates), parties_are_candidates)
    print("\nThe parties have been apportioned the following number of seats:")
    print(Party.names_in_list(parties, 2))

    print("\n---\n")

    elected = SeatElection.run(parties, achieved_quota, eliminated, not parties_are_candidates)

    print("The following candidates have been elected to Parliament:")
    print(Candidate.names_in_list(elected, True, False))
    print("Congratulations to the elected candidates!  Thank you for voting!")


if __name__ == "__main__":
    main()