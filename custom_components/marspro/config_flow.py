import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN

class MarsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="MarsPro", data=user_input)

        schema = vol.Schema({
            vol.Required("mac"): str,
            vol.Required("user"): str,
            vol.Required("password"): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema)