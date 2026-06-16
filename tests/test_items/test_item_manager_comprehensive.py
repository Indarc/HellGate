"""
Comprehensive tests for ItemManager
Tests item loading, retrieval, and conversion functionality
"""
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Optional

from game.manager.item_manager import ItemManager
from game.classes.items import Item, Weapon, Armor, Jewelry, EquipItem


@pytest.fixture
def temp_items_dir(tmp_path):
    """Create temporary directory structure with sample JSON items"""
    # Create subdirectories
    weapon_dir = tmp_path / "weapon"
    armor_dir = tmp_path / "armor"
    jewelry_dir = tmp_path / "jewelry"
    another_dir = tmp_path / "another"
    
    weapon_dir.mkdir()
    armor_dir.mkdir()
    jewelry_dir.mkdir()
    another_dir.mkdir()
    
    # Sample weapon item
    weapon_data = {
        "id": 1,
        "name": "Iron Sword",
        "item_type": "weapon",
        "_": "weapon",
        "rare": "common",
        "cost": 100,
        "description": "A simple iron sword",
        "emoji": "⚔️",
        "stacked": False,
        "slot": 0,
        "stats": {
            "damage": {"physical": 10},
            "crit": 5.0,
            "crit_multy": 1.5,
            "attack_speed": 1.0
        },
        "affixes": {},
        "equip_requirements": {}
    }
    
    # Sample armor item
    armor_data = {
        "id": 2,
        "name": "Leather Armor",
        "item_type": "armor",
        "_": "armor",
        "rare": "common",
        "cost": 50,
        "description": "Basic leather protection",
        "emoji": "🛡️",
        "stacked": False,
        "slot": "chest",
        "stats": {
            "armor": 5
        },
        "affixes": {},
        "equip_requirements": {}
    }
    
    # Sample jewelry item
    jewelry_data = {
        "id": 3,
        "name": "Gold Ring",
        "item_type": "jewelry",
        "_": "jewelry",
        "rare": "rare",
        "cost": 200,
        "description": "A shiny gold ring",
        "emoji": "💍",
        "stacked": False,
        "slot": "ring",
        "stats": {},
        "affixes": {},
        "equip_requirements": {}
    }
    
    # Sample simple item
    item_data = {
        "id": 4,
        "name": "Health Potion",
        "item_type": "another",
        "_": "another",
        "rare": "common",
        "cost": 10,
        "description": "Restores 50 HP",
        "emoji": "🧪",
        "stacked": True
    }
    
    # Write JSON files
    with open(weapon_dir / "sword.json", "w", encoding="utf-8") as f:
        json.dump(weapon_data, f)
    
    with open(armor_dir / "leather.json", "w", encoding="utf-8") as f:
        json.dump(armor_data, f)
    
    with open(jewelry_dir / "ring.json", "w", encoding="utf-8") as f:
        json.dump(jewelry_data, f)
    
    with open(another_dir / "potion.json", "w", encoding="utf-8") as f:
        json.dump(item_data, f)
    
    return tmp_path


class TestItemManagerInitialization:
    """Tests for ItemManager initialization"""
    
    def test_item_manager_init_with_valid_path(self, temp_items_dir):
        """Test ItemManager initialization with valid path"""
        manager = ItemManager(temp_items_dir)
        assert manager.items_path == temp_items_dir
        assert isinstance(manager.item_classes, dict)
        assert "weapon" in manager.item_classes
        assert "armor" in manager.item_classes
        assert "jewelry" in manager.item_classes
        assert "another" in manager.item_classes
    
    def test_item_manager_loads_items_on_init(self, temp_items_dir):
        """Test that ItemManager loads items from files on initialization"""
        manager = ItemManager(temp_items_dir)
        assert len(manager.items) > 0
        assert 1 in manager.items  # weapon
        assert 2 in manager.items  # armor
        assert 3 in manager.items  # jewelry
        assert 4 in manager.items  # simple item
    
    def test_item_manager_item_classes_mapping(self, temp_items_dir):
        """Test that item classes are correctly mapped"""
        manager = ItemManager(temp_items_dir)
        assert manager.item_classes["weapon"] == Weapon
        assert manager.item_classes["armor"] == Armor
        assert manager.item_classes["jewelry"] == Jewelry
        assert manager.item_classes["another"] == Item


class TestItemManagerGetItem:
    """Tests for get_item method"""
    
    def test_get_item_returns_item_by_id(self, temp_items_dir):
        """Test getting an item by its ID"""
        manager = ItemManager(temp_items_dir)
        item = manager.get_item(1)
        assert item is not None
        assert item.id == 1
        assert item.name == "Iron Sword"
    
    def test_get_item_returns_none_for_nonexistent_id(self, temp_items_dir):
        """Test that get_item returns None for non-existent ID"""
        manager = ItemManager(temp_items_dir)
        item = manager.get_item(999)
        assert item is None
    
    def test_get_item_returns_weapon(self, temp_items_dir):
        """Test getting a weapon item"""
        manager = ItemManager(temp_items_dir)
        item = manager.get_item(1)
        assert isinstance(item, Weapon)
    
    def test_get_item_returns_armor(self, temp_items_dir):
        """Test getting an armor item"""
        manager = ItemManager(temp_items_dir)
        item = manager.get_item(2)
        assert isinstance(item, Armor)
    
    def test_get_item_returns_jewelry(self, temp_items_dir):
        """Test getting a jewelry item"""
        manager = ItemManager(temp_items_dir)
        item = manager.get_item(3)
        assert isinstance(item, Jewelry)
    
    def test_get_item_returns_simple_item(self, temp_items_dir):
        """Test getting a simple item"""
        manager = ItemManager(temp_items_dir)
        item = manager.get_item(4)
        assert isinstance(item, Item)


class TestItemManagerDictToItem:
    """Tests for dict_to_item and dti methods"""
    
    def test_dict_to_item_converts_weapon_dict(self, temp_items_dir):
        """Test converting weapon dictionary to Item object"""
        manager = ItemManager(temp_items_dir)
        weapon_dict = {
            "id": 100,
            "name": "Test Weapon",
            "item_type": "weapon",
            "_": "weapon",
            "rare": "uncommon",
            "cost": 150,
            "description": "Test description",
            "emoji": "⚔️",
            "stacked": False,
            "slot": 0,
            "stats": {},
            "affixes": {},
            "equip_requirements": {}
        }
        item = manager.dict_to_item(weapon_dict)
        assert item is not None
        assert isinstance(item, Weapon)
        assert item.id == 100
        assert item.name == "Test Weapon"
    
    def test_dict_to_item_converts_armor_dict(self, temp_items_dir):
        """Test converting armor dictionary to Item object"""
        manager = ItemManager(temp_items_dir)
        armor_dict = {
            "id": 101,
            "name": "Test Armor",
            "item_type": "armor",
            "_": "armor",
            "rare": "common",
            "cost": 50,
            "description": "Test armor description",
            "emoji": "🛡️",
            "stacked": False,
            "slot": "chest",
            "stats": {},
            "affixes": {},
            "equip_requirements": {}
        }
        item = manager.dict_to_item(armor_dict)
        assert item is not None
        assert isinstance(item, Armor)
        assert item.id == 101
        assert item.name == "Test Armor"
    
    def test_dict_to_item_converts_jewelry_dict(self, temp_items_dir):
        """Test converting jewelry dictionary to Item object"""
        manager = ItemManager(temp_items_dir)
        jewelry_dict = {
            "id": 102,
            "name": "Test Jewelry",
            "item_type": "jewelry",
            "_": "jewelry",
            "rare": "rare",
            "cost": 300,
            "description": "Test jewelry description",
            "emoji": "💍",
            "stacked": False,
            "slot": "ring",
            "stats": {},
            "affixes": {},
            "equip_requirements": {}
        }
        item = manager.dict_to_item(jewelry_dict)
        assert item is not None
        assert isinstance(item, Jewelry)
        assert item.id == 102
    
    def test_dict_to_item_converts_simple_item_dict(self, temp_items_dir):
        """Test converting simple item dictionary to Item object"""
        manager = ItemManager(temp_items_dir)
        item_dict = {
            "id": 103,
            "name": "Test Item",
            "item_type": "another",
            "_": "another",
            "rare": "common",
            "cost": 20,
            "description": "Test item description",
            "emoji": "📦",
            "stacked": True
        }
        item = manager.dict_to_item(item_dict)
        assert item is not None
        assert isinstance(item, Item)
        assert item.id == 103
        assert item.name == "Test Item"
    
    def test_dict_to_item_returns_none_for_missing_id(self, temp_items_dir):
        """Test that dict_to_item returns None when id is missing"""
        manager = ItemManager(temp_items_dir)
        incomplete_dict = {
            "name": "Incomplete Item",
            "item_type": "another",
            "_": "another"
        }
        item = manager.dict_to_item(incomplete_dict)
        assert item is None
    
    def test_dict_to_item_returns_none_for_missing_type(self, temp_items_dir):
        """Test that dict_to_item returns None when type is missing"""
        manager = ItemManager(temp_items_dir)
        incomplete_dict = {
            "id": 200,
            "name": "Incomplete Item",
            "item_type": "another"
        }
        item = manager.dict_to_item(incomplete_dict)
        assert item is None
    
    def test_dict_to_item_returns_none_for_unknown_type(self, temp_items_dir):
        """Test that dict_to_item returns None for unknown item type"""
        manager = ItemManager(temp_items_dir)
        unknown_dict = {
            "id": 201,
            "name": "Unknown Item",
            "item_type": "unknown",
            "_": "unknown",
            "rare": "common",
            "cost": 50,
            "description": "Unknown type",
            "emoji": "❔",
            "stacked": False
        }
        item = manager.dict_to_item(unknown_dict)
        assert item is None
    
    def test_dti_is_overload_for_dict_to_item(self, temp_items_dir):
        """Test that dti method works as overload for dict_to_item"""
        manager = ItemManager(temp_items_dir)
        item_dict = {
            "id": 104,
            "name": "Test Overload",
            "item_type": "another",
            "_": "another",
            "rare": "common",
            "cost": 25,
            "description": "Test description",
            "emoji": "📦",
            "stacked": True
        }
        item1 = manager.dict_to_item(item_dict)
        item2 = manager.dti(item_dict)
        
        assert item1 is not None
        assert item2 is not None
        assert item1.id == item2.id
        assert item1.name == item2.name


class TestItemManagerEdgeCases:
    """Tests for edge cases and error handling"""
    
    def test_item_manager_with_multiple_items_same_type(self, tmp_path):
        """Test ItemManager loading multiple items of same type"""
        weapon_dir = tmp_path / "weapon"
        armor_dir = tmp_path / "armor"
        jewelry_dir = tmp_path / "jewelry"
        another_dir = tmp_path / "another"
        
        weapon_dir.mkdir()
        armor_dir.mkdir()
        jewelry_dir.mkdir()
        another_dir.mkdir()
        
        # Create multiple weapons
        for i in range(1, 4):
            weapon_data = {
                "id": i,
                "name": f"Weapon {i}",
                "item_type": "weapon",
                "_": "weapon",
                "rare": "common",
                "cost": 100 * i,
                "description": f"Weapon {i} description",
                "emoji": "⚔️",
                "stacked": False,
                "slot": 0,
                "stats": {},
                "affixes": {},
                "equip_requirements": {}
            }
            with open(weapon_dir / f"weapon_{i}.json", "w", encoding="utf-8") as f:
                json.dump(weapon_data, f)
        
        # Create dummy files for other types
        for subdir in [armor_dir, jewelry_dir, another_dir]:
            with open(subdir / "dummy.json", "w", encoding="utf-8") as f:
                json.dump({"id": 0, "item_type": subdir.name, "_": subdir.name}, f)
        
        manager = ItemManager(tmp_path)
        assert len(manager.items) >= 3
        assert 1 in manager.items
        assert 2 in manager.items
        assert 3 in manager.items
    
    def test_item_with_all_attributes(self, temp_items_dir):
        """Test that loaded items have all required attributes"""
        manager = ItemManager(temp_items_dir)
        item = manager.get_item(1)
        
        assert hasattr(item, 'id')
        assert hasattr(item, 'name')
        assert hasattr(item, 'rarity')
        assert hasattr(item, 'cost')
        assert hasattr(item, 'description')
        assert hasattr(item, 'emoji')
    
    def test_item_equality_after_load_and_retrieve(self, temp_items_dir):
        """Test that item retrieved is the same as loaded"""
        manager = ItemManager(temp_items_dir)
        item = manager.get_item(4)
        
        assert item.id == 4
        assert item.name == "Health Potion"
        assert item.item_type == "another"
        assert item.cost == 10
        assert item.stacked is True


class TestItemManagerItemIntegrity:
    """Tests for item data integrity"""
    
    def test_item_properties_preserved_after_load(self, temp_items_dir):
        """Test that item properties are preserved after loading"""
        manager = ItemManager(temp_items_dir)
        weapon = manager.get_item(1)
        
        assert weapon.name == "Iron Sword"
        assert weapon.rarity == "common"
        assert weapon.cost == 100
        assert weapon.emoji == "⚔️"
        assert weapon.item_type == "weapon"
    
    def test_dict_to_item_preserves_all_data(self, temp_items_dir):
        """Test that dict_to_item preserves all item data"""
        manager = ItemManager(temp_items_dir)
        
        original_dict = {
            "id": 500,
            "name": "Preserved Item",
            "item_type": "another",
            "_": "another",
            "rare": "epic",
            "cost": 999,
            "description": "This data should be preserved",
            "emoji": "✨",
            "stacked": False
        }
        
        item = manager.dict_to_item(original_dict)
        
        assert item.id == original_dict["id"]
        assert item.name == original_dict["name"]
        assert item.rarity == original_dict["rare"]
        assert item.cost == original_dict["cost"]
        assert item.description == original_dict["description"]
        assert item.emoji == original_dict["emoji"]


class TestItemManagerLoggingAndErrors:
    """Tests for logging and error handling"""
    
    @patch('game.manager.item_manager.loggers')
    def test_warning_logged_for_missing_id_in_dict(self, mock_loggers, temp_items_dir):
        """Test that warning is logged when id is missing"""
        manager = ItemManager(temp_items_dir)
        incomplete_dict = {
            "name": "Test",
            "item_type": "another",
            "_": "another"
        }
        manager.dict_to_item(incomplete_dict)
        mock_loggers.game.warning.assert_called()
    
    @patch('game.manager.item_manager.loggers')
    def test_warning_logged_for_unknown_type(self, mock_loggers, temp_items_dir):
        """Test that warning is logged for unknown item type"""
        manager = ItemManager(temp_items_dir)
        unknown_dict = {
            "id": 201,
            "name": "Unknown",
            "item_type": "unknown",
            "_": "unknown"
        }
        manager.dict_to_item(unknown_dict)
        mock_loggers.game.warning.assert_called()
