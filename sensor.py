"""Platform for sensor integration."""
from __future__ import annotations
import logging
from datetime import timedelta

from solis import solis
from homeassistant.helpers.entity import DeviceInfo
from homeassistant import config_entries
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfPower, UnitOfElectricPotential, TEMP_CELSIUS, UnitOfEnergy
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN
from .device import solis_device


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    _: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    """Setup sensors from a config entry created in the integrations UI."""

    for _, config in hass.data[DOMAIN].items():
        coordinator = await SolisCoordinator.create(hass, config["ip"], int(config["serial"]))
        await coordinator.async_config_entry_first_refresh()
        sensors = [
            BatteryLevel(coordinator),
            BatteryChargeRate(coordinator),
            DCVoltage1(coordinator),
            DCVoltage2(coordinator),
            Temperature(coordinator),
            PowerGenToday(coordinator),
            BatteryChargeToday(coordinator),
            BatteryDischargeToday(coordinator),
            HouseLoadToday(coordinator),
            GridImportedToday(coordinator),
            GridExportedToday(coordinator),
            PowerGenertion(coordinator),
            HouseLoad(coordinator),
            BackupLoad(coordinator),
            GridUsage(coordinator),
        ]
        async_add_entities(sensors)

class SolisCoordinator(DataUpdateCoordinator):
    """
    Home assistant coordinator for Solis. Responsible
    for pulling data from the Solis Inverter.
    """
    @classmethod
    async def create(cls, hass, ipaddr, serial):
        """
        Factory method for creating the object via a async
        co-routine.
        Use instead of the normal contructor.
        """
        self = SolisCoordinator(hass, serial)
        self.solis = await solis.Solis.create(ipaddr, serial)
        return self


    def __init__(self, hass, serial):
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="Solis",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=60),
        )
        self.solis = None
        self.serial = serial

    async def _async_update_data(self) -> None:
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

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT


    @property
    def name(self):
        """Name of the entity."""
        return "Battery Level"


    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.batt_charge_level
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_battlevel"

class BatteryChargeRate(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "Battery Charge Rate"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.batt_charge_rate
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_battcharge"

class DCVoltage1(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "DC Voltage 1"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.dc_voltage_1
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_dc_voltage_1"

class DCVoltage2(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "DC Voltage 2"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.dc_voltage_2
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_dc_voltage_2"

class Temperature(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "Temperture"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.temperture
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_temperture"

class PowerGenToday(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "Power Generation Today"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.power_gen_today
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_power_gen_today"

class BatteryChargeToday(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "Battery Charge Today"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.battery_charge_today
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_battery_charge_today"

class BatteryDischargeToday(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "Battery Discharge Today"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.battery_charge_today
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_battery_charge_today"

class HouseLoadToday(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "House Load Today"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.house_load_today
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_house_load_today"

class GridImportedToday(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "Grid Imported Today"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.grid_imported_today
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_grid_imported_today"

class GridExportedToday(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "Grid Exported Today"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.grid_exported_today
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_grid_exported_today"

class PowerGenertion(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "Power Generation"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.power_generation
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_power_generation"

class HouseLoad(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "House Load"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.house_load
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_house_load"

class BackupLoad(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "Backup Load"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.backup_load
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_backup_load"

class GridUsage(SolisSensor):
    """Representation of a Sensor."""

    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self):
        """Name of the entity."""
        return "Grid Usage"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self.coordinator.solis.grid_usage
        self.async_write_ha_state()

    @property
    def unique_id(self) ->  str:
        return str(self.serial) + "_grid_usage"