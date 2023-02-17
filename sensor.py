"""Platform for sensor integration."""
from __future__ import annotations
import logging

from .const import DOMAIN
from .device import solis_device
from solis import solis
_LOGGER = logging.getLogger(__name__)

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType



async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""

    for entry_id, config in hass.data[DOMAIN].items():
        _LOGGER.info(config)
        solis_inst = solis.Solis(config["ip"], int(config["serial"]))
        sensors = [
            BatteryLevel(solis_inst)
        ]
        async_add_entities(sensors, update_before_add=True)


class BatteryLevel(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Battery Level"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT


    def __init__(self, solis):

        self.solis = solis
        super().__init__()


    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = self.solis.batt_charge_level

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return solis_device(self.solis.serial)


    @property
    def unique_id(self) ->  str:
        return self.solis.serial