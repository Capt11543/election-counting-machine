from party import Party
from candidate import Candidate


def run(parties: list[Party], achieved_quota: list[Candidate], eliminated: list[Candidate], infer_candidate_lists: bool):
    elected: list[Candidate] = []
    
    for candidate in [candidate for candidate in achieved_quota if candidate.party_affiliation == "IND"]:
        elected.append(candidate)    
    
    for party in parties:
        if infer_candidate_lists:
            party.infer_candidate_list(achieved_quota, eliminated)
        
        for index in range(party.seats):
            if index >= len(party.candidate_list):
                elected.append(Candidate("VACANT", party.name, []))
            else:
                newly_elected = party.candidate_list[index]

                if infer_candidate_lists:
                    elected.append(newly_elected)
                else:
                    elected.append(Candidate(newly_elected, party.name, []))

    return elected