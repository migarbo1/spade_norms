from spade_norms.engines.reasoning_engine import ValueAwareNormativeReasoningEngine
from spade_norms.norms.norm_enums import NormType, NormativeActionStatus
from spade_norms.actions.normative_action import NormativeAction
from spade_norms.engines.norm_engine import NormativeEngine
from spade_norms.norms.normative_response import NormativeResponse
from spade_norms.spade_norms import NormativeMixin
from spade.behaviour import CyclicBehaviour
from spade_norms.norms.norm import Norm
from spade.agent import Agent
from enum import Enum
import asyncio
import spade


class DummyValues(Enum):
    PRO_EVEN = 0
    PRO_ODD = 1
    PRO_PRIME = 2


class Domain(Enum):
    NUMBERS = 1


async def cyclic_print(agent):
    print("count: {}".format(agent.counter))


def no_even_nums_cond_fn(agent):
    if agent.counter % 2 == 0:
        return NormativeActionStatus.FORBIDDEN

    return NormativeActionStatus.ALLOWED


def only_primes_cond_fn(agent):
    if agent.counter > 7 and (agent.counter % 2 == 0 or agent.counter % 3 == 0 or agent.counter % 5 == 0 or agent.counter % 7 == 0):
        return NormativeActionStatus.FORBIDDEN

    return NormativeActionStatus.ALLOWED


class CyclicPrintBehaviour(CyclicBehaviour):
    async def run(self):
        performed, _, _ = await self.agent.normative.perform("print")
        await asyncio.sleep(2)
        self.agent.counter += 1


class PrinterAgent(NormativeMixin, Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.will = 0.5

    async def setup(self):
        self.add_behaviour(CyclicPrintBehaviour())


async def main():
    """
    Example of how value aware normative decission process works.
    System computes how much a norm promotes/demotes a value.
    Based on that stablishes a probability of breaking the norm.
    Feel free to test different combinations of values and weights to see how the behaviour changes.
    """
    # 1 create normative action
    act = NormativeAction("print", cyclic_print, Domain.NUMBERS)

    # 2 create norm
    no_even_nums = Norm(
        "no-even-nums",
        NormType.PROHIBITION,
        no_even_nums_cond_fn,
        inviolable=False,
        domain=Domain.NUMBERS,
        promoting_values=[
            DummyValues.PRO_ODD.name,
            DummyValues.PRO_PRIME.name
        ],
        demoting_values=[
            DummyValues.PRO_EVEN.name
        ]
    )

    only_primes = Norm(
        "only-primes-nums",
        NormType.PROHIBITION,
        only_primes_cond_fn,
        inviolable=False,
        domain=Domain.NUMBERS,
        promoting_values=[
            DummyValues.PRO_PRIME.name
        ],
        demoting_values=[
            DummyValues.PRO_EVEN.name,
            DummyValues.PRO_ODD.name,
        ]
    )

    # 3 create normative engine
    normative_engine = NormativeEngine(norm_list=[no_even_nums, only_primes])

    # 4 create custom reasoning engine
    advanced_reasoning_engine = ValueAwareNormativeReasoningEngine()

    # 5 create agent with user, apssword and noramtive engine
    ag = PrinterAgent(
        "printer@your.xmpp.server",
        "test",
        reasoning_engine=advanced_reasoning_engine,
        normative_engine=normative_engine,
        actions=[act],
        values={
            DummyValues.PRO_EVEN.name: 0,
            DummyValues.PRO_ODD.name: 1,
            DummyValues.PRO_PRIME.name: 1
        }
    )

    # 6 start agent
    await ag.start()


if __name__ == "__main__":
    spade.run(main())
