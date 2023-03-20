import json
import logging
from dotenv import load_dotenv
import os

from chat import OpenAIChat

state_file = "state.json"


def _read_promptfile():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # data_dir = os.path.join(script_dir, '..', 'data')
    data_file = os.path.join(script_dir, 'system_prompt.txt')
    with open(data_file) as f:
        return f.read()


def backup(state):
    with open(state_file, "w") as f:
        f.write(json.dumps(state))


def main():
    openAi = OpenAIChat(_read_promptfile())
    if os.path.isfile(state_file):
        with open(state_file) as f:
            if input("Load existing state (y/N)? ") == "y":
                state = json.loads(f.read())
                openAi.load(state)
                print(openAi.last_message())

    while True:
        action = input("Choose action: ")
        out = openAi.get_completion(action)
        print(out)
        logging.info([action, out])
        backup(openAi.messages())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, force=True, filename='app.log')
    load_dotenv(".env.local")
    load_dotenv()
    main()
