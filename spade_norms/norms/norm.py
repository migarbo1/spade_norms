from enum import Enum
from .norm_enums import NormType, NormIssuer
from typing import Callable

#it1: only norms that are always active and cannot be violated. we also asume only personal norms. Roles are not available.

class Norm():
    def __init__(self ,name: str, norm_type: NormType, condition_fn: Callable, activation_fn: Callable = None, 
                is_active: bool = True, reward: float = 1.0, penalty: float = -1.0, role: Enum = None, 
                domain: Enum = None, affected_actions: list = [], inviolable: bool = True, 
                issuer: NormIssuer = None):
        self.name = name
        self.norm_type = norm_type
        self.condition_fn = condition_fn
        #self.activation_fn = activation_fn
        #self.is_active = is_active
        self.reward = reward
        self.penalty = penalty
        #self.role = role
        self.domain = domain
        #self.affected_actions = affected_actions
        self.inviolable = inviolable
        self.issuer = issuer

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Norm) and self.name == other.name and self.norm_type == other.norm_type