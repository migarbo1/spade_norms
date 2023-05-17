from enum import Enum

class NormativeAction():
    def __init__(self, name: str, action_fn: function, domain: Enum = None):
        self.name = name
        self.action_fn = action_fn
        self.domain = domain

    