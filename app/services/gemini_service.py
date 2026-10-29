import asyncio
from typing import Optional

import google.generativeai as genai

from app.config import get_settings

class GeminiService:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.google_api_key
        self.model_name = settings.gemini_model
        self.model = None
        self._ready = False

        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                self._ready = True
            except Exception:
                self.model = None
                self._ready = False

    def is_ready(self) -> bool:
        return self._ready and self.model is not None

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if not self.is_ready():
            raise RuntimeError("Gemini is not configured. Set GOOGLE_API_KEY in Vercel.")

        instructions = system_prompt or (
            "You are a careful strategic assistant for founders. "
            "Prioritize insight, clarity, and actionable recommendations. "
            "Keep the human in control of decisions and clearly separate "
            "recommendations from final judgment."
        )

        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.model.generate_content(
                [instructions, prompt],
                generation_config={
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "top_k": 40,
                    "max_output_tokens": 1200,
                },
            ),
        )

        return response.text or ""