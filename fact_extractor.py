from groq import Groq
import json
import os

# 🔐 Use environment variable (safer)
client = Groq(
    api_key="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"
)


def extract_facts(text: str):
    """
    Extract structured facts from user input using LLM.
    Returns: List of {entity, value}
    """

    prompt = f"""
Extract important user facts from this message.

Return ONLY valid JSON format like:
[
  {{ "entity": "...", "value": "..." }}
]

Rules:
- Extract meaningful user information only
- Do NOT include explanation or extra text
- If nothing useful, return []
- Keep entity names simple (budget, location, diet, condition, interest, etc.)

Examples:

User: My budget is 50000
Output:
[
  {{ "entity": "budget", "value": "50000" }}
]

User: I live in Chennai
Output:
[
  {{ "entity": "location", "value": "Chennai" }}
]

User: I am vegetarian
Output:
[
  {{ "entity": "diet", "value": "vegetarian" }}
]

User: I have headache
Output:
[
  {{ "entity": "condition", "value": "headache" }}
]

User: I want to learn machine learning
Output:
[
  {{ "entity": "interest", "value": "machine learning" }}
]

User: Suggest a laptop
Output:
[]

Now extract from:

{text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        result = response.choices[0].message.content.strip()

        # 🔹 Parse JSON safely
        facts = json.loads(result)

        # 🔹 Validate structure
        if isinstance(facts, list):
            return facts
        else:
            return []

    except json.JSONDecodeError:
        print("⚠️ JSON parsing failed:", result)
        return []

    except Exception as e:
        print("❌ Error in extract_facts:", e)
        return []
 
