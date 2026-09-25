from fileinput import filename

from ballot import Ballot
from candidate import Candidate
import input as Input
from party import Party
import json
import logger


def _parse_raw_ballots():
    ballots_filename = Input.input_string("Please input the path to the ballots (including \".json\"): ")

    ballots: list[Ballot] = []
    with open(ballots_filename, 'r') as myfile:
        ballot_file_json = json.load(myfile)

        raw_orders = ballot_file_json['ballots']
        for raw_order in raw_orders:
            ballots.append(Ballot(raw_order))
    
    return ballots


def _build_list(party_name: str, party_num: int):
    candidate_names = []
    num_candidates = Input.input_integer("PARTY #" + str(party_num) + " - How many candidates are running for " + party_name + "? ")
    
    logger.log_and_print("PARTY #" + str(party_num) + " - Enter the Minecraft usernames of the candidates in order below.")
    for i in range(num_candidates):
        name = Input.input_string("  " + str(i + 1) + ". ")
        candidate_names.append(name)
    
    return candidate_names


def _build_party_lists():
    lists = {}
    num_parties = Input.input_integer("How many parties are running in this election? ")
    for i in range(num_parties):
        party_name = Input.input_string("PARTY #" + str(i + 1) + " - Enter the name of the party EXACTLY as it appears on the ballot: ")
        lists[party_name] = _build_list(party_name, i + 1)

    return lists


def _build_independents_list():
    candidate_names = []
    num_candidates = Input.input_integer("How many independent candidates are running in this election? ")
    
    logger.log_and_print("Enter the Minecraft usernames of the independent candidates in order below.")
    for i in range(num_candidates):
        name = Input.input_string("  " + str(i + 1) + ". ")
        candidate_names.append(name)
    
    return candidate_names


def _build_raw_lists():
    party_lists = _build_party_lists()
    independent_names = _build_independents_list()

    if Input.yes_or_no("Save these lists to a file for future use? (y/n) "):
        new_lists_filename = Input.input_string("Enter the name of the file to save the lists to (not including \".json\"): ")
        new_lists_filename += ".json"
        with open(new_lists_filename, 'w') as output_file:
            json.dump({"parties": party_lists, "independents": independent_names}, output_file, indent=4)
        logger.log_and_print("Lists saved to " + new_lists_filename + ".")

    return party_lists, independent_names


def _parse_prebuilt_lists(filename: str):
    party_lists: dict[str, list[str]] = {}
    independent_names: list[str] = []

    try:
        with open(filename, 'r') as myfile:
            lists_file_json = json.load(myfile)

            party_lists = lists_file_json['parties']
            independent_names = lists_file_json['independents']
    except (OSError, json.JSONDecodeError, KeyError) as error:
        raise ValueError(f"Unable to load party lists from {filename!r}: {error}") from error
    
    return party_lists, independent_names


def _setup_raw_lists():
    lists_filename = Input.input_string("Please input the path to the party lists (including \".json\"; leave blank to manually input lists): ")

    if not lists_filename:
        return _build_raw_lists()
    
    try:
        return _parse_prebuilt_lists(lists_filename)
    except ValueError as error:
        logger.log_and_print(f"Error occurred while parsing prebuilt lists: {error}.  Please manually input the lists instead.")
        return _build_raw_lists()


def _parse_candidate_names(ballots: list[Ballot], party_lists: dict[str, list[str]], independent_names: list[str], parties_are_candidates: bool):
    candidate_names: list[str] = []
    party_names = [*party_lists]

    if parties_are_candidates:
        candidate_names += party_names
        candidate_names += independent_names
    else:
        infer_party_names = party_names == []
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


def parse_ballots(parties_are_candidates=False) -> tuple[list[Ballot], list[Candidate], list[Party]]:
    ballots = _parse_raw_ballots()
    party_lists, independent_names = _setup_raw_lists()
    
    candidate_names, party_names = _parse_candidate_names(ballots, party_lists, independent_names, parties_are_candidates)
    candidate_preferences = _parse_candidate_preferences(ballots, candidate_names)
    
    candidates, parties = _construct_final_lists(candidate_names, party_names, party_lists, candidate_preferences, parties_are_candidates)
    
    return ballots, candidates, parties
