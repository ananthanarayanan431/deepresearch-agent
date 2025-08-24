import opik

from deepresearch.config.env import OPIK_API_KEY


class Opik_prompts:
    """Wrapper class for Opik Prpmpt managent tool"""

    @classmethod
    def get_prompt(cls, prompt_name):
        if not OPIK_API_KEY:
            raise ValueError("Opik API Key is missing")

        try:
            opik_client = opik.Opik(api_key=OPIK_API_KEY)
            prompt = opik_client.get_prompt(name=prompt_name)
            return prompt.prompt

        except Exception:
            return None
