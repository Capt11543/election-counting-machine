from candidate import Candidate


def lowest_scorer(candidates: list[Candidate], preference_level = -1):
    least_votes: list[Candidate] = []
    least_votes_count = sum(candidate.votes for candidate in candidates)

    for candidate in candidates:
        compare_num = candidate.votes if preference_level < 0 else candidate.preferences[preference_level]
    
        if compare_num < least_votes_count:
            least_votes = [candidate]
            least_votes_count = candidate.votes
        elif compare_num == least_votes_count:
            least_votes.append(candidate)
        
    return least_votes


def backtrack_rounds(tied: list[Candidate], round: int, rounds: list[list[Candidate]]):
    if round < 1:
        return None
    
    tied_this_round = [candidate for candidate in rounds[round - 1] if candidate in tied]
    print("Backtracking to round " + str(round - 1) + ":")
    print(Candidate.names_in_list(tied_this_round, False, True))

    lowest_scoring = lowest_scorer(tied_this_round)

    if len(lowest_scoring) == 1:
        print("Tie broken after comparing votes from round " + str(round - 1) + ".")
        return lowest_scoring[0]
    
    for candidate in tied_this_round:
        if candidate not in lowest_scoring:
            print(candidate.name + " is no longer tied.")
            tied.remove(candidate)
    
    return backtrack_rounds(tied, round - 1, rounds)


def compare_preferences(tied: list[Candidate], num_candidates: int):
    for preference in range(num_candidates):
        ordinal_num = preference + 1
        ordinal_str = str(ordinal_num) + ("st" if (ordinal_num) % 10 == 1 and not (ordinal_num) / 10 == 1 else "nd" if (ordinal_num) % 10 == 2 and not (ordinal_num) / 10 == 1 else "rd" if (ordinal_num) % 10 == 3 and not (ordinal_num) / 10 == 1 else "th")

        print("Comparing " + ordinal_str + "-choice votes...")
        lowest_scoring = lowest_scorer(tied, preference)

        if len(lowest_scoring) == 1:
            print("Tie broken after comparing " + ordinal_str + "-choice votes.")
            return lowest_scoring[0]
        
        for candidate in tied:
            if candidate not in lowest_scoring:
                print(candidate.name + " is no longer tied.")
                tied.remove(candidate)
    
    return None