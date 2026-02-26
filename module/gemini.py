import os
from google import genai
from google.genai import types


class Gemini():

    def __init__(self, config_data: dict, username: str = None):

        self.conversation: list = []
        self.config_data = config_data
        self.username = username

        api_key = (os.environ.get("GEMINI_API_KEY")
                   or os.environ.get("GOOGLE_API_KEY")
                   or self.config_data.get("gemini", {}).get("api_key", ""))
        if not api_key or api_key == "YOUR_API_KEY":
            print("Warning: No valid Gemini API key found. "
                  "Set GEMINI_API_KEY environment variable or update module/config.json")

        self.client = genai.Client(api_key=api_key)

        gemini_config = self.config_data.get("gemini", {})
        chat_config = self.config_data.get("chatgpt", {})

        self.model_name = gemini_config.get("model", "gemini-2.0-flash")
        self.temperature = chat_config.get("temperature", 0.9)
        self.max_tokens = chat_config.get("max_tokens", 1000)
        self.role = chat_config.get("role", "")

        self.chat_history: list = []

    def add_current_message(self, content: str):
        self.conversation.append({'role': 'user', 'content': content})
        self.chat_history.append(
            types.Content(role="user", parts=[types.Part(text=content)])
        )

    def get_response(self) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=self.chat_history,
                config=types.GenerateContentConfig(
                    system_instruction=self.role,
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                ),
            )
            content = response.text
            self.conversation.append({'role': 'assistant', 'content': content})
            self.chat_history.append(
                types.Content(role="model", parts=[types.Part(text=content)])
            )
            return content
        except Exception as e:
            return f"Error: {e}"
