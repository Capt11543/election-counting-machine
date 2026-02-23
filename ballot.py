from candidate import Candidate
from decimal import *
import logger as Logger


class Ballot:
    def __init__(self, order: list[str]):
        self.position = 0
        self.value = Decimal(1.00000)
        self.order = order
    

    def exhausted(self):
        return self.position == -1
    
    
    def attributed_name(self, delta_pos = 0) -> str | None:
        if self.exhausted():
            return None
        
        if self.position + delta_pos >= len(self.order):
            return None
        
        return self.order[self.position + delta_pos]


    def _should_transfer(check_candidate: Candidate, achieved_quota: list[Candidate], eliminated: list[Candidate], is_special_election: bool):
        if check_candidate is None:
            return False
        
        if check_candidate in achieved_quota:
            if is_special_election or check_candidate.party_affiliation == "IND":
                return True
        
        if check_candidate in eliminated:
            return True
        
        return False
    
    
    def transfer(self, candidates: list[Candidate], achieved_quota: list[Candidate], eliminated: list[Candidate], is_special_election: bool, delta_pos = 0):
        check_candidate: Candidate | None = Candidate.get_from_list(self.attributed_name(delta_pos), candidates)
        if Ballot._should_transfer(check_candidate, achieved_quota, eliminated, is_special_election):
            self.transfer(candidates, achieved_quota, eliminated, is_special_election, delta_pos + 1)
        else:
            self.position += delta_pos
            if self.position >= len(self.order):
                self.position = -1
                return
            
            if delta_pos > 0:
                Logger.log_and_print(f"{str(self.value)} votes to {self.attributed_name()}.")
    

    def reweight(self, votes: int, threshold: float):
        transfer_value = Decimal((votes - threshold) / votes)
        self.value *= transfer_value
        self.value = self.value.quantize(Decimal('1.00000'))


    
    def __repr__(self):
        # print JSON formatting of the ballot (position, value, order)
        return f'{{"position": {self.position}, "value": {self.value}, "order": {self.order}}}'
