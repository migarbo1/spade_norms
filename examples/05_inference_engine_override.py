from spade_norms.engines.reasoning_engine import NormativeReasoningEngine
from spade_norms.norms.norm_enums import NormType, NormativeActionStatus
from spade_norms.actions.normative_action import NormativeAction
from spade_norms.engines.norm_engine import NormativeEngine
from spade_norms.norms.normative_response import NormativeResponse 
from spade_norms.spade_norms import NormativeMixin
from spade.behaviour import CyclicBehaviour
from spade_norms.norms.norm import Norm
from spade.agent import Agent
from enum import Enum
import time

# create class wich inherits from NormativeReasoningEngine and override inference method.
class RecklessReasoningEngine(NormativeReasoningEngine):
    def inference(self, norm_response: NormativeResponse):
        '''
        this method overrides the previous inference behaviour and returns exactly the oposite.
        '''
        if norm_response.responseType == NormativeActionStatus.NOT_REGULATED or norm_response.responseType == NormativeActionStatus.ALLOWED:
            return False
        
        if norm_response.responseType == NormativeActionStatus.INVIOLABLE:
            return True

        if norm_response.responseType == NormativeActionStatus.FORBIDDEN:
            return True

class Domain(Enum):
    NUMBERS=1

class Role(Enum):
    EVEN_HATER = 0
    THREE_HATER = 1

def cyclic_print(agent):
    print('count: {}'.format(agent.counter))
    time.sleep(2)

def no_even_nums_cond_fn(agent):
    if agent.counter % 2 == 0: 
        return NormativeActionStatus.FORBIDDEN
    
    return NormativeActionStatus.ALLOWED

def no_three_multipliers_cond_fn(agent):
    if agent.counter % 3 == 0: 
        return NormativeActionStatus.FORBIDDEN
    
    return NormativeActionStatus.ALLOWED

class CyclicPrintBehaviour(CyclicBehaviour):
    async def run(self):
        self.agent.normative.perform('print')
        self.agent.counter += 1

class PrinterAgent(NormativeMixin, Agent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def setup(self):
        self.add_behaviour(CyclicPrintBehaviour())

if __name__ == '__main__':
    '''
    Example of how to override norm compliance decision making process.
    '''
    #1 create normative action
    act = NormativeAction('print', cyclic_print, Domain.NUMBERS)

    #2 create norm
    no_even_nums = Norm('no-even-nums', NormType.PROHIBITION, no_even_nums_cond_fn, inviolable=False, domain=Domain.NUMBERS, roles=[Role.EVEN_HATER])
    no_prime_nums = Norm('no-three-multipliers-nums', NormType.PROHIBITION, no_three_multipliers_cond_fn, inviolable=False, domain=Domain.NUMBERS, roles=[Role.EVEN_HATER, Role.THREE_HATER])

    #3 create normative engine
    normative_engine = NormativeEngine(norm_list= [no_even_nums, no_prime_nums])

    #4 create custom reasoning engine
    reckless_reasoning_engine = RecklessReasoningEngine()

    #4 create agent with user, apssword and noramtive engine
    ag = PrinterAgent("migarbo1_printer@gtirouter.dsic.upv.es", "test",
        role = Role.THREE_HATER, 
        reasoning_engine = reckless_reasoning_engine, 
        normative_engine = normative_engine,
        actions = [act])

    #6 start agent
    ag.start()
    time.sleep(3)
    while ag.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            ag.stop()            
            break