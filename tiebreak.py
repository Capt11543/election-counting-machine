from candidate import Candidate
from party import Party
from typing import Any
from decimal import *
import logger as Logger


def _find_extreme_scorers(compare_objects: dict[Any, float], highest=False):
    extreme_scorers = []
    extreme_score = Decimal(-1.00000) if highest else sum(compare_objects.values())

    for object, score in compare_objects.items():
        condition = score > extreme_score if highest else score < extreme_score
        if condition:
            extreme_scorers = [object]
            extreme_score = score
        elif score == extreme_score:
            extreme_scorers.append(object)
    
    return extreme_scorers


def lowest_candidate(candidates: list[Candidate], preference_level = -1) -> list[Candidate]:
    return _find_extreme_scorers({candidate: candidate.preferences[preference_level] if preference_level > -1 else candidate.votes for candidate in candidates})


def highest_candidate(candidates: list[Candidate], preference_level = -1) -> list[Candidate]:
    return _find_extreme_scorers({candidate: candidate.preferences[preference_level] if preference_level > -1 else candidate.votes for candidate in candidates}, True)


def _is_quotient_dict(parties: list[Party] | dict[Party, float]):
    if not isinstance(parties, dict):
        return False
    
    return all(isinstance(key, Party) and isinstance(value, Decimal) for key, value in parties.items())


def highest_party(parties: list[Party] | dict[Party, float]) -> list[Party]:
    if _is_quotient_dict(parties):
        return _find_extreme_scorers(parties, True)
    
    return _find_extreme_scorers({party: party.votes for party in parties}, True)


def backtrack_rounds(tied: list[Candidate], round: int, rounds: list[list[Candidate]]):
    if round < 1:
        return None
    
    tied_this_round = [candidate for candidate in rounds[round - 1] if candidate.name in [candidate.name for candidate in tied]]
    Logger.log_and_print("Backtracking to round " + str(round - 1) + ":")
    Logger.log_and_print(str(Candidate.names_in_list(tied_this_round, False, True)))

    lowest_scoring = lowest_candidate(tied_this_round)

    if len(lowest_scoring) == 1:
        Logger.log_and_print("Tie broken after comparing votes from round " + str(round - 1) + ".")
        return lowest_scoring[0]
    
    for candidate in tied_this_round:
        if candidate not in lowest_scoring:
            Logger.log_and_print(candidate.name + " is no longer tied.")
            tied.remove(candidate)
    
    return backtrack_rounds(tied, round - 1, rounds)


def compare_preferences(tied: list[Candidate], num_candidates: int, highest=False):
    for preference in range(num_candidates):
        ordinal_num = preference + 1
        ordinal_str = str(ordinal_num) + ("st" if (ordinal_num) % 10 == 1 and not (ordinal_num) // 10 == 1 else "nd" if (ordinal_num) % 10 == 2 and not (ordinal_num) // 10 == 1 else "rd" if (ordinal_num) % 10 == 3 and not (ordinal_num) // 10 == 1 else "th")

        Logger.log_and_print("Comparing " + ordinal_str + "-choice votes...")
        Logger.log_and_print(str(Candidate.names_in_list(tied, False, True, preference)))
        lowest_scoring = highest_candidate(tied, preference) if highest else lowest_candidate(tied, preference)

        if len(lowest_scoring) == 1:
            Logger.log_and_print("Tie broken after comparing " + ordinal_str + "-choice votes.")
            return lowest_scoring[0]
        
        no_longer_tied = []
        for candidate in tied:
            if candidate not in lowest_scoring:
                Logger.log_and_print(candidate.name + " is no longer tied.")
                no_longer_tied.append(candidate)
        
        for candidate in no_longer_tied:
            tied.remove(candidate)
    
    return None