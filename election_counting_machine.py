from candidate import Candidate
from party import Party
from input import *
import parser as Parser
import stv as STV
import seat_allocation as SeatAllocation
import seat_election as SeatElection

import random


def main():
    # Get input from the user
    is_special_election = yes_or_no("Is this a special election? (y/n): ")
    total_seats = input_integer("Please enter the number of seats: ") # Number of Winners
    seed = input_integer("Please provide with a seed: ")
    random.seed(seed)

    parties_are_candidates = True and not is_special_election

    # Parse ballots
    party_lists = {}
    if parties_are_candidates:
        party_lists = Parser.parse_party_lists()
    ballots, candidates, parties = Parser.parse_ballots(party_lists, parties_are_candidates)

    # Run the STV process
    achieved_quota, eliminated = STV.run(total_seats, ballots, candidates, is_special_election)
    print("\nThe following candidates have achieved a quota after transfers: ")
    print(Candidate.names_in_list(achieved_quota, False, True))

    print("\n---\n")

    # Run the Seat Allocation process
    if not is_special_election:
        SeatAllocation.run(parties, total_seats, achieved_quota, len(candidates), parties_are_candidates)
        print("\nThe parties have been apportioned the following number of seats:")
        print(Party.names_in_list(parties, 2))

        print("\n---\n")

    elected = achieved_quota if is_special_election else SeatElection.run(parties, achieved_quota, eliminated, not parties_are_candidates)

    print("The following candidates have been elected to Parliament:")
    print(Candidate.names_in_list(elected, True, False))
    print("Congratulations to the elected candidates!  Thank you for voting!")


if __name__ == "__main__":
    main()