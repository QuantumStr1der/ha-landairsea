"""Config flow for LandAirSea integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD
from .api import LandAirSeaAPI

class LandAirSeaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for LandAirSea."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user enters credentials."""
        errors = {}

        if user_input is not None:
            api = LandAirSeaAPI(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            success = await api.login()
            await api.close() # Close this temporary test session

            if success:
                return self.async_create_entry(title="LandAirSea Tracking", data=user_input)
            else:
                errors["base"] = "invalid_auth"

        data_schema = vol.Schema({
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )