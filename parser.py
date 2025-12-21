from ballot import Ballot

def parse_raw_ballots(filename: str) -> tuple[list[Ballot], list[str], list[str], dict[str, list[int]]]:
    ballots: list[Ballot] = []
    candidate_names: list[str] = []
    party_names: list[str] = []
    candidate_preferences: dict[str, list[int]] = {}

    with open(filename, 'r') as myfile:
        raw_ballots = myfile.read()
        raw_ballots = raw_ballots.split("\n")

        for ballot in raw_ballots:
            ballots.append(Ballot(ballot[84:].split(", ")))
    
    for ballot in ballots:
        for name in ballot.order:
            if name not in candidate_names:
                candidate_names.append(name)
                if "(" in name and ")" in name:
                    party = name[(name.index("(") + 1):name.index(")")]
                    if not party == "IND" and party not in party_names:
                        party_names.append(party)
    
    candidate_preferences = {name: [0] * len(candidate_names) for name in candidate_names}
    for ballot in ballots:
        for position in range(len(ballot.order)):
            name = ballot.order[position]
            candidate_preferences[name][position] += 1
    
    return ballots, candidate_names, party_names, candidate_preferences


def parse_party_lists(filename: str) -> dict[str, list[str]]:
    party_lists: dict[str, list[str]] = {}

    with open(filename, 'r') as myfile:
        raw_lists = myfile.read()
        raw_lists = raw_lists.split("\n")

        for list in raw_lists:
            parts = list.split(": ")
            party = parts[0]
            candidates = parts[1].split(", ")

            party_lists[party] = candidates
    
    return party_lists


def main():
    lists_filename = input("Please enter the path to the party lists: ")
    party_lists = parse_party_lists(lists_filename)
    print(party_lists)


if __name__ == "__main__":
    main()
