from ..norms.normative_response import NormativeResponse
from ..norms.norm_enums import NormativeActionStatus
from spade.agent import Agent
import random

class NormativeReasoningEngine():
    def __init__(self):
        pass

    def inference(self, agent:Agent, norm_response: NormativeResponse):
        '''
        This function allows the agent to reason about whether to perform an action or not.
        You can override this method to change this behaviour.
        '''
        if norm_response.response_type == NormativeActionStatus.NOT_REGULATED or norm_response.response_type == NormativeActionStatus.ALLOWED:
            return True
        
        if norm_response.response_type == NormativeActionStatus.INVIOLABLE:
            return False

        if norm_response.response_type == NormativeActionStatus.FORBIDDEN:
            return False
        

class ValueAwareNormativeReasoningEngine():
    def __init__(self):
        pass

    def inference(self, agent:Agent, norm_response: NormativeResponse):
        '''
        This function allows the agent to reason about whether to perform an action or not 
        taking into account how the applying norms affect to its values.
        '''
        if norm_response.response_type == NormativeActionStatus.NOT_REGULATED or norm_response.response_type == NormativeActionStatus.ALLOWED:
            return True
        
        if norm_response.response_type == NormativeActionStatus.INVIOLABLE:
            return False

        if norm_response.response_type == NormativeActionStatus.FORBIDDEN:
            appraisal = 0

            for norm in norm_response.norms_allowing:
                # get normalized value weights taking into consideration both promoting and demoting values
                value_weights = agent.get_averaged_values(norm.promoting_values + norm.demoting_values)

                # accumulate promoting value weights
                for pv in  norm.promoting_values:
                    appraisal += value_weights[pv] 

            # select action based on major probability density
            # higher value promotion means higher normative compliance
            return random.random() > appraisal
            