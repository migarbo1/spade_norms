from .norm_enums import NormativeActionStatus
from .norm import Norm

class NormativeResponse():
    def __init__(self, responseType: NormativeActionStatus = None, norms_allowing: list = None, norms_forbidding : list = None
                , total_reward:float = 0.0, total_penalty: float = 0.0):
        self.responseType = responseType
        self.norms_allowing = norms_allowing if norms_allowing != None else [] 
        self.norms_forbidding = norms_forbidding if norms_forbidding != None else [] 
        self.total_reward = total_reward
        self.total_penalty = total_penalty

    def add_allowing_norm(self, norm: Norm):
        '''
        Adds a new norm to the response list, updates rewards and computes the response type enum.
        - if no norm has been processed or current status is ALLOWED, status will be ALLOWED.
        - if there has been at least one norm violated, then status will be MIXED
        - if there has been a forbidden state for an INVIOLABLE norm, status will remain the same.
        '''
        self.norms_allowing.append(norm)
        self.total_reward += norm.reward

        if self.responseType == None or self.responseType == NormativeActionStatus.ALLOWED or self.responseType == NormativeActionStatus.NOT_REGULATED:
            self.responseType = NormativeActionStatus.ALLOWED

        elif self.responseType == NormativeActionStatus.MIXED or self.responseType == NormativeActionStatus.FORBIDDEN:
            self.responseType = NormativeActionStatus.MIXED
        else:
            self.responseType = NormativeActionStatus.INVIOLABLE

    def add_forbidding_norm(self, norm: Norm):
        '''
        Adds a new norm to the response list and computes the response type enum.
        - if no norm has been processed or current status is FORBIDDEN, status will be FORBIDDEN.
        - if there has been at least one norm allowed, then status will be MIXED
        - if there has been a forbidden state for an inviolable norm, status will remain the same.
        '''
        self.norms_forbidding.append(norm)
        self.total_penalty += norm.penalty

        if norm.inviolable:
            self.responseType = NormativeActionStatus.INVIOLABLE

        if self.responseType == None or self.responseType == NormativeActionStatus.FORBIDDEN or self.responseType == NormativeActionStatus.NOT_REGULATED:
            self.responseType = NormativeActionStatus.FORBIDDEN
            
        elif self.responseType == NormativeActionStatus.MIXED or self.responseType == NormativeActionStatus.ALLOWED:
            self.responseType = NormativeActionStatus.MIXED

    def __str__(self):
        return '{' +  '\tresponse type: {},\n\tnorms_allow: {},\n\tnorms_forbidding: {},\n\ttotal_reward: {},\n\ttotal_penalty: {}'.format(self.responseType, self.norms_allowing, self.norms_forbidding, self.total_reward, self.total_penalty)  + '}'