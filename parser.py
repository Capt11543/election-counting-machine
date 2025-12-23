from ballot import Ballot
from candidate import Candidate


def choose_party_affiliation(name: str, include_party_affiliation, party_names: list[str]):
    if not include_party_affiliation:
        return None
    
    check_name = Candidate.find_party_affiliation(name)
    return check_name if check_name in party_names else "IND"


def parse_raw_ballots(filename: str, include_party_affiliation = True, party_names = []) -> tuple[list[Ballot], list[Candidate], list[str]]:
    ballots: list[Ballot] = []
    with open(filename, 'r') as myfile:
        raw_ballots = myfile.read()
        raw_ballots = raw_ballots.split("\n")

        for ballot in raw_ballots:
            ballots.append(Ballot(ballot[84:].split(", ")))
    
    candidate_names: list[str] = []
    infer_party_names = include_party_affiliation and party_names == []
    for ballot in ballots:
        for name in ballot.order:
            if name not in candidate_names:
                candidate_names.append(name)

                if infer_party_names:
                    if "(" in name and ")" in name:
                        new_party = name[name.index("(") + 1:name.index(")")]
                        if new_party not in party_names and "IND" not in new_party:
                            party_names.append(new_party)
                        
    candidate_preferences = {name: [0] * len(candidate_names) for name in candidate_names}
    for ballot in ballots:
        for position in range(len(ballot.order)):
            name = ballot.order[position]
            candidate_preferences[name][position] += 1
    
    candidates: list[Candidate] = []
    for name in candidate_names:
        candidates.append(Candidate(name[:name.index("(")], choose_party_affiliation(name, include_party_affiliation, party_names), candidate_preferences[name]))
    
    return ballots, candidates, party_names


def parse_party_lists(filename: str) -> dict[str, list[str]]:
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


def main():
    ballots_filename = input("Please enter the path to the raw ballots: ")
    ballots, candidates, party_names = parse_raw_ballots(ballots_filename)
    print ("Ballots: " + str(ballots))
    print("Candidates: " + str(candidates))
    print("Party Names: " + str(party_names))

if __name__ == "__main__":
    main()
