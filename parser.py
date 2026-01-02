from ballot import Ballot
from candidate import Candidate
from party import Party


def _convert_to_hypothetical(raw_order: list[str], party_names: list[str]):
    if not party_names:
        raise ValueError("party_names may not be empty or null")

    new_order: list[str] = []
    found_in_order = {name: False for name in party_names}

    for name in raw_order:
        party_affiliation = Candidate.find_party_affiliation(name, False, "")
        if party_affiliation in party_names:
            if not found_in_order[party_affiliation]:
                new_order.append(party_affiliation)
                found_in_order[party_affiliation] = True
        elif party_affiliation == "IND":
            new_order.append(Candidate.strip_party_affiliation(name))
        else:
            new_order.append(name)

    return new_order


def _parse_raw_ballots(filename: str, simulate_new_system: bool, party_names=None):
    if simulate_new_system and party_names is None:
        raise ValueError("party_names cannot be None if simulate_new_system is True")

    ballots: list[Ballot] = []
    with open(filename, 'r') as myfile:
        raw_ballots = myfile.read()
        raw_ballots = raw_ballots.split("\n")

        for ballot in raw_ballots:
            raw_order = ballot[84:].split(", ")

            if simulate_new_system:
                raw_order = _convert_to_hypothetical(raw_order, party_names)

            ballots.append(Ballot(raw_order))
    
    return ballots


def _parse_candidate_names(ballots: list[Ballot], party_lists: dict[str, list[str]], parties_are_candidates):
    candidate_names: list[str] = []
    party_names = [*party_lists]

    if parties_are_candidates:
        candidate_names += party_names

    infer_party_names = not parties_are_candidates and party_names == []
    for ballot in ballots:
        for name in ballot.order:
            if name not in candidate_names:
                candidate_names.append(name)

                if infer_party_names:
                    if "(" in name and ")" in name:
                        new_party = name[name.index("(") + 1:name.index(")")]
                        if new_party not in party_names and "IND" not in new_party:
                            party_names.append(new_party)
    
    return candidate_names, party_names


def _parse_candidate_preferences(ballots: list[Ballot], candidate_names: list[str]):
    candidate_preferences = {name: [0] * len(candidate_names) for name in candidate_names}
    for ballot in ballots:
        for position in range(len(ballot.order)):
            name = ballot.order[position]
            candidate_preferences[name][position] += 1
    
    return candidate_preferences


def _choose_party_affiliation(name: str, party_names: list[str], parties_are_candidates: bool, default="IND"):
    check_name = Candidate.find_party_affiliation(name, parties_are_candidates)
    return check_name if check_name in party_names else default


def _construct_final_lists(candidate_names: list[str], party_names: list[str], party_lists: dict[str, list[str]], candidate_preferences: dict[str, list[int]], parties_are_candidates: bool):
    candidates: list[Candidate] = []
    for name in candidate_names:
        candidates.append(Candidate(Candidate.strip_party_affiliation(name), _choose_party_affiliation(name, party_names, parties_are_candidates), candidate_preferences[name]))
    
    parties: list[Party] = []
    for name in party_names:
        parties.append(Party(name, party_lists[name] if name in party_lists else []))
    
    return candidates, parties


def parse_ballots(party_lists: dict[str, list[str]] = {}, parties_are_candidates=False, simulate_new_system=False) -> tuple[list[Ballot], list[Candidate], list[Party]]:
    filename = input("Please input the path to the ballots: ")
    
    ballots = _parse_raw_ballots(filename, simulate_new_system, party_lists)
    
    candidate_names, party_names = _parse_candidate_names(ballots, party_lists, parties_are_candidates)
    candidate_preferences = _parse_candidate_preferences(ballots, candidate_names)
    
    candidates, parties = _construct_final_lists(candidate_names, party_names, party_lists, candidate_preferences, parties_are_candidates)
    
    return ballots, candidates, parties


def parse_party_lists() -> dict[str, list[str]]:
    filename = input("Please input the path to the party lists: ")

    party_lists: dict[str, list[str]] = {}

    with open(filename, 'r') as myfile:
        raw_lists = myfile.read()
        raw_lists = raw_lists.split("\n")

        for plist in raw_lists:
            parts = plist.split(": ")
            party = parts[0]
            candidates = parts[1].split(", ")

            party_lists[party] = candidates
    
    return party_lists
