import json

SYSTEM_RULES = """
You are a financial explanation assistant.

Rules:
- Do NOT perform calculations
- Do NOT create new numbers
- Do NOT change provided values
- Do NOT infer missing data
- Only explain and suggest based on given information
"""


def build_summary_prompt(data: dict):
    return f"""
{SYSTEM_RULES}

Here is a pre-calculated financial summary (JSON):
{json.dumps(data, indent=2)}

Explain the user's financial situation clearly and cautiously. Analyze the financial health of this month based on the data provided.
"""
