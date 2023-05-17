from spade_norms.actions.normative_action import NormativeAction
from spade_norms.spade_norms import NormativeMixin
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import time

def cyclic_print():
    #print('count: {}'.format(self.agent.counter))
    #self.agent.counter += 1
    print('this is a test')
    time.sleep(2)

class CyclicPrintBehaviour(CyclicBehaviour):
    async def run(self):
        self.agent.normative.perform('print')

class PrinterAgent(NormativeMixin, Agent):

    async def setup(self):
        self.add_behaviour(CyclicPrintBehaviour())

if __name__ == '__main__':
    act = NormativeAction('print', cyclic_print)
    ag = PrinterAgent("migarbo1_printer@gtirouter.dsic.upv.es", "test") 
    ag.normative.add_action(act)
    ag.start()