from .engines.reasoning_engine import NormativeReasoningEngine
from .actions.normative_action import NormativeAction
from .engines.norm_engine import NormativeEngine
from .norms.norm import Norm
from spade.agent import Agent
from enum import Enum
import traceback
import logging
import sys

class NormativeMixin:

    def __init__(self, *args, role: Enum = None, normative_engine: NormativeEngine = None, reasoning_engine: NormativeReasoningEngine = None, actions: list = [], concerns: dict = {}, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = role
        self.normative = NormativeComponent(self, normative_engine, reasoning_engine, actions, concerns)

class NormativeComponent:
    def __init__(self, agent: Agent, normative_engine: NormativeEngine, reasoning_engine: NormativeReasoningEngine, actions: list = [], concerns: dict = {}):
        '''
        Creates a normative agent given a `NormativeEngine` and a `NormativeReasoningEngine`. If no `NormativeReasoningEngine` is provided the default is used.
        User can pass also the agent's actions as a list of `NormativeAction`. Or the agent concerns as  a `dict` with `key: norm_domain` and `value: Norm` 
        '''
        self.agent = agent
        self.normative_engine = normative_engine
        self.concerns = concerns
        self.reasoning_engine = NormativeReasoningEngine() if reasoning_engine == None else reasoning_engine
        
        self.actions = {}
        if len(actions) > 0:
            self.add_actions(actions)

    def set_normative_engine(self, normative_engine: NormativeEngine):
        '''
        Overrides the agent's actual normative engine
        '''
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
    
    def add_actions(self, action_list: list):
        for action in action_list:
            self.add_action(action)
    
    def delete_action(self, action: NormativeAction):
        self.__check_exists(action_name=action.name)
        self.actions.pop(action.name)

    def add_concern(self, concern: Norm):
        domain = concern.domain if concern.domain != None else 0
        if self.concerns.get(domain, None) == None:
            self.concerns[domain] = []
        self.concerns[domain].append(concern)

    def add_concerns(self, concern_list: list):
        for concern in concern_list:
            self.add_concern(concern)

    def contains_concern(self, concern: Norm) -> bool:
        for domain in self.concerns.keys():
            for local_concern in self.concerns[domain]:
                if concern == local_concern:
                    return True
        return False

    #TODO
    def delete_concern(self, concern: Norm) -> bool:
        pass
