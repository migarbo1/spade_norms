''''
This class will handle the norm activation, checking periodically (parameter) the activation condition of all norms
and setting them active or not.
User can deactivate this automatic update by 
'''
from ..actions.normative_action import NormativeAction 
from ..norms.normative_response import NormativeResponse
from ..norms.norm_enums import *
from ..norms.norm import Norm
from spade.agent import Agent

class NormativeEngine():
    def __init__(self, norm: Norm = None, norm_list: list = None):
        self.norm_db = {}
        #self.active_norms = {}
        if norm_list != None:
            self.add_norms(norm_list)
        if norm != None:
            self.add_norm(norm)

    def add_norms(self, norms: list):
        for norm in norms:
            self.add_norm(norm)
    
    def add_norm(self, norm: Norm):
        domain = norm.domain if norm.domain != None else 0
        if self.norm_db.get(domain, None) == None:
            self.norm_db[domain] = []
        self.norm_db[domain].append(norm)

    def check_legislation(self, action: NormativeAction, agent: Agent) -> NormativeResponse:
        domain = action.domain if action.domain != None else 0
        normative_response = NormativeResponse()
        if self.norm_db.get(domain, None) == None:
            normative_response.responseType = NormativeActionStatus.NOT_REGULATED
            return normative_response
        
        related_norms = self.norm_db[domain]
        for norm in related_norms:
            forbidden = norm.condition_fn(agent)
            if forbidden:
                normative_response.add_forbidding_norm(norm)
            else:
                normative_response.add_allowing_norm(norm)
        
        return normative_response

        

