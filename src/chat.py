from typing import Dict, List
import openai
from os import getenv
import logging

from util.read_file import read_app_file

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class OpenAIChat():
    _messages: List[str] = []
    # Keep history
    _user_message_context_length = 4

    def __init__(self, prompt):
        OPENAI_API_KEY = getenv("OPENAI_API_KEY")
        if OPENAI_API_KEY == None:
            print("OPENAI_API_KEY isn't set!")
            exit(1)
        openai.api_key = OPENAI_API_KEY
        self._prompt = f"system_prompts/{prompt}"

    def load(self, messages):
        self._messages = messages

    def messages(self):
        return self._messages

    def last_message(self):
        return self._messages[-1]["content"]

    def _system_prompt(self):
        # Reload system prompt every time so I can tweak it mid-game.
        system_prompt = read_app_file(self._prompt)
        return {"role": "system", "content": system_prompt}

    def get_completion(self, input: str) -> str:
        user_msg = {"role": "user", "content": input.strip()}
        messages = self._concat_message(user_msg)

        logger.info("making a request")

        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[self._system_prompt()] + messages,
            temperature=1,
            max_tokens=2048
        )
        content_out = result["choices"][0]["message"]["content"]

        self._messages.append(user_msg)
        self._messages.append({"role": "assistant", "content": content_out})
        return content_out.strip()

    def _concat_message(self, user_msg) -> List[Dict[str, str]]:
        msgs = self._messages + [user_msg]
        # For each user message, keep 1 chatgpt message.
        # So with user message context length 1, it will be like:
        # "Run away" -> "long chatgpt message asking for next context" -> prompt
        total_history_length = self._user_message_context_length * 2
        return msgs[-total_history_length:]
