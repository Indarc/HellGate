"""
Pytest configuration and shared fixtures for all tests
"""
import pytest
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_logger():
    """Mock logger fixture for all tests"""
    logger = MagicMock()
    logger.info = MagicMock()
    logger.error = MagicMock()
    logger.warning = MagicMock()
    logger.debug = MagicMock()
    return logger


@pytest.fixture
def sample_item_dict():
    """Sample item dictionary for testing"""
    return {
        "id": 1,
        "name": "Test Item",
        "item_type": "another",
        "_": "another",
        "rare": "common",
        "cost": 100,
        "description": "Test description",
        "emoji": "📦",
        "stacked": False
    }


@pytest.fixture
def sample_weapon_dict():
    """Sample weapon dictionary for testing"""
    return {
        "id": 101,
        "name": "Test Sword",
        "item_type": "weapon",
        "_": "weapon",
        "rare": "uncommon",
        "cost": 500,
        "description": "A powerful sword",
        "emoji": "⚔️",
        "stacked": False,
        "slot": 0,
        "stats": {
            "damage": {"physical": 25},
            "crit": 10.0,
            "crit_multy": 2.0,
            "attack_speed": 1.2
        },
        "affixes": {},
        "equip_requirements": {}
    }


@pytest.fixture
def sample_armor_dict():
    """Sample armor dictionary for testing"""
    return {
        "id": 102,
        "name": "Steel Plate",
        "item_type": "armor",
        "_": "armor",
        "rare": "uncommon",
        "cost": 400,
        "description": "Heavy steel armor",
        "emoji": "🛡️",
        "stacked": False,
        "slot": "chest",
        "stats": {
            "armor": 30,
            "health": 50
        },
        "affixes": {},
        "equip_requirements": {}
    }


@pytest.fixture
def sample_user_dict():
    """Sample user dictionary for testing"""
    return {
        "_": "User",
        "id": 12345,
        "player": {
            "id": 12345,
            "name": "TestPlayer",
            "level": 5,
            "experience": 1000,
            "inventory": {}
        }
    }


# Pytest configuration
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async (requires pytest-asyncio)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
