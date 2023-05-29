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
        '''
        Adds a list of norms to the normative database. Norms are indexed by domain, 
        if no domain is provided on the actions, a base one is assumed. Althoug is highly recommended to provide it. 
        '''
        for norm in norms:
            self.add_norm(norm)
    
    def add_norm(self, norm: Norm):
        '''
        Adds a single norm to the normative database. Norms are indexed by domain, 
        if no domain is provided on the actions, a base one is assumed. Althoug is highly recommended to provide it. 
        '''
        domain = norm.domain if norm.domain != None else 0
        if self.norm_db.get(domain, None) == None:
            self.norm_db[domain] = []
        self.norm_db[domain].append(norm)

    def check_legislation(self, action: NormativeAction, agent: Agent) -> NormativeResponse:
        '''
        This method checks the current norm database and for a given action returns if it is allowed or not in the form of a `NormativeResponse` object
        '''
        domain = action.domain if action.domain != None else 0
        normative_response = NormativeResponse(action=action)
        if self.norm_db.get(domain, None) == None:
            normative_response.responseType = NormativeActionStatus.NOT_REGULATED
            return normative_response
        
        related_norms = self.norm_db[domain]
        related_norms = self.filter_norms_by_role(related_norms, agent.role)
        for norm in related_norms:
            cond_result = norm.condition_fn(agent)
            assert isinstance(cond_result, NormativeActionStatus)
            
            if cond_result == NormativeActionStatus.FORBIDDEN:
                normative_response.add_forbidding_norm(norm)

            if cond_result == NormativeActionStatus.ALLOWED:
                normative_response.add_allowing_norm(norm)
        
        return normative_response

    def filter_norms_by_role(norm_list, role) -> bool: 
        '''
        Receives a `list of norms` and a `role`. 
        Returns the sublist of norms that have the given `role` inside the affected roles list 
        '''
        relevant_norms_for_role = []
        for norm in norm_list:
            if norm.roles == None or role in norm.roles:
                relevant_norms_for_role.append(norm)
        return relevant_norms_for_role