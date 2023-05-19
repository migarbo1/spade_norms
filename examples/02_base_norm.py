from spade_norms.actions.normative_action import NormativeAction
from spade_norms.engines.norm_engine import NormativeEngine 
from spade_norms.spade_norms import NormativeMixin
from spade_norms.norms.norm_enums import NormType
from spade.behaviour import CyclicBehaviour
from spade_norms.norms.norm import Norm
from spade.agent import Agent
import time

def cyclic_print(agent):
    print('count: {}'.format(agent.counter))
    time.sleep(2)

def no_even_nums_cond_fn(agent):
    return agent.counter % 2 == 0

class CyclicPrintBehaviour(CyclicBehaviour):
    async def run(self):
        self.agent.normative.perform('print', self.agent)
        self.agent.counter += 1

class PrinterAgent(NormativeMixin, Agent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def setup(self):
        self.add_behaviour(CyclicPrintBehaviour())

if __name__ == '__main__':
    #1 create normative action
    act = NormativeAction('print', cyclic_print)

    #2 create norm
    no_even_nums = Norm('no-even-nums', NormType.PROHIBITION, no_even_nums_cond_fn)

    #3 create normative engine
    normative_engine = NormativeEngine(norm = no_even_nums)

    #4 create agent with user, apssword and noramtive engine
    ag = PrinterAgent("migarbo1_printer@gtirouter.dsic.upv.es", "test")
    ag.normative.set_normative_engine(normative_engine)
    #5 add action to agent
    ag.normative.add_action(act)

    #6 start agent
    ag.start()
    time.sleep(3)
    while ag.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            ag.stop()            
            break