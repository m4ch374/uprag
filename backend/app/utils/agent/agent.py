# TODO: streaming support


class Agent:
    def __init__(self, model: str, system_prompt: str, temperature: float = 1):
        self.model = model
        self.system_prompt = system_prompt
        self.temperature = temperature

        self.history = self.__generate_initial_history__()

    def __generate_initial_history__(self):
        raise NotImplementedError("Not implemented")

    async def generate_chat_response(self, user_query: str):
        raise NotImplementedError("Not implemented")

    async def generate_ragged_chat_response(self, user_query: str):
        raise NotImplementedError("Not implemented")

    async def generate_response(self, user_query: str, rag: bool = False):
        return await (
            self.generate_chat_response(user_query)
            if not rag
            else self.generate_ragged_chat_response(user_query)
        )
