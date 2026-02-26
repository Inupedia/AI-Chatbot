import os
from openai import OpenAI


class ChatGPT():

    def __init__(self, config_data: dict, username: str = None):

        self.conversation: list = []
        self.config_data = config_data
        self.username = username

        api_key = os.environ.get("OPENAI_API_KEY") or self.config_data["openai"].get("api_key", "")
        if not api_key or api_key == "YOUR_API_KEY":
            print("Warning: No valid OpenAI API key found. Set OPENAI_API_KEY environment variable or update module/config.json")

        client_kwargs = {"api_key": api_key}

        if self.config_data["proxy"]["enabled"]:
            base_url = self.config_data["proxy"]["host"]
            print(f'Using proxy: {base_url}')
            client_kwargs["base_url"] = base_url

        self.client = OpenAI(**client_kwargs)

        self.conversation.append(
            {'role': 'system', 'content': self.config_data["chatgpt"]["role"]})

        self.current_message = {'role': 'user', 'content': ''}

    def add_current_message(self, content: str):
        self.current_message = {'role': 'user', 'content': content}
        self.conversation.append(self.current_message)

    def get_response(self) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=self.config_data['chatgpt']['model'],
                messages=self.conversation,
                max_tokens=self.config_data['chatgpt']['max_tokens'],
                temperature=self.config_data['chatgpt']['temperature'],
                top_p=self.config_data['chatgpt']['top_p'],
                frequency_penalty=self.config_data['chatgpt']['frequency_penalty'],
                presence_penalty=self.config_data['chatgpt']['presence_penalty']
            )
            content = resp.choices[0].message.content
            self.conversation.append(
                {'role': 'assistant', 'content': content})
            return content
        except Exception as e:
            return f"Error: {e}"

    def get_response_from_chatgpt(self) -> str:
        return self.get_response()
