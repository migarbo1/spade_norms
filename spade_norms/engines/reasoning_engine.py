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
            total_appraisal = 1

            for norm in norm_response.norms_forbidding:
                # get normalized value weights taking into consideration both promoting and demoting values
                value_weights = agent.normative.get_averaged_values(norm.promoting_values + norm.demoting_values)

                # accumulate demoting value weights (promoting = 1-demoting, thus is implicit)
                appraisal = 0
                for dv in  norm.demoting_values:
                    appraisal += value_weights[dv] 

                total_appraisal *= appraisal # if appraisal == 1 means that it is really alligned with values. So we decide not to perform the action

            # select action based on major probability density
            # higher value promotion means higher normative compliance
            print('appraisal:', appraisal)
            return random.random() <= appraisal
            