from .const import DOMAIN
from .coordinator import MarsCoordinator

async def async_setup_entry(hass, entry):
    mac = entry.data["mac"]
    user = entry.data["user"]
    password = entry.data["password"]

    coordinator = MarsCoordinator(hass, mac, user, password)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "binary_sensor"])

    return True