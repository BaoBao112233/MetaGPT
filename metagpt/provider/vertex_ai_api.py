#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from typing import List, Optional, Union

import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    HarmCategory,
    HarmBlockThreshold,
)

from metagpt.configs.llm_config import LLMConfig, LLMType
from metagpt.const import USE_CONFIG_TIMEOUT
from metagpt.logs import log_llm_stream, logger
from metagpt.provider.base_llm import BaseLLM
from metagpt.provider.llm_provider_registry import register_provider

@register_provider(LLMType.VERTEX_AI)
class VertexAILLM(BaseLLM):
    def __init__(self, config: LLMConfig):
        self.use_system_prompt = False
        self.config = config
        self.model = config.model
        self.pricing_plan = self.config.pricing_plan or self.model
        self.__init_vertexai(config)
        self.llm = GenerativeModel(model_name=self.model)

    def __init_vertexai(self, config: LLMConfig):
        if config.proxy:
            logger.info(f"Use proxy: {config.proxy}")
            os.environ["http_proxy"] = config.proxy
            os.environ["https_proxy"] = config.proxy
        
        credentials = None
        if config.service_account_path:
            credentials = service_account.Credentials.from_service_account_file(config.service_account_path)
            if not config.project_id:
                with open(config.service_account_path, 'r') as f:
                    sa_data = json.load(f)
                    config.project_id = sa_data.get('project_id')
        
        vertexai.init(
            project=config.project_id,
            location=config.location,
            credentials=credentials
        )

    def _user_msg(self, msg: str, images: Optional[Union[str, list[str]]] = None) -> dict:
        return {"role": "user", "parts": [{"text": msg}]}

    def _assistant_msg(self, msg: str) -> dict:
        return {"role": "model", "parts": [{"text": msg}]}

    def _system_msg(self, msg: str) -> dict:
        return {"role": "user", "parts": [{"text": msg}]}

    def format_msg(self, messages: Union[str, "Message", list[dict], list["Message"], list[str]]) -> list[dict]:
        from metagpt.schema import Message
        if not isinstance(messages, list):
            messages = [messages]
        processed_messages = []
        for msg in messages:
            if isinstance(msg, str):
                processed_messages.append({"role": "user", "parts": [{"text": msg}]})
            elif isinstance(msg, dict):
                processed_messages.append(msg)
            elif isinstance(msg, Message):
                processed_messages.append({"role": "user" if msg.role == "user" else "model", "parts": [{"text": msg.content}]})
        return processed_messages

    def _const_kwargs(self, messages: list[dict], stream: bool = False) -> dict:
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
        }
        return {
            "contents": messages,
            "generation_config": GenerationConfig(
                temperature=self.config.temperature,
                max_output_tokens=self.config.max_token,
            ),
            "safety_settings": safety_settings,
            "stream": stream,
        }

    async def _achat_completion(self, messages: list[dict], timeout: int = USE_CONFIG_TIMEOUT) -> any:
        resp = await self.llm.generate_content_async(**self._const_kwargs(messages))
        if hasattr(resp, "usage_metadata"):
            usage = {
                "prompt_tokens": resp.usage_metadata.prompt_token_count,
                "completion_tokens": resp.usage_metadata.candidates_token_count
            }
            self._update_costs(usage)
        return resp

    def get_choice_text(self, resp) -> str:
        """Required to provide the first text of choice"""
        try:
            return resp.text
        except ValueError:
            # If the response is blocked, resp.text will raise ValueError
            logger.error(f"Vertex AI response blocked: {resp}")
            return ""

    async def acompletion(self, messages: list[dict], timeout=USE_CONFIG_TIMEOUT) -> any:
        return await self._achat_completion(messages, timeout=self.get_timeout(timeout))

    async def _achat_completion_stream(self, messages: list[dict], timeout: int = USE_CONFIG_TIMEOUT) -> str:
        logger.debug(f"Vertex AI max_token: {self.config.max_token}")
        resp = await self.llm.generate_content_async(**self._const_kwargs(messages, stream=True))
        collected_content = []
        last_chunk = None
        async for chunk in resp:
            try:
                content = chunk.text
                if content:
                    log_llm_stream(content)
                    collected_content.append(content)
            except ValueError:
                # This happens if the chunk is blocked or doesn't contain text
                if chunk.candidates and chunk.candidates[0].finish_reason:
                    logger.warning(f"Stream interrupted. Finish reason: {chunk.candidates[0].finish_reason}")
                else:
                    logger.warning("Chunk contains no text and no finish reason.")
            last_chunk = chunk
        log_llm_stream("\n")
        
        if last_chunk and hasattr(last_chunk, "usage_metadata"):
            usage = {
                "prompt_tokens": last_chunk.usage_metadata.prompt_token_count,
                "completion_tokens": last_chunk.usage_metadata.candidates_token_count
            }
            self._update_costs(usage)
        return "".join(collected_content)
