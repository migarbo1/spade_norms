from ..norms.normative_response import NormativeResponse
from ..norms.norm_enums import NormativeActionStatus
import random

class NormativeReasoningEngine():
    def __init__(self):
        pass

    def inference(norm_response: NormativeResponse):
        '''
        This function allows the agent to reason about whether to perform an action or not.
        You can override this method to change this behaviour.
        '''
        if norm_response.responseType == NormativeActionStatus.NOT_REGULATED or NormativeActionStatus.ALLOWED:
            print('Doing action because is not regulated or allowed')
            return True
        
        if norm_response.responseType == NormativeActionStatus.INVIOLABLE:
            print('Not doing action because is inviolable')
            return False
        
        if norm_response.responseType == NormativeActionStatus.MIXED:
            print('Mixed responses, doing action only if benefit is greater than penalty')
            return norm_response.total_reward > norm_response.total_penalty

        if norm_response.responseType == NormativeActionStatus.FORBIDDEN:
            print('Forbiden action, doing only 1 out of 10 times')
            return random.random() > 0.9