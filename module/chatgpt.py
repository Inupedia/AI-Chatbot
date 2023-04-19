import openai


class ChatGPT():

    def __init__(self, config_data: dict, username: str = None):

        self.conversation: list = []
        self.config_data = config_data
        self.username = username

        # set up openai api key
        openai.api_key = self.config_data["openai"]["api_key"]

        # initialize the personality of the AI vtuber
        self.conversation.append(
            {'role': 'system', 'content': self.config_data["chatgpt"]["role"]})

        # initialize the current message
        self.current_message = {'role': 'user', 'content': ''}

    def add_current_message(self, content: str):
        self.current_message['content'] = content
        self.conversation.append(self.current_message)

    def get_response_from_chatgpt(self) -> str:
        try:
            resp = openai.ChatCompletion.create(
                model=self.config_data['chatgpt']['model'],
                messages=self.conversation,
                max_tokens=self.config_data['chatgpt']['max_tokens'],
                temperature=self.config_data['chatgpt']['temperature'],
                top_p=self.config_data['chatgpt']['top_p'],
                frequency_penalty=self.config_data['chatgpt']['frequency_penalty'],
                presence_penalty=self.config_data['chatgpt']['presence_penalty']
            )
            content = resp['choices'][0]['message']['content']
            self.conversation.append(
                {'role': 'assistant', 'content': content})
            return content
        except openai.OpenAIError as e:
            return f"Error: {e}"
