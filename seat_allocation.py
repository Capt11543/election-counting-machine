from candidate import Candidate
from party import Party
import tiebreak as Tiebreak
import random


def _get_num_seats_for_parties(total_seats: int, achieved_quota: list[Candidate]):
    for candidate in achieved_quota:
        if candidate.party_affiliation == "IND":
            total_seats -= 1
    
    return total_seats


def _break_tie(tied_parties: list[Party], achieved_quota: list[Candidate], num_candidates: int, parties_are_candidates: bool):
    tied_parties = Tiebreak.highest_party(tied_parties)
    if len(tied_parties) == 1:
        return tied_parties[0]
    
    tied_party_candidates = [candidate for candidate in achieved_quota if candidate.party_affiliation in [party.name for party in tied_parties]]
    if parties_are_candidates:
        highest_preference_candidate = Tiebreak.compare_preferences(tied_party_candidates, num_candidates, True)
        if highest_preference_candidate is not None:
            return Party.get_from_list(highest_preference_candidate.party_affiliation, tied_parties)
    else:
        most_votes_candidate = Tiebreak.highest_candidate(tied_party_candidates)
        if len(most_votes_candidate) == 1:
            return Party.get_from_list(most_votes_candidate[0].party_affiliation, tied_parties)
        
        highest_preference_candidate = Tiebreak.compare_preferences(most_votes_candidate, num_candidates, True)
        if highest_preference_candidate is not None:
            return Party.get_from_list(highest_preference_candidate.party_affiliation, tied_parties)
        
    return random.choice(tied_parties)


def _find_highest_party(parties: list[Party], achieved_quota: list[Candidate], num_candidates: int, parties_are_candidates: bool):
    party_quotients = {party: party.votes / (2 * party.seats + 1) for party in parties}
    print("Party Quotients:")
    print({party.name: party_quotients[party] for party in party_quotients})

    highest_party = Tiebreak.highest_party(party_quotients)
    
    if len(highest_party) == 1:
        return highest_party[0]
    else:
        return _break_tie(highest_party, achieved_quota, num_candidates, parties_are_candidates)


def run(parties: list[Party], total_seats: int, achieved_quota: list[Candidate], num_candidates: int, parties_are_candidates=False):
    for party in parties:
        party.votes = sum([candidate.votes for candidate in achieved_quota if candidate.party_affiliation == party.name])

    print("The number of votes won by each party is shown below: ")
    print(Party.names_in_list(parties, 1))

    seats_for_parties = _get_num_seats_for_parties(total_seats, achieved_quota)

    print(str(seats_for_parties) + " seats are to be apportioned among the parties.")

    round = 0
    while round < seats_for_parties:
        print("\nRound: " + str(round))
        print("Party Seats:")
        print(Party.names_in_list(parties, 2))
        highest_party = _find_highest_party(parties, achieved_quota, num_candidates, parties_are_candidates)
        print(highest_party.name + " wins a seat this round.")
        highest_party.seats += 1

        round += 1
