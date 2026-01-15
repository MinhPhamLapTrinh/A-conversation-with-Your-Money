from ollama import chat
from ollama import ChatResponse


class LLMClient:
    def __init__(self, model: str):
        self.model = model

    async def generate(self, prompt: str):
        response: ChatResponse = chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
            ],
        )

        return response['message']['content']
