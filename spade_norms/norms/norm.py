from enum import Enum
from norm_enums import NormType

#it1: only norms that are always active and cannot be violated

class Norm():
    def __init__(self ,name: str, norm_type: NormType, condition_fn: function, activation_fn: function = None, 
                is_active:bool = True, reward: float = 1.0, penalty: float = -1.0, role: Enum = None, 
                domain: Enum = None, affected_actions: list = [], mandatory: bool = False):
        self.name = name
        self.norm_type = norm_type
        self.condition_fn = condition_fn
        #self.activation_fn = activation_fn
        #self.is_active = is_active
        self.reward = reward
        self.penalty = penalty
        self.role = role
        self.domain = domain
        #self.affected_actions = affected_actions
        #self.mandatory = mandatory
