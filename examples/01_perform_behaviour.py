from spade_norms.actions.normative_action import NormativeAction
from spade_norms.spade_norms import NormativeMixin
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import time

def cyclic_print(agent):
    print('count: {}'.format(agent.counter))
    agent.counter += 1
    time.sleep(2)

class CyclicPrintBehaviour(CyclicBehaviour):
    async def run(self):
        self.agent.normative.perform('print')

class PrinterAgent(NormativeMixin, Agent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def setup(self):
        self.add_behaviour(CyclicPrintBehaviour())

if __name__ == '__main__':
    '''
    Simple example of how to use the perform directive in normative agents
    '''
    act = NormativeAction('print', cyclic_print)
    ag = PrinterAgent("migarbo1_printer@gtirouter.dsic.upv.es", "test") 
    ag.normative.add_action(act)
    ag.start()
    time.sleep(3)
    while ag.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            ag.stop()            
            break