import logging
from typing import List, Dict, Any, Tuple
# Assuming OpenAIClient and OllamaClient are available from provided clients
from clients.openai import OpenAIClient
from clients.ollama import OllamaClient
from skill_tests.skill_test import SkillTest

class LocalModel:
    """
    Local model (minion) which can use either OpenAI API or Ollama (local LLM).
    Provides a unified interface to get responses from the model.
    """
    def __init__(self, name: str, model_type: str = "openai", model_name: str = "gpt-3.5-turbo", temperature: float = 0.0, max_tokens: int = 1024):
        """
        model_type: "openai" for OpenAI API, "ollama" for local Ollama server.
        model_name: identifier for the model (e.g., "gpt-3.5-turbo" or an Ollama model name).
        """
        self.name = name
        self.model_type = model_type.lower()
        self.logger = logging.getLogger(self.__class__.__name__ + f"({name})")
        if self.model_type == "openai":
            # Create OpenAI client for this model
            self.client = OpenAIClient(model_name=model_name, temperature=temperature, max_tokens=max_tokens)
        elif self.model_type == "ollama":
            # Create Ollama client for this model
            self.client = OllamaClient(model_name=model_name, temperature=temperature, max_tokens=max_tokens)
        else:
            raise ValueError(f"Unsupported model_type: {model_type}")
        self.logger.info(f"Initialized local model '{name}' of type '{model_type}' with model_name='{model_name}'")

    def generate_response(self, messages: List[Dict[str, Any]]) -> str:
        """
        Send a list of messages to the model and return the response text.
        Handles the difference in return format between OpenAI and Ollama clients.
        """
        try:
            result = self.client.chat(messages=messages)
        except Exception as e:
            self.logger.error(f"Local model '{self.name}' API call failed: {e}")
            return ""
        # Both OpenAIClient.chat and OllamaClient.chat return a tuple; first element is list of outputs.
        outputs = result[0] if isinstance(result, tuple) else result
        if isinstance(outputs, list) and outputs:
            return outputs[0]
        elif isinstance(outputs, str):
            return outputs
        else:
            return ""

    def run_test(self, test: SkillTest) -> str:
        """
        Given a SkillTest (with context and question), run the local model to produce an answer.
        Constructs the prompt in a straightforward way (context + question as user message).
        """
        prompt = ""
        if test.context:
            prompt += f"{test.context}\n"
        prompt += f"Q: {test.question}\nA:"  # Format context and question for the prompt
        messages = [{"role": "user", "content": prompt}]
        answer = self.generate_response(messages)
        return answer.strip()

    def __repr__(self):
        return f"LocalModel(name={self.name}, type={self.model_type})"