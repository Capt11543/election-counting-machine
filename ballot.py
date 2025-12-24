from candidate import Candidate


class Ballot:
    def __init__(self, order: list[int]):
        self.position = 0
        self.value = 1
        self.order = order
    

    def exhausted(self):
        return self.position == -1
    
    
    def attributed_name(self, delta_pos = 0) -> str | None:
        if self.exhausted():
            return None
        
        if self.position + delta_pos >= len(self.order):
            return None
        
        return self.order[self.position + delta_pos]


    def _should_transfer(check_candidate: Candidate, achieved_quota: list[Candidate], eliminated: list[Candidate]):
        if check_candidate is None:
            return False
        
        if check_candidate in achieved_quota:
            if check_candidate.party_affiliation == "IND":
                return True
        
        if check_candidate in eliminated:
            return True
        
        return False
    
    
    def transfer(self, candidates: list[Candidate], achieved_quota: list[Candidate], eliminated: list[Candidate], delta_pos = 0):
        check_candidate: Candidate | None = Candidate.get_from_list(self.attributed_name(delta_pos), candidates)
        if Ballot._should_transfer(check_candidate, achieved_quota, eliminated):
            self.transfer(candidates, achieved_quota, eliminated, delta_pos + 1)
        else:
            self.position += delta_pos
            if self.position >= len(self.order):
                self.position = -1
    

    def reweight(self, votes: int, threshold: float):
        transfer_value = (votes - threshold) / votes
        self.value *= transfer_value

    
    def __repr__(self):
        # print JSON formatting of the ballot (position, value, order)
        return f'{{"position": {self.position}, "value": {self.value}, "order": {self.order}}}'
