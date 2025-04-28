import logging
from typing import Optional, List, Dict, Any, Tuple
from clients.openai import OpenAIClient

class RemoteModel:
    """
    Remote model (supervisor) that uses a powerful LLM (e.g., GPT-4 via OpenAI).
    Provides an interface to generate responses using the OpenAI API.
    """
    def __init__(self, name: str, model_name: str = "gpt-4", temperature: float = 0.0, max_tokens: int = 2048):
        self.name = name
        self.logger = logging.getLogger(self.__class__.__name__)
        # Initialize OpenAI client for the remote model
        self.client = OpenAIClient(model_name=model_name, temperature=temperature, max_tokens=max_tokens)
        self.logger.info(f"Initialized remote model '{name}' with model_name='{model_name}'")

    def generate_response(self, messages: List[Dict[str, Any]]) -> str:
        """
        Send a list of messages (role/content dicts) to the model and return the response text.
        This wraps the underlying OpenAIClient to provide a unified interface.
        """
        try:
            result = self.client.chat(messages=messages)
        except Exception as e:
            self.logger.error(f"Remote model API call failed: {e}")
            return ""
        # OpenAIClient.chat returns (responses, usage) tuple; take the first response string
        outputs = result[0] if isinstance(result, tuple) else result
        if isinstance(outputs, list) and outputs:
            return outputs[0]
        elif isinstance(outputs, str):
            return outputs
        else:
            return ""

    def __repr__(self):
        return f"RemoteModel(name={self.name})"