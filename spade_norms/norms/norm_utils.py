from spade.agent import Agent 
from .norm import Norm
from enum import Enum

def add_single(norm_or_concern_db: dict, norm_or_concern: Norm) -> dict:
    '''
        Adds a single norm or concern to the input database. Norms are indexed by domain, 
        if no domain is provided, a base one is assumed. Althoug is highly recommended to provide it. 
    '''
    domain = norm_or_concern.domain if norm_or_concern.domain != None else 0
    if norm_or_concern_db.get(domain, None) == None:
        norm_or_concern_db[domain] = []
    norm_or_concern_db[domain].append(norm_or_concern)
    return norm_or_concern_db

def add_multiple(norm_or_concern_db: dict, norm_or_concern_list: list) -> dict:
    '''
        Adds a list of norms or concerns to the normative or concerns database. They are indexed by domain, 
        if no domain is provided, a base one is assumed. Althoug is highly recommended to provide it. 
    '''
    for concern in norm_or_concern_list:
        norm_or_concern_db = add_single(norm_or_concern_db, concern)
    return norm_or_concern_db

def contains(norm_or_concern_db: dict, norm_or_concern: Norm) -> bool:
    '''
        Searches in the given db for a norm. Returns `True` if found, `Else` otherwise
    '''
    for domain in norm_or_concern_db.keys():
        for local_concern in norm_or_concern_db[domain]:
            if norm_or_concern == local_concern:
                return True
    return False

#TODO
def remove(norm_or_concern_db: dict, norm_or_concern: Norm) -> dict:
    '''
        Removes a norm or a concern from the given database.
    '''
    domain_restrictions = norm_or_concern_db.get(norm_or_concern.domain, [])
    if domain_restrictions != []:
        for idx, restriction in enumerate(domain_restrictions):
            if restriction == norm_or_concern:
                norm_or_concern_db[norm_or_concern.domain].pop(idx)
                break
    return norm_or_concern_db

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

def join_norms_and_concerns(norms: list, agent: Agent, domain:Enum) -> list:
    '''
    Receives as input the organization norms and the agent concerns
    Returns the concatenation of both lists 
    '''
    return norms + agent.normative.concerns.get(domain, [])