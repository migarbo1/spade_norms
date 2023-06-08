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
        time.sleep(2)
        self.agent.counter += 1
        no_three_mul_nums = Norm('no-three-multipliers-nums', NormType.PROHIBITION, no_three_multipliers_cond_fn, inviolable=False, domain=Domain.NUMBERS)
        if self.agent.counter > 6 and not self.agent.normative.contains_concern(no_three_mul_nums) and not self.agent.concern_removed:
            #The agent updates its own concerns and does not modify the normative engine, so this norm it's only for itself
            self.agent.normative.add_concern(no_three_mul_nums)
            print('CONCERN ADDED: no_three_mul_nums')
        if self.agent.counter > 15 and self.agent.normative.contains_concern(no_three_mul_nums) and not self.agent.concern_removed:
            self.agent.normative.remove_concern(no_three_mul_nums)
            self.agent.concern_removed = True
            print('CONCERN REMOVED: no_three_mul_nums')


class PrinterAgent(NormativeMixin, Agent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.concern_removed = False

    async def setup(self):
        self.add_behaviour(CyclicPrintBehaviour())

if __name__ == '__main__':
    '''
    This example how norms and concerns can be added and deleted from an agent dynamically
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
    removed = False
    while ag.is_alive():
        try:
            time.sleep(0.5)
            if ag.counter >= 3 and not normative_engine.contains_norm(no_even_nums) and not removed:
                normative_engine.add_norm(no_even_nums)
                print('NORM ADDED: no_even_nums')
            if ag.counter >= 10 and normative_engine.contains_norm(no_even_nums) and not removed:
                normative_engine.remove_norm(no_even_nums)
                removed = True
                print('NORM REMOVED: no_even_nums')
        except KeyboardInterrupt:
            ag.stop()            
            break