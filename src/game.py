import json
import reactivex as rx
from reactivex import operators as ops
from chat import OpenAIChat
from game_display.obs.obs import ObsAudio, ObsText, init_obs
from game_display.obs.tts import Tts
from util.read_file import app_file_path


class Game():
    _obs_text: ObsText
    _ai: OpenAIChat
    _tts: Tts
    chat_command_timeout = 30

    def __init__(self, ai, game_config) -> None:
        self._ai = ai

        obs = init_obs()
        self._obs_text = ObsText(obs, self.chat_command_timeout)
        self._obs_text.lines_limit = game_config["subtitle_max_lines"]
        self._obs_text.chars_per_line = game_config["subtitle_max_width"]
        self._obs_text.element_id = game_config["subtitle_input_name"]

        self.is_open = True
        self._tts = Tts(ObsAudio(obs, app_file_path("tts.mp3")))
        self._tts.speaking.subscribe(self._obs_text.update_text)
        self._state_file = app_file_path("state.json")

    def _run_command(self, cmd):
        self._obs_text.add_newlines(2)
        self._tts.speak('You decide to: ' + cmd)

    def _complete(self, command):
        print("\n\n#######getting ai completion!!!!!!!!\n\n")
        ai_completion = self._ai.get_completion(command)
        print(ai_completion)
        self._backup()
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
        ai_completion = self._complete(command)
        # ai_completion = self._debug_complete(command)

        self._obs_text.clear()
        self._tts.speak(ai_completion)

        self._obs_text.begin_wait()
        self.is_open = True

    def _backup(self):
        with open(self._state_file, "w") as f:
            f.write(json.dumps(self._ai.messages()))

# ai_completion = """You step carefully up to the door while the zombie glares at you hungrily from the other side. You press your face up against the bars and try to reason with the undead creature, hoping that there might be a bit of its humanity left.

# "You don't have to do this," you plead, "We can figure something out together."

# The zombie continues to stare at you with vacant eyes, clearly not responding to your words. Suddenly it lunges forward, grabbing at the bars of the cell with its undead strength.

# Rolling the dice... You need at least a 15 to successfully dodge the zombie's attack.

# You rolled a 3. Unfortunately, you are unable to dodge the attack and the zombie grabs your arm, sinking its teeth into your flesh. You scream in pain, but the zombie doesn't let go. Your vision begins to blur as you realize the severity of your mistake.

# Game over."""
