from spade_norms.norms.norm_enums import NormType, NormativeActionStatus
from spade_norms.actions.normative_action import NormativeAction
from spade_norms.engines.norm_engine import NormativeEngine 
from spade_norms.spade_norms import NormativeMixin
from spade.behaviour import CyclicBehaviour
from spade_norms.norms.norm import Norm
from spade.agent import Agent
from enum import Enum
import threading
import spade
import time

class Domain(Enum):
    NUMBERS=1

async def cyclic_print(agent):
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
        await self.agent.normative.perform('print')
        time.sleep(2)
        self.agent.counter += 1
        no_three_mul_nums = Norm('no-three-multipliers-nums', NormType.PROHIBITION, no_three_multipliers_cond_fn, inviolable=False, domain=Domain.NUMBERS)
        if self.agent.counter > 6 and not self.agent.normative.contains_concern(no_three_mul_nums):
            #The agent updates its own concerns and does not modify the normative engine, so this norm it's only for itself
            no_three_mul_nums = Norm('no-three-multipliers-nums', NormType.PROHIBITION, no_three_multipliers_cond_fn, inviolable=False, domain=Domain.NUMBERS)
            self.agent.normative.add_concern(no_three_mul_nums)
            print('CONCERN ADDED: no_three_mul_nums')

class PrinterAgent(NormativeMixin, Agent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def setup(self):
        self.add_behaviour(CyclicPrintBehaviour())

def loop(ag, normative_engine, no_even_nums):
    time.sleep(3)
    while ag.is_alive():
        try:
            time.sleep(1)
            if ag.counter >= 3 and not normative_engine.contains_norm(no_even_nums):
                normative_engine.add_norm(no_even_nums)
                print('NORM ADDED: no_even_nums')
        except KeyboardInterrupt:
            ag.stop()            
            break

async def main():
    '''
    This example follows the same structure as 06_dynamic_norm_addition. But in this case, we add a norm to the agent (concern) so this will only affect its behaviour, not the behaviour of all the agents.
    '''
    #1 create normative action
    act = NormativeAction('print', cyclic_print, Domain.NUMBERS)

    #2 create norm
    no_even_nums = Norm('no-even-nums', NormType.PROHIBITION, no_even_nums_cond_fn, inviolable=False, domain=Domain.NUMBERS)

    #3 create normative engine
    normative_engine = NormativeEngine()

    #4 create agent with user, apssword and noramtive engine
    ag = PrinterAgent("printer@your.xmpp.server", "test")
    ag.normative.set_normative_engine(normative_engine)
    
    #5 add action to agent
    ag.normative.add_action(act)

    t = threading.Thread(target=loop, args=(ag, normative_engine, no_even_nums))
    t.start()

    #6 start agent
    await ag.start()

if __name__ == '__main__':
    spade.run(main())