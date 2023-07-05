from spade_norms.norms.norm_enums import NormType, NormativeActionStatus
from spade_norms.actions.normative_action import NormativeAction
from spade_norms.engines.norm_engine import NormativeEngine
from spade_norms.spade_norms import NormativeMixin
from spade.behaviour import CyclicBehaviour
from spade_norms.norms.norm import Norm
from spade.agent import Agent
from enum import Enum
import asyncio
import spade


class Domain(Enum):
    NUMBERS = 1


async def cyclic_print(agent):
    print("count: {}".format(agent.counter))


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
        await self.agent.normative.perform("print")
        await asyncio.sleep(2)
        self.agent.counter += 1


class PrinterAgent(NormativeMixin, Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def setup(self):
        self.add_behaviour(CyclicPrintBehaviour())


async def main():
    """
    More complex normative environment with violable norms and use of domain
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
    )
    no_prime_nums = Norm(
        "no-three-multipliers-nums",
        NormType.PROHIBITION,
        no_three_multipliers_cond_fn,
        inviolable=False,
        domain=Domain.NUMBERS,
    )

    # 3 create normative engine
    normative_engine = NormativeEngine(norm_list=[no_even_nums, no_prime_nums])

    # 4 create agent with user, apssword and noramtive engine
    ag = PrinterAgent("printer@your.xmpp.server", "test")
    ag.normative.set_normative_engine(normative_engine)

    # 5 add action to agent
    ag.normative.add_action(act)

    # 6 start agent
    await ag.start()


if __name__ == "__main__":
    spade.run(main())
