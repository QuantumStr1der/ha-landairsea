"""Sensor platform for LandAirSea."""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfSpeed
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = []
    for vehicle in coordinator.data:
        entities.append(LandAirSeaBatterySensor(coordinator, vehicle["id"]))
        entities.append(LandAirSeaSpeedSensor(coordinator, vehicle["id"]))

    async_add_entities(entities)


class LandAirSeaBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for LandAirSea sensors."""

    def __init__(self, coordinator, vehicle_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.vehicle_id = vehicle_id

    @property
    def _vehicle_data(self):
        for vehicle in self.coordinator.data:
            if vehicle["id"] == self.vehicle_id:
                return vehicle
        return {}

    @property
    def device_info(self):
        """Link this sensor to the main vehicle device."""
        return {
            "identifiers": {(DOMAIN, self.vehicle_id)},
            "name": self._vehicle_data.get("name", "LandAirSea Vehicle"),
            "manufacturer": "LandAirSea",
        }


class LandAirSeaBatterySensor(LandAirSeaBaseSensor):
    """Representation of a vehicle's battery sensor."""

    @property
    def unique_id(self):
        return f"{self.vehicle_id}_battery"

    @property
    def name(self):
        return f"{self._vehicle_data.get('name', 'Vehicle')} Battery"

    @property
    def native_value(self):
        return self._vehicle_data.get("battery")

    @property
    def device_class(self):
        return SensorDeviceClass.BATTERY

    @property
    def state_class(self):
        return SensorStateClass.MEASUREMENT

    @property
    def native_unit_of_measurement(self):
        return PERCENTAGE


class LandAirSeaSpeedSensor(LandAirSeaBaseSensor):
    """Representation of a vehicle's speed sensor."""

    @property
    def unique_id(self):
        return f"{self.vehicle_id}_speed"

    @property
    def name(self):
        return f"{self._vehicle_data.get('name', 'Vehicle')} Speed"

    @property
    def native_value(self):
        return self._vehicle_data.get("speed")

    @property
    def device_class(self):
        return SensorDeviceClass.SPEED

    @property
    def state_class(self):
        return SensorStateClass.MEASUREMENT

    @property
    def native_unit_of_measurement(self):
        return UnitOfSpeed.MILES_PER_HOUR