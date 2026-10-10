from groq import Groq
import httpx

class LLMWrapper:
    def __init__(self, provider="groq", api_key=None):
        self.provider = provider

        if provider == "groq":
            self.client = Groq(
                api_key=api_key,
                http_client=httpx.Client(verify=False)
            )

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content
