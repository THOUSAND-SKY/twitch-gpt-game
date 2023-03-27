import reactivex as rx
from reactivex import operators as ops
from chat import OpenAIChat


class GameCLI():
    _ai: OpenAIChat
    chat_command_timeout = 1

    def __init__(self, ai) -> None:
        self._ai = ai
        self.is_open = True

    def _run_command(self, cmd):
        print("\n\nYou decide to:", cmd)

    def _complete(self, command):
        ai_completion = self._ai.get_completion(command)
        return ai_completion

    def _debug_complete(self, command):
        return """You  find yourself in a holding cell. The walls are made of thick concrete and there's only one door. You can hear growls and moans on the other side. You notice a small hole on the ceiling, maybe big enough to climb through. What do you do?

Option 1: Check the door for a way to open it quietly and peek through to assess the situation.
Option 2: Check the door for a way to open it quietly and peek through to assess the situation.
Option 3: Climb the hole in the ceiling to try to escape.
Option 4: Yell as loud as you can for help."""

    def run(self, command: str):
        if not command:
            print("no command")
            return
        self.is_open = False
        self._run_command(command)
        print("\n\n#######getting ai completion!!!!!!!!\n\n")
        ai_completion = self._complete(command)
        # ai_completion = self._debug_complete(command)

        print(ai_completion)

        self.is_open = True
