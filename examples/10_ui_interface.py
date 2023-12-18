import asyncio
import logging
from enum import Enum

import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

from spade_norms import (
    NormativeMixin,
    NormativeAction,
    NormType,
    Norm,
    NormativeActionStatus,
    NormativeEngine,
)

logging.basicConfig(level=logging.INFO)


class Domain(Enum):
    NUMBERS = 1


class Role(Enum):
    SENDER = 0
    RECEIVER = 1


async def cyclic_print(agent):
    print("count: {}".format(agent.counter))


async def action2(agent):
    print("action2: {}".format(agent.jid))


def no_even_nums_cond_fn(agent):
    if agent.counter % 2 == 0:
        return NormativeActionStatus.FORBIDDEN

    return NormativeActionStatus.ALLOWED


def cond_fn(agent):
    if agent.jid.startswith("admin"):
        return NormativeActionStatus.ALLOWED
    else:
        return NormativeActionStatus.FORBIDDEN


def reward_cb(agent):
    return 100


def penalty_cb(agent):
    return -100


def reward_cb2(agent):
    return 2000


def penalty_cb2(agent):
    return -2000


class A(NormativeMixin, Agent):
    class CBehav(CyclicBehaviour):
        async def run(self):
            await asyncio.sleep(1)

    async def setup(self):
        self.add_behaviour(self.CBehav())


async def main():
    a = A("jpalanca@gtirouter.dsic.upv.es", "kakatua", verify_security=False)
    act = NormativeAction("print", cyclic_print)
    act2 = NormativeAction("show_jid", action2)
    no_even_nums = Norm(
        "no-even-nums",
        NormType.PROHIBITION,
        no_even_nums_cond_fn,
        reward_cb=reward_cb,
        penalty_cb=penalty_cb,
        roles=[Role.SENDER, Role.RECEIVER],
        domain=Domain.NUMBERS,
        inviolable=False,
    )
    admin_only = Norm(
        "admin-only",
        NormType.PERMISSION,
        cond_fn,
        reward_cb=reward_cb2,
        penalty_cb=penalty_cb2,
        roles=[Role.SENDER],
        domain=Domain.NUMBERS,
        inviolable=True,
    )
    normative_engine = NormativeEngine(norm_list=[no_even_nums, admin_only])
    a.normative.set_normative_engine(normative_engine)
    a.normative.add_action(act)
    a.normative.add_action(act2)
    await a.start()

    a.web.start(hostname="127.0.0.1", port=8080)

    while True:
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            break
    await a.stop()


if __name__ == "__main__":
    spade.run(main())
