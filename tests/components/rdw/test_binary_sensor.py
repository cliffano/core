"""Tests for the sensors provided by the RDW integration."""
from homeassistant.components.binary_sensor import DEVICE_CLASS_PROBLEM
from homeassistant.components.rdw.const import DOMAIN, ENTRY_TYPE_SERVICE
from homeassistant.const import ATTR_DEVICE_CLASS, ATTR_FRIENDLY_NAME, ATTR_ICON
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr, entity_registry as er

from tests.common import MockConfigEntry


async def test_vehicle_binary_sensors(
    hass: HomeAssistant,
    init_integration: MockConfigEntry,
) -> None:
    """Test the RDW vehicle binary sensors."""
    entity_registry = er.async_get(hass)
    device_registry = dr.async_get(hass)

    state = hass.states.get("binary_sensor.liability_insured")
    entry = entity_registry.async_get("binary_sensor.liability_insured")
    assert entry
    assert state
    assert entry.unique_id == "11ZKZ3_liability_insured"
    assert state.state == "off"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Liability Insured"
    assert state.attributes.get(ATTR_ICON) == "mdi:shield-car"
    assert ATTR_DEVICE_CLASS not in state.attributes

    state = hass.states.get("binary_sensor.pending_recall")
    entry = entity_registry.async_get("binary_sensor.pending_recall")
    assert entry
    assert state
    assert entry.unique_id == "11ZKZ3_pending_recall"
    assert state.state == "off"
    assert state.attributes.get(ATTR_FRIENDLY_NAME) == "Pending Recall"
    assert state.attributes.get(ATTR_DEVICE_CLASS) == DEVICE_CLASS_PROBLEM
    assert ATTR_ICON not in state.attributes

    assert entry.device_id
    device_entry = device_registry.async_get(entry.device_id)
    assert device_entry
    assert device_entry.identifiers == {(DOMAIN, "11ZKZ3")}
    assert device_entry.manufacturer == "Skoda"
    assert device_entry.name == "Skoda: 11ZKZ3"
    assert device_entry.entry_type == ENTRY_TYPE_SERVICE
    assert device_entry.model == "Citigo"
    assert (
        device_entry.configuration_url
        == "https://ovi.rdw.nl/default.aspx?kenteken=11ZKZ3"
    )
    assert not device_entry.sw_version
