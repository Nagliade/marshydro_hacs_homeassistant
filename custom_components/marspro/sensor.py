from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

SENSORS = {
    "temp": ("Temperature", "°C"),
    "humi": ("Humidity", "%"),
    "co2": ("CO2", "ppm"),
    "vpd": ("VPD", "kPa"),
    "ppfd": ("PPFD", "µmol/m²/s"),
    "tempSoil": ("Soil Temperature", "°C"),
    "humiSoil": ("Soil Humidity", "%"),
    "ECSoil": ("Soil EC", "mS/cm"),
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    for key, (name, unit) in SENSORS.items():
        entities.append(MarsSensor(coordinator, key, name, unit))

    async_add_entities(entities)


class MarsSensor(SensorEntity):
    def __init__(self, coordinator, key, name, unit):
        self.coordinator = coordinator
        self.key = key
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self):
        return self.coordinator.data.get("sensor", {}).get(self.key)

    @property
    def available(self):
        return bool(self.coordinator.data)