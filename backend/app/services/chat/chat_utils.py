import json

from typing import List


class ChatUtils:
    @staticmethod
    def history_to_string(string: List[dict]):
        return json.dumps(string)

    @staticmethod
    def string_to_history(chat: str):
        return json.loads(chat)
