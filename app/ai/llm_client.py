from ollama import Client
from app.config import settings
class LLMClient:
    def __init__(self, model: str):
        self.model = model
        self.client = Client(host=settings.OLLAMA_HOST)
    async def generate(self, prompt: str):
        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
            ],
        )

        return response['message']['content']
