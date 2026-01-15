from app.ai.llm_client import LLMClient
from app.ai.prompt import build_summary_prompt


class AIAnalyst:
    def __init__(self):
        self.client = LLMClient()

    async def generate_financial_insight(self, data: dict) -> str:
        prompt = build_summary_prompt(data)
        return await self.client.generate(prompt)