"""Binary sensor platform for LandAirSea."""
from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the binary sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    entities = [LandAirSeaWiredSensor(coordinator, vehicle["id"]) for vehicle in coordinator.data]
    async_add_entities(entities)

class LandAirSeaWiredSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a vehicle's wired status."""

    def __init__(self, coordinator, vehicle_id):
        super().__init__(coordinator)
        self.vehicle_id = vehicle_id

    @property
    def _vehicle_data(self):
        for vehicle in self.coordinator.data:
            if vehicle["id"] == self.vehicle_id: return vehicle
        return {}

    @property
    def unique_id(self):
        return f"{self.vehicle_id}_wired"

    @property
    def name(self):
        return f"{self._vehicle_data.get('name', 'Vehicle')} Power Connected"

    @property
    def is_on(self):
        """Return true if the tracker is hardwired."""
        return self._vehicle_data.get("is_wired", False)

    @property
    def device_class(self):
        return BinarySensorDeviceClass.POWER

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.vehicle_id)},
            "name": self._vehicle_data.get("name", "LandAirSea Vehicle"),
            "manufacturer": "LandAirSea",
        }