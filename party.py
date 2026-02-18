from __future__ import annotations

from candidate import Candidate
from decimal import *


class Party:
    def __init__(self, name: str, candidate_list: list[str]):
        self.name = name
        self.votes = Decimal(0.00000)
        self.seats = 0
        self.candidate_list = candidate_list
    

    def names_in_list(parties: list[Party], mode=0):
        match mode:
            case 0:
                return [party.name for party in parties]
            case 1:
                return {party.name: str(party.votes) for party in parties}
            case 2:
                return {party.name: party.seats for party in parties}
            case _:
                raise ValueError("Invalid mode for names_in_list. Valid modes are 0 (names only), 1 (include votes), and 2 (include seats).")
    

    def get_from_list(name: str, list: list[Party]):
        if name is None:
            return None

        return next((party for party in list if name.startswith(party.name)), None)
    

    def infer_candidate_list(self, achieved_quota: list[Candidate], eliminated: list[Candidate]):
        quota_candidates = [candidate for candidate in achieved_quota if candidate.party_affiliation == self.name]
        ordered_quota_candidates = sorted(quota_candidates, key=lambda x: x.votes, reverse=True)
        
        for candidate in ordered_quota_candidates:
            self.candidate_list.append(candidate)
        
        for candidate in reversed(eliminated):
            if candidate.party_affiliation == self.name:
                self.candidate_list.append(candidate)
    

    def tally_votes(self, achieved_quota: list[Candidate]):
        self.votes = Decimal(sum([candidate.votes for candidate in achieved_quota if candidate.party_affiliation == self.name]))
        self.votes = self.votes.quantize(Decimal('1.00000'))
    

    def get_quotient(self):
        result = self.votes / Decimal(2 * self.seats + 1)
        result = result.quantize(Decimal('1.00000'))
        return result
    

    def set_votes(self, votes: int):
        self.votes = Decimal(votes)
        self.votes = self.votes.quantize(Decimal('1.00000'))
    

    def __repr__(self):
        # print JSON formatting of the paty (name, votes, seats, candidate_list)
        return f'{{"name": "{self.name}", "votes": {self.votes}, "seats": "{self.seats}", "candidate_list": {self.candidate_list}}}'