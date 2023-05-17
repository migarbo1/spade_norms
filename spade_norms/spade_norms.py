from spade_norms.actions.normative_action import NormativeAction
import traceback
import logging
import sys

class NormativeMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _hook_plugin_after_connection(self, *args, **kwargs):
        try:
            await super()._hook_plugin_after_connection(*args, **kwargs)
        except AttributeError:
            pass #logger.debug("_hook_plugin_after_connection is undefined")
        self.normative = NormativeComponent()

class NormativeComponent:
    def __init__(self):
        self.actions = {}

    def perform(self, action: str, **kwargs):
        self.__check(action)
        try:
            action_result = self.actions[action](**kwargs)
            if action_result != None:
                return action_result
        except Exception:
            logging.error(traceback.format_exc())
            print("Error performing action: ", sys.exc_info()[0])

    async def performAsync(self, action: str, **kwargs):
        self.__check(action)
        try:
            action_result = await self.actions[action].action_fn(**kwargs)
            if action_result != None:
                return action_result
        except Exception:
            logging.error(traceback.format_exc())
            print("Error performing action: ", sys.exc_info()[0])

    def __check(self, action: str):
        if self.actions.get(action, None) == None:
            raise Exception('Action with name {} does not exist in action dict'.format(action))
        
    def add_action(self, action: NormativeAction):
        self.actions[action.name] = action.action_fn
        