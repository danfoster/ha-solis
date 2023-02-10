import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries, core
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from .const import DOMAIN

from solis import solis

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
            serial = user_input["serial"]
            ip = user_input["ip"]
            s = solis.Solis(ip, serial)
            try:
                s.serial
                return self.async_create_entry(
                    title=f"{user_input['ip']} ({user_input['serial']})",
                    data=user_input
                )
            except solis.exceptions.SerialInvalid:
                errors["serial"] = "serial_invalid"
            except Exception as err:
                errors["base"] = "unknown"
            
        return self.async_show_form(
            step_id="user", data_schema=CONFIG_SCHEMA, errors=errors
        )