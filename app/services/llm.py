import logging
from typing import Any, Dict, List, Optional
from app.core.config import settings
from app.core.exceptions import LLMError

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        self.api_key = settings.LLM_API_KEY
        self.base_url = settings.LLM_BASE_URL
        self.temperature = settings.LLM_TEMPERATURE
        self.max_tokens = settings.LLM_MAX_TOKENS

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        context: Optional[str] = None,
    ) -> str:
        try:
            from litellm import acompletion

            system_message = (
                f"You are Cloud Companion, an AI assistant for cloud troubleshooting. "
                f"Use the following context to provide step-by-step solutions:\n{context}"
                if context
                else "You are Cloud Companion, an AI assistant for cloud troubleshooting."
            )

            formatted_messages = [
                {"role": "system", "content": system_message},
                *messages,
            ]

            response = await acompletion(
                model=f"{self.provider}/{self.model}",
                messages=formatted_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_base=self.base_url if self.provider == "ollama" else None,
                api_key=self.api_key or "not-needed",
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            raise LLMError(f"Failed to generate response: {str(e)}")

    async def create_embeddings(self, text: str) -> List[float]:
        try:
            from litellm import aembedding

            response = await aembedding(
                model=f"{self.provider}/embedding",
                input=[text],
                api_base=self.base_url if self.provider == "ollama" else None,
                api_key=self.api_key or "not-needed",
            )

            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Embedding generation error: {str(e)}")
            raise LLMError(f"Failed to generate embeddings: {str(e)}")

    async def health_check(self) -> bool:
        try:
            await self.generate_response([{"role": "user", "content": "ping"}])
            return True
        except Exception as e:
            logger.error(f"LLM health check failed: {str(e)}")
        return False
