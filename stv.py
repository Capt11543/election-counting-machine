from candidate import Candidate
from decimal import *
import tiebreak as Tiebreak
import random
import copy
import logger as Logger

# only needed for type checking
from ballot import Ballot


def _calculate_threshold(total_votes: int, total_seats: int):
    result = Decimal(total_votes / total_seats)
    result = result.quantize(Decimal('1.00000'))
    return result


def _should_freeze_score(check_candidate: Candidate, achieved_quota: list[Candidate], is_special_election: bool):
    if check_candidate in achieved_quota:
        if check_candidate.party_affiliation == "IND" or is_special_election:
            return True
    return False


def _tally_candidate_votes(candidates: list[Candidate], ballots: list[Ballot], achieved_quota: list[Candidate], is_special_election: bool):
    for candidate in candidates:
        candidate.tally_votes(ballots, _should_freeze_score(candidate, achieved_quota, is_special_election))


def _save_round(rounds: list[list[Candidate]], this_round: list[Candidate]):
    temp = copy.deepcopy(this_round)
    rounds.append(temp)


def _reweight_ballots(threshold: float, candidate: Candidate, ballots: list[Ballot], is_special_election: bool):
    if not is_special_election and not candidate.party_affiliation == "IND":
        return

    Logger.log_and_print(f"{str(candidate.votes - threshold)} votes are now transferred.")

    for ballot in ballots:
        if ballot.exhausted():
            continue

        if ballot.attributed_name().startswith(candidate.name):
            ballot.reweight(candidate.votes, threshold)


def _award_quotas(threshold: float, candidates: list[Candidate], ballots: list[Ballot], achieved_quota: list[Candidate], is_special_election: bool):
    awarded_quota = False
    for candidate in candidates:
        if candidate.votes >= threshold:
            if candidate not in achieved_quota:
                achieved_quota.append(candidate)

                awarded_quota = True
                Logger.log_and_print(f"{candidate.name} has been elected with {candidate.votes} / {threshold} votes.")

                _reweight_ballots(threshold, candidate, ballots, is_special_election)
    
    return awarded_quota


def _break_tie(tied: list[Candidate], round: int, rounds: list[list[Candidate]], num_candidates):
    result = Tiebreak.backtrack_rounds(tied, round, rounds)

    if result is None:
        result = Tiebreak.compare_preferences(tied, num_candidates)
    
    if result is None:
        result = random.choice(tied)
    
    return result


def _eliminate_lowest_scorer(in_contention: list[Candidate], round: int, rounds: list[list[Candidate]], num_candidates: int):
    lowest_scorers: list[Candidate] = Tiebreak.lowest_candidate(in_contention)
    eliminated_candidate: Candidate = None
    
    if lowest_scorers is not None:
        if len(lowest_scorers) == 1:
            eliminated_candidate = lowest_scorers[0]
        else:
            Logger.log_and_print("A tie has to be broken between: " + str(Candidate.names_in_list(lowest_scorers, False, True)))
            eliminated_candidate = _break_tie(lowest_scorers, round, rounds, num_candidates)
    
    Logger.log_and_print(eliminated_candidate.name + " has been eliminated with " + str(eliminated_candidate.votes) + " votes.")
    return eliminated_candidate


def _transfer_ballots(ballots: list[Ballot], candidates: list[Candidate], achieved_quota: list[Candidate], eliminated: list[Candidate], is_special_election: bool):
    for ballot in ballots:
        ballot.transfer(candidates, achieved_quota, eliminated, is_special_election)


def run(total_seats: int, ballots: list[Ballot], candidates: list[Candidate], is_special_election: bool):
    total_votes = len(ballots)
    threshold = _calculate_threshold(total_votes, total_seats)
    Logger.log_and_print("Threshold to achieve quota: " + str(threshold))

    achieved_quota: list[Candidate] = []
    eliminated: list[Candidate] = []

    round = 0
    rounds: list[list[Candidate]] = []
    while len(achieved_quota) + len(eliminated) < len(candidates):
        Logger.log_and_print("\nRound " + str(round))
        _tally_candidate_votes(candidates, ballots, achieved_quota, is_special_election)
        Logger.log_and_print(str(Candidate.names_in_list(candidates, False, True)))
        _save_round(rounds, candidates)

        in_contention = [candidate for candidate in candidates if candidate not in achieved_quota and candidate not in eliminated]
        
        if is_special_election:
            if len(in_contention) <= total_seats - len(achieved_quota):
                Logger.log_and_print("There are as many unfilled seats as candidates remaining in contention.  The following candidates are elected:")
                Logger.log_and_print(str(Candidate.names_in_list(in_contention, False, True)))
                achieved_quota.extend(in_contention)
                continue
        
        awarded_quota = _award_quotas(threshold, candidates, ballots, achieved_quota, is_special_election)
        if not awarded_quota:
            eliminated.append(_eliminate_lowest_scorer(in_contention, round, rounds, len(candidates)))
        
        _transfer_ballots(ballots, candidates, achieved_quota, eliminated, is_special_election)

        round += 1
    else:
        _tally_candidate_votes(candidates, ballots, achieved_quota, is_special_election)
    
    return achieved_quota, eliminated


def main():
    pass


if __name__ == "__main__":
    main()