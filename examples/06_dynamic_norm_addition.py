from spade_norms.norms.norm_enums import NormType, NormativeActionStatus
from spade_norms.actions.normative_action import NormativeAction
from spade_norms.engines.norm_engine import NormativeEngine 
from spade_norms.spade_norms import NormativeMixin
from spade.behaviour import CyclicBehaviour
from spade_norms.norms.norm import Norm
from spade.agent import Agent
from enum import Enum
import time

class Domain(Enum):
    NUMBERS=1

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
        no_three_mul_nums = Norm('no-three-multipliers-nums', NormType.PROHIBITION, no_three_multipliers_cond_fn, inviolable=False, domain=Domain.NUMBERS)
        if self.agent.counter > 6 and not normative_engine.contains_norm(no_three_mul_nums):
            normative_engine.add_norm(no_three_mul_nums)
            print('no_three_mul_nums norm added')

class PrinterAgent(NormativeMixin, Agent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def setup(self):
        self.add_behaviour(CyclicPrintBehaviour())

if __name__ == '__main__':
    '''
    Example with dynamic norm addition to normative engine
    '''
    #1 create normative action
    act = NormativeAction('print', cyclic_print, Domain.NUMBERS)

    #2 create norm
    no_even_nums = Norm('no-even-nums', NormType.PROHIBITION, no_even_nums_cond_fn, inviolable=False, domain=Domain.NUMBERS)
    no_three_mul_nums = Norm('no-three-multipliers-nums', NormType.PROHIBITION, no_three_multipliers_cond_fn, inviolable=False, domain=Domain.NUMBERS)

    #3 create normative engine
    normative_engine = NormativeEngine()

    #4 create agent with user, apssword and noramtive engine
    ag = PrinterAgent("migarbo1_printer@gtirouter.dsic.upv.es", "test")
    ag.normative.set_normative_engine(normative_engine)
    
    #5 add action to agent
    ag.normative.add_action(act)

    #6 start agent
    ag.start()
    time.sleep(3)
    i = 0
    while ag.is_alive():
        try:
            time.sleep(1)
            if i > 3 and not normative_engine.contains_norm(no_even_nums):
                normative_engine.add_norm(no_even_nums)
                print('no_even_nums norm added')
            #if i > 6 and not normative_engine.contains_norm(no_three_mul_nums):
            #    normative_engine.add_norm(no_three_mul_nums)
            #    print('no_three_mul_nums norm added')
            i += 1
            print(normative_engine.norm_db)
        except KeyboardInterrupt:
            ag.stop()            
            break