from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

def solis_device(serial):
    return DeviceInfo(
        identifiers={
            # Serial numbers are unique identifiers within a specific domain
            (DOMAIN, serial)
        },
        name=f"Solis Inverter ({serial})",
        manufacturer="ginlong",
        model="solis",
        sw_version="0.0.1"
    )
