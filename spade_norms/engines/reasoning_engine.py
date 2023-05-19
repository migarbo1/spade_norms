from ..norms.normative_response import NormativeResponse
from ..norms.norm_enums import NormativeActionStatus
import random

class NormativeReasoningEngine():
    def __init__(self):
        pass

    def inference(self, norm_response: NormativeResponse):
        '''
        This function allows the agent to reason about whether to perform an action or not.
        You can override this method to change this behaviour.
        '''
        if norm_response.responseType == NormativeActionStatus.NOT_REGULATED or norm_response.responseType == NormativeActionStatus.ALLOWED:
            return True
        
        if norm_response.responseType == NormativeActionStatus.INVIOLABLE:
            return False
        
        if norm_response.responseType == NormativeActionStatus.MIXED:
            return abs(norm_response.total_reward) > abs(norm_response.total_penalty) or random.random() > 0.65

        if norm_response.responseType == NormativeActionStatus.FORBIDDEN:
            return random.random() > 0.8