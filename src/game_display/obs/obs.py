import os
import shutil
import reactivex as rx
from reactivex import operators as ops
from obswebsocket import requests as obs_req, obsws
import os
from game_display.obs.util.audio import change_tempo, get_duration
from game_display.obs.util.text import text_square

# https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#requests-table-of-contents


def init_obs():
    obs_host = 'localhost'
    obs_port = 4455
    obs_password = os.getenv("OBS_PASSWORD")
    if obs_password == None:
        print("OBS_PASSWORD isn't set!")
        exit(1)
    obs_ws = obsws(obs_host, obs_port, obs_password)
    obs_ws.connect()
    return obs_ws


class ObsAudio():
    def __init__(self, obs_ws, filename) -> None:
        self.filename = filename
        # Can't use filename because it'd start playing immediately,
        # even before play() because change_tempo rewrites the file.
        # Don't know if I can make ffmpeg use the "save_to_fp", not worth.
        self._temp_filename = filename + ".tmp.mp3"
        self._obs_ws = obs_ws
        self._current_tempo = 1.0

    def play(self):
        try:
            shutil.copy(self._temp_filename, self.filename)
        except:
            pass
        update_request = obs_req.SetInputSettings(
            inputName="Game TTS Audio",
            inputSettings={
                "local_file": self.filename,
                "from_file": True,
                "close_inactive": True,
            }
        )
        self._obs_ws.call(update_request)

    def change_tempo(self, tempo: float):
        if tempo == self._current_tempo:
            return
        change_tempo(self._temp_filename, tempo)

    def duration(self):
        return get_duration(self._temp_filename)

    def use(self, file):
        file.save(self._temp_filename)


class ObsText():
    lines_limit = 18
    chars_per_line = 50
    element_id = "Game Text"
    _line_chars = 0

    def __init__(self, obs_ws, chat_timeout):
        self._obs_ws = obs_ws
        self._text = ""
        self._chat_timeout = chat_timeout

    def clear(self):
        self._text = ""

    def add_newlines(self, count=1):
        self._text = text_square(
            self._text + ("\n" * count),
            self.chars_per_line,
            self.lines_limit
        )
        self._update_text()

    def update_text(self, word_or_phrase):
        # print(f'.{word_or_phrase}.')
        self._text = text_square(
            self._text + word_or_phrase,
            self.chars_per_line,
            self.lines_limit
        )
        self._update_text()

    def _update_text(self):
        update_request = obs_req.SetInputSettings(
            inputName=self.element_id,
            inputSettings={
                "text": self._text,
                "from_file": False
            }
        )
        self._obs_ws.call(update_request)

    def begin_wait(self):
        rx.interval(1).pipe(
            ops.take(self._chat_timeout),
            ops.start_with(-1),
        ).subscribe(lambda i: self._update_wait(self._chat_timeout - i - 1))

    def _update_wait(self, i):
        update_request = obs_req.SetInputSettings(
            inputName="Waiting on player text",
            inputSettings={
                "text": f"Your command? {i}..." if i > 0 else "",
                "from_file": False
            }
        )
        self._obs_ws.call(update_request)
