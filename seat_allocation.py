from candidate import Candidate
from party import Party


def _get_num_seats_for_parties(total_seats: int, achieved_quota: list[Candidate]):
    for candidate in achieved_quota:
        if candidate.party_affiliation == "IND":
            total_seats -= 1
    
    return total_seats


def _find_highest_party(parties: list[Party]):
    party_quotients = {party: party.votes / (2 * party.seats + 1) for party in parties}
    print("Party Quotients:")
    print({party.name: party_quotients[party] for party in party_quotients})

    highest_quotient = 0
    highest_party = []
    for party in party_quotients:
        if party_quotients[party] > highest_quotient:
            highest_party = [party]
            highest_quotient = party_quotients[party]
        elif party_quotients[party] == highest_quotient:
            highest_party.append(party)
    
    if len(highest_party) == 1:
        return highest_party[0]
    else:
        return max(highest_party, key=lambda x: party_quotients[x])


def run(parties: list[Party], total_seats: int, achieved_quota: list[Candidate]):
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
        highest_party = _find_highest_party(parties)
        highest_party.seats += 1

        round += 1
    else:
        print("\nThe parties have been apportioned the following number of seats:")
        print(Party.names_in_list(parties, 2))
