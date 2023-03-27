import logging
import random
import reactivex as rx
from reactivex import operators as ops
from chat import OpenAIChat
from cli_game import GameCLI
from game import Game
from game_display.obs.bot import Bot
from util.read_file import read_dotenv


game_config_raiden = {
    "system_prompt": "raiden.txt",
    "subtitle_max_width": 47,
    "subtitle_max_lines": 10,
    "subtitle_input_name": "Game Text Raiden",
}

game_config_zombie_game = {
    "system_prompt": "zombie_game.txt",
    "subtitle_max_width": 50,
    "subtitle_max_lines": 18,
    "subtitle_input_name": "Game Text",
}


def main():
    game_config = game_config_raiden
    open_ai = OpenAIChat(game_config["system_prompt"])

    game_loop = Game(open_ai, game_config)

    # game_loop = GameCLI(open_ai)

    b = Bot()

    # get messages from a pipeline
    # wait 10 seconds for messages to accumulate
    # pick a random message from those
    # do an action on that message, that takes a while
    # while action is happening, ignore any events coming in
    # once action is finished, start waiting for new messages again, and go again
    b.chat.pipe(
        ops.filter(lambda _: game_loop.is_open),
        ops.filter(lambda m: len(m) <= 150 and m.startswith("!")),
        ops.map(lambda m: m[1:].strip()),
        ops.buffer_with_time(game_loop.chat_command_timeout),
        ops.filter(lambda xs: len(xs) > 0),
        ops.map(random.choice),
    ).subscribe(lambda c: game_loop.run(c))

    b.on_ready(lambda: b.chat.on_next("!Commander, where am I?"))

    b.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, force=True, filename='app.log')
    read_dotenv()
    main()
