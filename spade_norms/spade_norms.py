from spade_norms.actions.normative_action import NormativeAction
from .engines.norm_engine import NormativeEngine
from .engines.reasoning_engine import NormativeReasoningEngine
from spade.agent import Agent
import traceback
import logging
import sys

class NormativeMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.normative = NormativeComponent(self)

class NormativeComponent:
    def __init__(self, agent: Agent, normative_engine: NormativeEngine = None, reasoning_engine: NormativeReasoningEngine = None):
        self.actions = {}
        self.agent = agent
        self.normative_engine = normative_engine
        self.reasoning_engine = NormativeReasoningEngine() if reasoning_engine == None else reasoning_engine

    def set_normative_engine(self, normative_engine: NormativeEngine):
        self.normative_engine = normative_engine

    def perform(self, action_name: str, *args, **kwargs):
        self.__check_exists(action_name)
        action = self.actions[action_name]
        if self.normative_engine != None:
            normative_response = self.normative_engine.check_legislation(action, self.agent)
            do_action = self.reasoning_engine.inference(normative_response)
        else:
            do_action = True
        if do_action:
            try:
                action_result = self.actions[action_name].action_fn(self.agent, *args, **kwargs)
                if action_result != None:
                    return action_result
            except Exception:
                logging.error(traceback.format_exc())
                print("Error performing action: ", sys.exc_info()[0])
        else:
            #TODO: proceeding for actions not performed
            print("Action {} not performed due to normative constrictions".format(action_name))

    async def performAsync(self, action_name: str, *args, **kwargs):
        self.__check_exists(action_name)
        action = self.actions[action_name]
        if self.normative_engine != None:
            normative_response = self.normative_engine.check_legislation(action, self.agent)
            do_action = self.reasoning_engine.inference(normative_response)
        else:
            do_action = True
        if do_action:
            try:    
                action_result = await self.actions[action_name].action_fn(self.agent, *args, **kwargs)
                if action_result != None:
                    return action_result
            except Exception:
                logging.error(traceback.format_exc())
                print("Error performing action: ", sys.exc_info()[0])
        else:
            #TODO: proceeding for actions not performed
            print("Action {} not performed due to normative constrictions".format(action_name))

    def __check_exists(self, action_name: str):
        if self.actions.get(action_name, None) == None:
            raise Exception('Action with name {} does not exist in action dict'.format(action_name))
        
    def add_action(self, action: NormativeAction):
        self.actions[action.name] = action
        