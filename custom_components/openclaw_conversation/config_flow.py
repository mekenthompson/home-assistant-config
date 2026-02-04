"""Config flow for OpenClaw Conversation integration."""
from __future__ import annotations

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_API_TOKEN,
    CONF_API_URL,
    CONF_MODEL,
    CONF_TIMEOUT,
    DEFAULT_API_URL,
    DEFAULT_MODEL,
    DEFAULT_TIMEOUT,
    DOMAIN,
)


class OpenClawConversationConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OpenClaw Conversation."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Test the connection
            url = user_input[CONF_API_URL].rstrip("/")
            token = user_input[CONF_API_TOKEN]

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{url}/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {token}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": user_input.get(CONF_MODEL, DEFAULT_MODEL),
                            "messages": [
                                {"role": "user", "content": "ping"}
                            ],
                        },
                        timeout=aiohttp.ClientTimeout(total=30),
                    ) as resp:
                        if resp.status == 401:
                            errors["base"] = "invalid_auth"
                        elif resp.status >= 400:
                            errors["base"] = "cannot_connect"
            except (aiohttp.ClientError, TimeoutError):
                errors["base"] = "cannot_connect"

            if not errors:
                await self.async_set_unique_id("openclaw_conversation")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title="KenGPT (OpenClaw)",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_URL, default=DEFAULT_API_URL): str,
                    vol.Required(CONF_API_TOKEN): str,
                    vol.Optional(CONF_MODEL, default=DEFAULT_MODEL): str,
                    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
                }
            ),
            errors=errors,
        )
