"""Device tracker platform for LandAirSea."""
from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the device tracker platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = []
    for vehicle in coordinator.data:
        entities.append(LandAirSeaTracker(coordinator, vehicle["id"]))

    async_add_entities(entities)


class LandAirSeaTracker(CoordinatorEntity, TrackerEntity):
    """Representation of a LandAirSea device tracker."""

    def __init__(self, coordinator, vehicle_id):
        """Initialize the tracker."""
        super().__init__(coordinator)
        self.vehicle_id = vehicle_id

    @property
    def _vehicle_data(self):
        """Helper to get the data for this specific vehicle from the coordinator."""
        for vehicle in self.coordinator.data:
            if vehicle["id"] == self.vehicle_id:
                return vehicle
        return {}

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.vehicle_id}_tracker"

    @property
    def name(self):
        """Return the name of the vehicle."""
        return self._vehicle_data.get("name", "LandAirSea Vehicle")

    @property
    def latitude(self):
        """Return latitude value."""
        return self._vehicle_data.get("latitude")

    @property
    def longitude(self):
        """Return longitude value."""
        return self._vehicle_data.get("longitude")

    @property
    def battery_level(self):
        """Return the battery level of the device."""
        return self._vehicle_data.get("battery")

    @property
    def source_type(self):
        """Return the source type, e.g. GPS or router."""
        return SourceType.GPS

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:car"