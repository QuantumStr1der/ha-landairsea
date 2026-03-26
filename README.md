# LandAirSea Home Assistant Integration

A custom integration for Home Assistant that tracks [LandAirSea](https://landairsea.com/) GPS devices. This component uses the SilverCloud web portal to bring your vehicle's real-time location and telemetry directly into your smart home dashboard.

## Features

This integration creates a single device for each tracker on your account, populated with the following entities:

* **📍 Device Tracker:** Shows the live location on your Home Assistant map.
* **🔋 Battery Sensor:** Monitors the internal battery percentage.
* **⚡ Speed Sensor:** Tracks the current speed in MPH.
* **🔌 Power Status:** Indicates whether the tracker is currently running on hardwired power or internal battery.
* **🗺️ Address Sensor:** A text sensor displaying the current street address.
* **⛰️ Elevation Sensor:** Displays the current elevation in feet.
* **🕒 Last Updated Sensor:** Shows the timestamp when the tracker was last moved.

## Installation

### Option 1: HACS (Recommended)
1. Open HACS in your Home Assistant instance.
2. Click the three dots in the top right corner and select **Custom repositories**.
3. Add the URL to this repository and select **Integration** as the category.
4. Click **Add**, then search for "LandAirSea" in HACS and click Download.
5. Restart Home Assistant.

### Option 2: Manual
1. Download this repository.
2. Copy the `custom_components/land_air_sea` directory into your Home Assistant `config/custom_components` directory.
3. Restart Home Assistant.

## Configuration

Setup is handled entirely through the Home Assistant UI. No YAML configuration is required!

1. Go to **Settings > Devices & Services**.
2. Click the **+ Add Integration** button in the bottom right.
3. Search for "LandAirSea".
4. Enter your LandAirSea portal Username and Password.

*Note: The integration polls the server every 60 seconds to prevent your account from being rate-limited while still providing near real-time updates.*

## Example Automations

With all this data exposed, you can build powerful automations. 

**Notify when a vehicle leaves home:**
```yaml
alias: "Security: Dirtbike Left Home"
trigger:
  - platform: state
    entity_id: device_tracker.811047_tracker
    from: "home"
    to: "not_home"
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "Movement Detected!"
      message: "The dirtbike just left the home zone."