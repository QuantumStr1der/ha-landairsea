"""The LandAirSea integration."""
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, UPDATE_INTERVAL
from .api import LandAirSeaAPI

_LOGGER = logging.getLogger(__name__)

# We will create a device tracker (for the map) and standard sensors (for battery/speed)
PLATFORMS = ["device_tracker", "sensor", "binary_sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up LandAirSea from a UI config entry."""
    
    api = LandAirSeaAPI(entry.data[CONF_USERNAME], entry.data[CONF_PASSWORD])
    await api.login()

    async def async_update_data():
        """Fetch the latest GPS data from the API."""
        try:
            vehicles = await api.get_vehicles()
            if not vehicles:
                raise UpdateFailed("No vehicles returned from API")
            return vehicles
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="landairsea_tracking",
        update_method=async_update_data,
        update_interval=timedelta(seconds=UPDATE_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "api": api
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the integration when the user deletes it or restarts."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["api"].close()
    return unload_ok