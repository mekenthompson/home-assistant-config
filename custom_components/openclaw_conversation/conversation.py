"""Conversation platform for OpenClaw."""
from __future__ import annotations

import logging
from typing import Literal

import aiohttp

from homeassistant.components.conversation import (
    ConversationEntity,
    ConversationInput,
    ConversationResult,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.intent import IntentResponse
from homeassistant.util import ulid

from .const import (
    CONF_API_TOKEN,
    CONF_API_URL,
    CONF_MODEL,
    CONF_TIMEOUT,
    DEFAULT_MODEL,
    DEFAULT_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the OpenClaw conversation entity."""
    async_add_entities(
        [OpenClawConversationEntity(config_entry)]
    )


class OpenClawConversationEntity(ConversationEntity):
    """OpenClaw conversation agent entity."""

    _attr_has_entity_name = True
    _attr_name = "KenGPT"

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the entity."""
        self._config_entry = config_entry
        self._attr_unique_id = config_entry.entry_id
        self._api_url = config_entry.data[CONF_API_URL].rstrip("/")
        self._api_token = config_entry.data[CONF_API_TOKEN]
        self._model = config_entry.data.get(CONF_MODEL, DEFAULT_MODEL)
        self._timeout = config_entry.data.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)
        # Track conversation IDs to OpenClaw session keys
        self._conversations: dict[str, str] = {}

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return supported languages (all)."""
        return "*"

    async def async_process(
        self, user_input: ConversationInput
    ) -> ConversationResult:
        """Process a sentence."""
        # Get or create conversation/session mapping
        conv_id = user_input.conversation_id or ulid.ulid_now()
        session_key = self._conversations.get(conv_id, f"voice:google:{conv_id}")
        self._conversations[conv_id] = session_key

        _LOGGER.info(
            "OpenClaw processing: %s (conv=%s, session=%s)",
            user_input.text,
            conv_id,
            session_key,
        )

        try:
            response_text = await self._call_openclaw(
                user_input.text, session_key
            )
        except Exception as err:
            _LOGGER.error("OpenClaw API error: %s", err, exc_info=True)
            response_text = "Sorry, I couldn't reach OpenClaw right now."

        # Build the response
        intent_response = IntentResponse(language=user_input.language)
        intent_response.async_set_speech(response_text)
        return ConversationResult(
            response=intent_response,
            conversation_id=conv_id,
        )

    async def _call_openclaw(self, text: str, session_key: str) -> str:
        """Call OpenClaw's chat completions API."""
        headers = {
            "Authorization": f"Bearer {self._api_token}",
            "Content-Type": "application/json",
            "x-openclaw-session-key": session_key,
        }

        # System prompt to keep responses concise for voice
        messages = [
            {
                "role": "system",
                "content": (
                    "You are KenGPT, Ken's AI assistant. This query comes via "
                    "Google Assistant voice. Keep responses concise and natural "
                    "for spoken delivery — 1-3 sentences unless more detail is "
                    "explicitly asked for. No markdown, no bullet points, no "
                    "formatting. Just plain spoken English."
                ),
            },
            {"role": "user", "content": text},
        ]

        payload = {
            "model": self._model,
            "messages": messages,
            "stream": False,
            "user": f"google-assistant-{session_key}",
        }

        _LOGGER.info("OpenClaw request to %s", self._api_url)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._api_url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self._timeout),
            ) as resp:
                body = await resp.text()
                _LOGGER.info("OpenClaw response status: %s", resp.status)
                if resp.status != 200:
                    raise Exception(
                        f"OpenClaw returned {resp.status}: {body}"
                    )
                import json
                data = json.loads(body)
                choices = data.get("choices", [])
                if not choices:
                    return "I processed your request but got an empty response."
                return choices[0]["message"]["content"]
