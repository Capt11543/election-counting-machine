class Ballot:
    def __init__(self, order: list[int]):
        self.position = 0
        self.value = 1
        self.order = order
    

    def exhausted(self):
        return self.position == -1
    
    
    def attributed_name(self):
        if self.exhausted():
            return None
        
        return self.order[self.position]


    def _check_name(self, delta_pos: int):
        return self.order[self.position + delta_pos]


    def transfer(self, achieved_quorum: dict[str, float], eliminated: list[str]):
        delta_pos = 0

        while (self._check_name(delta_pos) in achieved_quorum and "(IND)" in self._check_name(delta_pos)) or self._check_name(delta_pos) in eliminated:
            delta_pos += 1

            if self.position + delta_pos >= len(self.order):
                self.position = -1
                break
        
        self.position += delta_pos




