import time
from reactivex import operators as ops
from gtts import gTTS
import reactivex as rx
import re

from config import TTS_SPEED


class Tts():
    speaking: rx.Subject

    def __init__(self, obs_audio) -> None:
        self.speaking = rx.Subject()
        self._obs_audio = obs_audio

    def speak(self, words):
        tts = gTTS(words, slow=False)
        self._obs_audio.use(tts)
        self._obs_audio.change_tempo(TTS_SPEED)
        duration = self._obs_audio.duration()
        self._emit_spoken_sentences(words, duration)
        self._obs_audio.play()
        # I used to use "playsound" which was blocking, so I'll block here.
        time.sleep(duration)

    def _emit_spoken_sentences(self, words, total_duration):
        s = self._sentences(words)
        ws = words.split()
        word_duration = (total_duration / len(ws)) - 0.05
        rx.interval(word_duration).pipe(
            ops.take(len(ws)),
            ops.filter(lambda i: self._contains_pause(ws[i])),
            # ops.do_action(lambda i: print(ws[i])),
            # It takes about 0.5s to wait for pauses between sentences.
            ops.delay(0.5),
            ops.start_with("start"),
            # Final sentence's period shouldn't count.
            ops.filter_indexed(lambda _, i: i < len(s)),
            ops.map_indexed(lambda _, i: s[i]),
        ).subscribe(self.speaking.on_next)

    def _contains_pause(self, word):
        return re.search(r'[^,.:?!;][,.:?!;]', word) is not None

    # Splits up anything with a pause in speech.
    def _sentences(self, words):
        return re.findall(r'[^,.:?!;]+[,.:?!;]*', words)


def _test():
    t = Tts()
    t.speaking.subscribe(print)
    ai_completion_ends_without_period = """You find yourself in a small holding cell. The room is dimly lit, and you can hear the faint sound of moaning and shuffling outside of the door. You have no weapons and only a small water bottle in your inventory. You see a small window with bars above you, but it seems too high to reach.

Actions:
1. Try to break open the cell door
2. Look for any objects that could help in your escape
3. Try to climb up to the window"""
    t._emit_spoken_sentences(ai_completion_ends_without_period, 31.152)

#     ai_completion = """You step carefully up to the door while the zombie glares at you hungrily from the other side. You press your face up against the bars and try to reason with the undead creature, hoping that there might be a bit of its humanity left.

# "You don't have to do this," you plead, "We can figure something out together."

# The zombie continues to stare at you with vacant eyes, clearly not responding to your words. Suddenly it lunges forward, grabbing at the bars of the cell with its undead strength.

# Rolling the dice... You need at least a 15 to successfully dodge the zombie's attack.

# You rolled a 3. Unfortunately, you are unable to dodge the attack and the zombie grabs your arm, sinking its teeth into your flesh. You scream in pain, but the zombie doesn't let go. Your vision begins to blur as you realize the severity of your mistake.

# Game over."""
#     t._emit_spoken_sentences(ai_completion, 59.088)

    # t.speak(ai_completion)
    time.sleep(60)


if __name__ == "__main__":
    _test()
