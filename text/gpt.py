import openai
import os


class Gpt():
    def __init__(self, bot_description: str) -> None:
        if bot_description is None:
            raise AttributeError("system_config must be provided")

        openai.api_key = os.getenv("OPENAI_API_KEY")

        system_config = {
            "role": "system",
            "content": bot_description
        }

        self.__history = [system_config]

    def completion(self, message: str, temperature: float = 1) -> str:
        if message is None:
            raise AttributeError("message must be provided")

        self.__add_user_message(message)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=temperature,
            messages=self.__history
        )

        message_content = response.choices[0].message.content

        self.__add_bot_message(message_content)

        return message_content

    def __add_user_message(self, message: str) -> None:
        new_message = {
            "role": "user",
            "content": message
        }

        self.__history.append(new_message)

    def __add_bot_message(self, message: str) -> None:
        new_message = {
            "role": "assistant",
            "content": message
        }
        
        self.__history.append(new_message)
