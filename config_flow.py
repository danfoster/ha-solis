import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries, core
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from .const import DOMAIN

from solis import solis
from solis.exceptions import ConnectionError

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {vol.Required("ip"): cv.string, vol.Required("serial"): cv.string}
)



class SolisConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Solis Local Custom config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            # Validate

            ip = user_input["ip"]
            CONFIG_SCHEMA = vol.Schema(
                 {vol.Required("ip", default=user_input["ip"]): cv.string,
                  vol.Required("serial", default=user_input["serial"]): cv.string}
            )
            try:
                serial = int(user_input["serial"])
            except ValueError:
                errors["serial"] = "serial_invalid"
                return self.async_show_form(
                    step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
                )

            try:
                s = solis.Solis(ip, serial)
            except ConnectionError:
                errors["misc"] = "connection_error"
                return self.async_show_form(
                    step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
                )

            return self.async_create_entry(
                title=f"{user_input['ip']} ({user_input['serial']})",
                data=user_input
            )
        else:
            CONFIG_SCHEMA = vol.Schema(
                 {vol.Required("ip"): cv.string, vol.Required("serial"): cv.string}
            )
        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )