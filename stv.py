import tiebreak as Tiebreak
from candidate import Candidate
import random
import copy

# only needed for type checking
from ballot import Ballot


def _should_freeze_score(check_candidate: Candidate, achieved_quota: list[Candidate]):
    if check_candidate in achieved_quota:
        if check_candidate.party_affiliation == "IND":
            return True
    return False


def _tally_candidate_votes(candidates: list[Candidate], ballots: list[Ballot], achieved_quota: list[Candidate]):
    for candidate in candidates:
        candidate.tally_votes(ballots, _should_freeze_score(candidate, achieved_quota))


def _save_round(rounds: list[list[Candidate]], this_round: list[Candidate]):
    temp = copy.deepcopy(this_round)
    rounds.append(temp)


def _reweight_ballots(threshold: float, candidate: Candidate, ballots: list[Ballot]):
    if not candidate.party_affiliation == "IND":
        return

    print(f"{str(candidate.votes - threshold)} votes are now transferred.")

    for ballot in ballots:
        if ballot.exhausted():
            continue

        if ballot.attributed_name().startswith(candidate.name):
            ballot.reweight(candidate.votes, threshold)


def _award_quotas(threshold: float, candidates: list[Candidate], ballots: list[Ballot], achieved_quota: list[Candidate]):
    awarded_quota = False
    for candidate in candidates:
        if candidate.votes >= threshold:
            if candidate not in achieved_quota:
                achieved_quota.append(candidate)

                awarded_quota = True
                print(f"{candidate.name} has been elected with {candidate.votes} / {threshold} votes.")

                _reweight_ballots(threshold, candidate, ballots)
    
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
            print("A tie has to be broken between: " + str(Candidate.names_in_list(lowest_scorers, False, True)))
            eliminated_candidate = _break_tie(lowest_scorers, round, rounds, num_candidates)
    
    print(eliminated_candidate.name + " has been eliminated with " + str(eliminated_candidate.votes) + " votes.")
    return eliminated_candidate


def _transfer_ballots(ballots: list[Ballot], candidates: list[Candidate], achieved_quota: list[Candidate], eliminated: list[Candidate]):
    for ballot in ballots:
        ballot.transfer(candidates, achieved_quota, eliminated)


def run(total_seats: int, ballots: list[Ballot], candidates: list[Candidate]):
    total_votes = len(ballots)
    threshold = total_votes / total_seats
    print("Threshold to achieve quota: " + str(threshold))

    achieved_quota: list[Candidate] = []
    eliminated: list[Candidate] = []

    round = 0
    rounds: list[list[Candidate]] = []
    while len(achieved_quota) + len(eliminated) < len(candidates):
        print("\nRound " + str(round))
        _tally_candidate_votes(candidates, ballots, achieved_quota)
        print(Candidate.names_in_list(candidates, False, True))
        _save_round(rounds, candidates)
        
        awarded_quota = _award_quotas(threshold, candidates, ballots, achieved_quota)
        if not awarded_quota:
            in_contention = [candidate for candidate in candidates if candidate not in achieved_quota and candidate not in eliminated]
            eliminated.append(_eliminate_lowest_scorer(in_contention, round, rounds, len(candidates)))
        
        _transfer_ballots(ballots, candidates, achieved_quota, eliminated)

        round += 1
    else:
        _tally_candidate_votes(candidates, ballots, achieved_quota)
    
    return achieved_quota, eliminated


def main():
    pass


if __name__ == "__main__":
    main()