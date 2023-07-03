import asyncio
import threading
from spade_norms.norms.norm_enums import NormType, NormativeActionStatus
from spade_norms.actions.normative_action import NormativeAction
from spade_norms.engines.norm_engine import NormativeEngine 
from spade_norms.spade_norms import NormativeMixin
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade_norms.norms.norm import Norm
from spade.template import Template
from spade.message import Message
from spade.agent import Agent
from enum import Enum
import spade
import time

class Domain(Enum):
    NUMBERS=1

class Role(Enum):
    SENDER = 0
    RECEIVER = 1

async def send_number(agent, behaviour, send_agent, recv_agent):
    msg = Message(to=str(recv_agent.jid), body="{}".format(send_agent.counter), metadata={"performative": "inform"})
    await behaviour.send(msg)

def only_sender_can_send(agent):
    return NormativeActionStatus.FORBIDDEN

class CyclicSendBehaviour(CyclicBehaviour):
    async def run(self):
        await self.agent.normative.perform('send', self, self.agent, self.agent.recv)
        time.sleep(2)
        self.agent.counter += 1

class CyclicRecvBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=5)
        if msg:
            print('{} received count: {}'.format(self.agent.jid, msg.body))
        time.sleep(1)

class PrinterAgent(NormativeMixin, Agent):

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.recv = None

    async def setup(self):
        template = Template(metadata={"performative": "inform"})
        self.add_behaviour(CyclicSendBehaviour())
        self.add_behaviour(CyclicRecvBehaviour(), template)

def create_agents():
    #1 create normative action
    act = NormativeAction('send', send_number, Domain.NUMBERS)

    #2 create norm
    no_rec_sending = Norm('no-even-nums', NormType.PROHIBITION, only_sender_can_send, inviolable=False, domain=Domain.NUMBERS, roles=[Role.RECEIVER])

    #3 create normative engine
    normative_engine = NormativeEngine(norm_list= [no_rec_sending])

    #4 create agent with user, apssword and noramtive engine
    ag1 = PrinterAgent("migarbo1_sender1@gtirouter.dsic.upv.es", "test", role = Role.SENDER)
    ag2 = PrinterAgent("migarbo1_receiver1@gtirouter.dsic.upv.es", "test", role = Role.RECEIVER)

    ag1.normative.set_normative_engine(normative_engine)
    ag2.normative.set_normative_engine(normative_engine)

    ag1.recv = ag2
    ag2.recv = ag1
    
    #5 add action to agent
    ag1.normative.add_action(act)
    ag2.normative.add_action(act)

    #6 start agent
    #await ag1.start()
    #await ag2.start()
    return ag1, ag2

async def launch_ag(ag):
    await ag.start()

if __name__ == '__main__':
    '''
        More complex example with multiple cyclic agents and different roles. Only sender can emit messages. Agent reports the count of the receiving message so sender will never report the count while receiver will do each time sender emits the message.
    '''
    ag1, ag2 = create_agents()
    t1 = threading.Thread(target=asyncio.run, args=(launch_ag(ag1),))
    t2 = threading.Thread(target=asyncio.run, args=(launch_ag(ag2),))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
