import aiohttp
import logging
import time

_LOGGER = logging.getLogger(__name__)

class LandAirSeaAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_url = "https://portal.gps-tracking.com"
        self.session = None

    async def login(self):
        """Authenticate with the LandAirSea portal."""
        if self.session is None:
            self.session = aiohttp.ClientSession()

        login_url = f"{self.base_url}/default.aspx"
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/146.0.0.0",
        }

        payload = {
            "action": "login",
            "UTCoffset": "240", 
            "username": self.username,
            "password": self.password
        }

        try:
            async with self.session.post(login_url, headers=headers, data=payload, allow_redirects=False) as response:
                if response.status in (302, 303):
                    _LOGGER.info("Successfully authenticated with LandAirSea.")
                    return True
                
                _LOGGER.error("Authentication failed. Check credentials.")
                return False

        except Exception as e:
            _LOGGER.error(f"Connection error during LandAirSea login: {e}")
            return False

    async def get_vehicles(self):
        """Fetch the latest GeoJSON data for all tracked vehicles."""
        if not self.session:
            _LOGGER.error("Session not initialized. Call login() first.")
            return []

        timestamp = int(time.time() * 1000)
        data_url = f"{self.base_url}/geojson.aspx?action=scinit&_={timestamp}"

        headers = {
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/146.0.0.0",
        }

        try:
            async with self.session.get(data_url, headers=headers) as response:
                if response.status != 200:
                    _LOGGER.error(f"Failed to fetch vehicle data. HTTP Status: {response.status}")
                    return []

                raw_data = await response.json(content_type=None) # content_type=None forces parsing even if the server headers are weird
                
                parsed_vehicles = []
                
                if "features" in raw_data:
                    for feature in raw_data["features"]:
                        props = feature.get("properties", {})
                        geom = feature.get("geometry", {})
                        
                        coords = geom.get("coordinates", [0.0, 0.0])
                        longitude = coords[0]
                        latitude = coords[1]
                        
                        vehicle_data = {
                            "id": feature.get("id"),
                            "name": props.get("name", "Unknown Vehicle"),
                            "latitude": latitude,
                            "longitude": longitude,
                            "battery": props.get("batt", 0),
                            "speed": props.get("spd", 0),
                            "heading": props.get("hdg", 0),
                            "address": props.get("addy", ""),
                            "last_updated": props.get("date", ""),
                            "is_wired": props.get("wired", False)
                        }
                        parsed_vehicles.append(vehicle_data)
                        
                return parsed_vehicles

        except Exception as e:
            _LOGGER.error(f"Error fetching vehicle data: {e}")
            return []

    async def close(self):
        """Close the session."""
        if self.session:
            await self.session.close()