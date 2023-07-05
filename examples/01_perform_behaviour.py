from spade_norms.actions.normative_action import NormativeAction
from spade_norms.spade_norms import NormativeMixin
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import spade
import time

async def cyclic_print(agent):
    print('count: {}'.format(agent.counter))

class CyclicPrintBehaviour(CyclicBehaviour):
    async def run(self):
        await self.agent.normative.perform('print')
        time.sleep(2)
        self.agent.counter += 1

class PrinterAgent(NormativeMixin, Agent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def setup(self):
        self.add_behaviour(CyclicPrintBehaviour())

async def main():
    '''
    Simple example of how to use the perform directive in normative agents
    '''
    act = NormativeAction('print', cyclic_print)
    ag = PrinterAgent("printer@your.xmpp.server", "test") 
    ag.normative.add_action(act)
    await ag.start()

if __name__ == '__main__':
    spade.run(main())