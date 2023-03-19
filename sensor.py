"""Platform for sensor integration."""
from __future__ import annotations
import logging

from .const import DOMAIN
from .device import solis_device
from solis import solis
from datetime import timedelta
_LOGGER = logging.getLogger(__name__)

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""

    for entry_id, config in hass.data[DOMAIN].items():
        coordinator = Solis Coordinator(hass, config["ip"], int(config["serial"]))
        await coordinator.async_config_entry_first_refresh()
        sensors = [
            BatteryLevel(coordinator),
            BatteryChargeRate(coordinator)
        ]
        async_add_entities(sensors)


class SolisCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, ip, serial):
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="Solis",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=60),
        )
        self.solis = solis.Solis(ip, serial)

        self.serial = serial

    async def _async_update_data(self) -> None:
        await self.solis._init()
        await self.solis.async_update()

class SolisSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""


    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.serial = self.coordinator.serial

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return solis_device(self.serial)


class BatteryLevel(SolisSensor):
    """Representation of a Sensor."""

    _attr_name = "Battery Level"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def state(self):
        return self.coordinator.solis.batt_charge_level

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_battlevel"

class BatteryChargeRate(SolisSensor):
    """Representation of a Sensor."""

    _attr_name = "Battery Charge Rate"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def state(self):
        return self.coordinator.solis.batt_charge_rate

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_battcharge"