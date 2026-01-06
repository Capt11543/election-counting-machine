from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ballot import Ballot


class Candidate:
    def get_from_list(name: str, list: list[Candidate]):
        if name is None:
            return None

        return next((candidate for candidate in list if name.startswith(candidate.name)), None)
    

    def find_party_affiliation(name: str, parties_are_candidates=False, default="IND") -> str:
        if parties_are_candidates:
            return name
        
        if "(" in name and ")" in name:
            return name[(name.index("(") + 1):name.index(")")]
        return default
    

    def strip_party_affiliation(name: str):
        result = ""

        try:
            result = name[:name.index("(") - 1]
        except ValueError:
            result = name
        finally:
            return result
    

    def names_in_list(candidates: list[Candidate], include_party_affiliation = False, include_score = False, preference_level = -1):
        if include_score:
            return {candidate.name + ((" (" + candidate.party_affiliation + ")") if include_party_affiliation else ""): candidate.preferences[preference_level] if preference_level > -1 else candidate.votes for candidate in candidates}
        else:
            return [candidate.name + ((" (" + candidate.party_affiliation + ")") if include_party_affiliation else "") for candidate in candidates]

    
    def __init__(self, name: str, party_affiliation: str, preferences: list[int]):
        self.name = name
        self.votes = 0.0
        self.party_affiliation = party_affiliation
        self.preferences = preferences
    

    def tally_votes(self, ballots: list[Ballot], should_freeze_score: bool):
        if should_freeze_score:
            return
        
        self.votes = 0.0
        for ballot in ballots:
            if not ballot.exhausted():
                if ballot.attributed_name().startswith(self.name):
                    self.votes += ballot.value
    
    
    def __repr__(self):
        # print JSON formatting of the candidate (name, votes, party_affiliation, preferences)
        return f'{{"name": "{self.name}", "votes": {self.votes}, "party_affiliation": "{self.party_affiliation}", "preferences": {self.preferences}}}'