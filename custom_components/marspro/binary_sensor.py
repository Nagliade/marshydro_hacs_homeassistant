from homeassistant.components.binary_sensor import BinarySensorEntity

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["marspro"][entry.entry_id]
    async_add_entities([MarsLight(coordinator)])

class MarsLight(BinarySensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Light"

    @property
    def is_on(self):
        return self.coordinator.data.get("light", {}).get("on") == 1
