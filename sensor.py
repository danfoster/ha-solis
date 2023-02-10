"""Platform for sensor integration."""
from __future__ import annotations
import logging

from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity import DeviceInfo


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""
    
    for entry_id, config in hass.data[DOMAIN].items():
        _LOGGER.info(config)
        sensors = [ExampleSensor(config["ip"], config["serial"])]
        async_add_entities(sensors, update_before_add=True)

class ExampleSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    name = "solis"
    manufacturername = "ginlong"
    model = "solis"
    sw_version = "0.0.0"

    def __init__(self, ip, serial):
    
        self.ip = ip
        self.serial = serial
        super().__init__()


    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = 27

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self.serial)
            },
            name=self.name,
            manufacturer=self.manufacturername,
            model=self.model,
            sw_version=self.sw_version,
        )

    @property
    def unique_id(self) ->  str:
        return self.serial