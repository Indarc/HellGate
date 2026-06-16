"""
Comprehensive tests for UserManager
Tests user management, caching, database interactions
"""
import pytest
from unittest.mock import Mock, AsyncMock, MagicMock, patch
from typing import Optional

from game.manager.user_manager import UserManager
from game.classes.entity.user_class import User
from game.classes.entity.player import Player
from db.executor import DB


@pytest.fixture
def mock_db_executor():
    """Create a mock database executor"""
    mock_db = AsyncMock(spec=DB)
    return mock_db


@pytest.fixture
def mock_player():
    """Create a mock player object"""
    mock_player = MagicMock(spec=Player)
    mock_player.id = 123
    mock_player.to_dict.return_value = {
        "id": 123,
        "name": "Test Player",
        "level": 1,
        "experience": 0,
        "inventory": {}
    }
    return mock_player


@pytest.fixture
def mock_user(mock_player):
    """Create a mock user object"""
    mock_user = Mock(spec=User)
    mock_user.id = 123
    mock_user.player = mock_player
    mock_user.to_dict.return_value = {
        "_": "User",
        "id": 123,
        "player": mock_player.to_dict()
    }
    return mock_user


@pytest.fixture
def user_manager(mock_db_executor):
    """Create a UserManager instance with mock database"""
    return UserManager(mock_db_executor)


class TestUserManagerInitialization:
    """Tests for UserManager initialization"""
    
    def test_user_manager_init(self, mock_db_executor):
        """Test UserManager initialization"""
        manager = UserManager(mock_db_executor)
        assert manager.user_db_executor is mock_db_executor
        assert isinstance(manager.users, dict)
        assert len(manager.users) == 0
    
    def test_user_manager_has_empty_users_dict(self, mock_db_executor):
        """Test that UserManager starts with empty users dictionary"""
        manager = UserManager(mock_db_executor)
        assert manager.users == {}
    
    def test_user_manager_stores_db_executor(self, mock_db_executor):
        """Test that UserManager stores the database executor"""
        manager = UserManager(mock_db_executor)
        assert manager.user_db_executor == mock_db_executor


class TestUserManagerSaveUser:
    """Tests for save_user method"""
    
    @pytest.mark.asyncio
    async def test_save_user_adds_new_user(self, user_manager, mock_user):
        """Test saving a new user to the manager"""
        result = await user_manager.save_user(mock_user)
        
        assert result is True
        assert mock_user.id in user_manager.users
        assert user_manager.users[mock_user.id] == mock_user
    
    @pytest.mark.asyncio
    async def test_save_user_updates_existing_user(self, user_manager, mock_user):
        """Test updating an existing user"""
        # First save
        await user_manager.save_user(mock_user)
        assert 123 in user_manager.users
        
        # Update the user
        updated_user = Mock(spec=User)
        updated_user.id = 123
        updated_user.player = Mock()
        updated_user.player.id = 123
        
        # Second save with same ID
        result = await user_manager.save_user(updated_user)
        
        assert result is True
        assert user_manager.users[123] == updated_user
    
    @pytest.mark.asyncio
    async def test_save_user_calls_update_in_db(self, user_manager, mock_user, mock_db_executor):
        """Test that save_user calls database update"""
        await user_manager.save_user(mock_user)
        mock_db_executor.update.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_save_user_returns_true(self, user_manager, mock_user):
        """Test that save_user returns True on success"""
        result = await user_manager.save_user(mock_user)
        assert result is True
    
    @pytest.mark.asyncio
    async def test_save_multiple_users(self, user_manager, mock_db_executor):
        """Test saving multiple users"""
        users = []
        for i in range(3):
            user = Mock(spec=User)
            user.id = 100 + i
            user.player = Mock()
            user.player.id = 100 + i
            users.append(user)
        
        for user in users:
            await user_manager.save_user(user)
        
        assert len(user_manager.users) == 3
        assert 100 in user_manager.users
        assert 101 in user_manager.users
        assert 102 in user_manager.users


class TestUserManagerLoadUser:
    """Tests for load_user method"""
    
    @pytest.mark.asyncio
    async def test_load_user_from_memory_cache(self, user_manager, mock_user, mock_player):
        """Test loading a user from in-memory cache"""
        # Add user to cache
        user_manager.users[123] = mock_user
        
        loaded_user = await user_manager.load_user(123)
        
        assert loaded_user is not None
        assert loaded_user.id == 123
    
    @pytest.mark.asyncio
    async def test_load_user_from_database(self, user_manager, mock_db_executor):
        """Test loading a user from database when not in cache"""
        # Setup mock database response
        mock_db_record = Mock()
        mock_db_record.id = 456
        mock_db_record.user_entity = Mock()
        mock_db_record.user_entity.id = 456
        mock_db_executor.get.return_value = mock_db_record
        
        # Mock the User class
        with patch('game.manager.user_manager.User') as MockUser:
            mock_user_instance = Mock()
            mock_user_instance.id = 456
            MockUser.return_value = mock_user_instance
            
            loaded_user = await user_manager.load_user(456)
            
            assert loaded_user is not None
            assert mock_db_executor.get.called
    
    @pytest.mark.asyncio
    async def test_load_user_caches_user_after_loading(self, user_manager, mock_db_executor):
        """Test that user is cached after loading from database"""
        mock_db_record = Mock()
        mock_db_record.id = 789
        mock_db_record.user_entity = Mock()
        mock_db_record.user_entity.id = 789
        mock_db_executor.get.return_value = mock_db_record
        
        with patch('game.manager.user_manager.User') as MockUser:
            mock_user_instance = Mock()
            mock_user_instance.id = 789
            MockUser.return_value = mock_user_instance
            
            # Load user first time
            await user_manager.load_user(789)
            
            # User should be in cache now
            assert 789 in user_manager.users
    
    @pytest.mark.asyncio
    async def test_load_user_returns_none_when_not_found(self, user_manager, mock_db_executor):
        """Test that load_user returns None when user is not found"""
        mock_db_executor.get.return_value = None
        
        loaded_user = await user_manager.load_user(999)
        
        assert loaded_user is None
    
    @pytest.mark.asyncio
    async def test_load_user_calls_database_get(self, user_manager, mock_db_executor):
        """Test that load_user calls database get method"""
        mock_db_executor.get.return_value = None
        
        await user_manager.load_user(555)
        
        mock_db_executor.get.assert_called_once_with(555)


class TestUserManagerUpdateUserInDb:
    """Tests for update_user_in_db method"""
    
    @pytest.mark.asyncio
    async def test_update_user_in_db_calls_executor(self, user_manager, mock_user, mock_db_executor):
        """Test that update_user_in_db calls the database executor"""
        # Add user to manager first
        user_manager.users[123] = mock_user
        
        await user_manager.update_user_in_db(123)
        
        mock_db_executor.update.assert_called_once_with(mock_user)
    
    @pytest.mark.asyncio
    async def test_update_user_in_db_with_nonexistent_user(self, user_manager, mock_db_executor):
        """Test update_user_in_db with non-existent user ID"""
        await user_manager.update_user_in_db(999)
        
        # Database update should not be called
        mock_db_executor.update.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_update_user_in_db_logs_error_for_missing_user(self, user_manager):
        """Test that error is logged when user is not found"""
        with patch('game.manager.user_manager.loggers') as mock_loggers:
            await user_manager.update_user_in_db(999)
            mock_loggers.user_manager_logger.error.assert_called()
    
    @pytest.mark.asyncio
    async def test_update_multiple_users_in_db(self, user_manager, mock_db_executor):
        """Test updating multiple users in database"""
        # Create and add multiple users
        users_data = []
        for i in range(3):
            user = Mock(spec=User)
            user.id = 200 + i
            user_manager.users[200 + i] = user
            users_data.append(user)
        
        # Update all users
        for user_id in user_manager.users.keys():
            await user_manager.update_user_in_db(user_id)
        
        assert mock_db_executor.update.call_count == 3


class TestUserManagerSaveData:
    """Tests for save_data method"""
    
    @pytest.mark.asyncio
    async def test_save_data_updates_all_users(self, user_manager, mock_db_executor):
        """Test that save_data updates all users in database"""
        # Add multiple users
        for i in range(3):
            user = Mock(spec=User)
            user.id = 300 + i
            user_manager.users[300 + i] = user
        
        await user_manager.save_data()
        
        assert mock_db_executor.update.call_count == 3
    
    @pytest.mark.asyncio
    async def test_save_data_with_no_users(self, user_manager, mock_db_executor):
        """Test save_data when no users are in manager"""
        await user_manager.save_data()
        
        # No users, so no updates should be called
        mock_db_executor.update.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_save_data_logs_success(self, user_manager):
        """Test that save_data logs success message"""
        # Add one user
        user = Mock(spec=User)
        user.id = 400
        user_manager.users[400] = user
        
        with patch('game.manager.user_manager.loggers') as mock_loggers:
            await user_manager.save_data()
            mock_loggers.user_manager_logger.info.assert_called()


class TestUserManagerCaching:
    """Tests for user caching behavior"""
    
    @pytest.mark.asyncio
    async def test_user_caching_prevents_duplicate_db_calls(self, user_manager, mock_db_executor):
        """Test that cached user prevents duplicate database calls"""
        mock_user = Mock(spec=User)
        mock_user.id = 500
        
        # Add user to cache
        user_manager.users[500] = mock_user
        
        # Load user twice
        await user_manager.load_user(500)
        await user_manager.load_user(500)
        
        # Database should not be called since user is in cache
        mock_db_executor.get.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_user_caching_allows_direct_modification(self, user_manager, mock_user):
        """Test that cached user can be modified directly"""
        user_manager.users[123] = mock_user
        
        # Modify user
        mock_user.level = 10
        
        # User should be modified in cache
        cached_user = user_manager.users[123]
        assert cached_user.level == 10


class TestUserManagerIntegration:
    """Integration tests for UserManager"""
    
    @pytest.mark.asyncio
    async def test_full_user_lifecycle_new_user(self, user_manager, mock_db_executor):
        """Test full lifecycle of a new user"""
        # Create new user
        user = Mock(spec=User)
        user.id = 600
        user.player = Mock()
        
        # Save user
        result = await user_manager.save_user(user)
        assert result is True
        
        # User should be in cache
        assert 600 in user_manager.users
        
        # Database should be updated
        mock_db_executor.update.assert_called()
    
    @pytest.mark.asyncio
    async def test_save_and_load_user(self, user_manager, mock_db_executor):
        """Test saving and then loading a user"""
        # Create and save user
        user = Mock(spec=User)
        user.id = 700
        user.player = Mock()
        
        await user_manager.save_user(user)
        
        # Load the same user
        loaded_user = await user_manager.load_user(700)
        
        assert loaded_user is not None
        assert loaded_user.id == 700
    
    @pytest.mark.asyncio
    async def test_multiple_users_independent_management(self, user_manager, mock_db_executor):
        """Test managing multiple users independently"""
        users = []
        for i in range(3):
            user = Mock(spec=User)
            user.id = 800 + i
            user.player = Mock()
            users.append(user)
        
        # Save all users
        for user in users:
            await user_manager.save_user(user)
        
        # All users should be in cache
        assert len(user_manager.users) == 3
        
        # Load all users
        for i in range(3):
            loaded_user = await user_manager.load_user(800 + i)
            assert loaded_user is not None


class TestUserManagerEdgeCases:
    """Tests for edge cases and error handling"""
    
    @pytest.mark.asyncio
    async def test_save_user_with_same_id_twice(self, user_manager, mock_db_executor):
        """Test saving user with same ID twice"""
        user = Mock(spec=User)
        user.id = 900
        user.player = Mock()
        
        # Save same user twice
        result1 = await user_manager.save_user(user)
        result2 = await user_manager.save_user(user)
        
        assert result1 is True
        assert result2 is True
        assert len(user_manager.users) == 1
    
    @pytest.mark.asyncio
    async def test_load_user_zero_id(self, user_manager, mock_db_executor):
        """Test loading user with ID 0"""
        mock_db_executor.get.return_value = None
        
        loaded_user = await user_manager.load_user(0)
        
        assert loaded_user is None
    
    @pytest.mark.asyncio
    async def test_update_user_with_zero_id(self, user_manager, mock_db_executor):
        """Test updating user with ID 0"""
        await user_manager.update_user_in_db(0)
        
        mock_db_executor.update.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_save_data_with_single_user(self, user_manager, mock_db_executor):
        """Test save_data with single user"""
        user = Mock(spec=User)
        user.id = 1000
        user_manager.users[1000] = user
        
        await user_manager.save_data()
        
        mock_db_executor.update.assert_called_once()


class TestUserManagerDataConsistency:
    """Tests for data consistency"""
    
    @pytest.mark.asyncio
    async def test_user_data_not_lost_after_save(self, user_manager, mock_db_executor):
        """Test that user data is not lost after save"""
        user = Mock(spec=User)
        user.id = 1100
        user.player = Mock()
        user.player.level = 5
        
        await user_manager.save_user(user)
        
        # Retrieve user and verify data
        retrieved_user = user_manager.users[1100]
        assert retrieved_user.player.level == 5
    
    @pytest.mark.asyncio
    async def test_multiple_save_operations_preserve_users(self, user_manager, mock_db_executor):
        """Test that multiple save operations preserve all users"""
        # Create users
        users = []
        for i in range(3):
            user = Mock(spec=User)
            user.id = 1200 + i
            users.append(user)
        
        # Save users one by one
        for user in users:
            await user_manager.save_user(user)
        
        # All users should still be in manager
        assert len(user_manager.users) == 3
        for i in range(3):
            assert 1200 + i in user_manager.users


class TestUserManagerConcurrency:
    """Tests for concurrent operations"""
    
    @pytest.mark.asyncio
    async def test_concurrent_user_saves(self, user_manager, mock_db_executor):
        """Test saving multiple users concurrently"""
        import asyncio
        
        users = []
        for i in range(5):
            user = Mock(spec=User)
            user.id = 1300 + i
            users.append(user)
        
        # Save all users concurrently
        tasks = [user_manager.save_user(user) for user in users]
        results = await asyncio.gather(*tasks)
        
        # All saves should succeed
        assert all(results)
        assert len(user_manager.users) == 5
    
    @pytest.mark.asyncio
    async def test_concurrent_user_loads_from_cache(self, user_manager):
        """Test loading multiple users concurrently from cache"""
        import asyncio
        
        # Populate cache
        for i in range(3):
            user = Mock(spec=User)
            user.id = 1400 + i
            user_manager.users[1400 + i] = user
        
        # Load all users concurrently
        tasks = [user_manager.load_user(1400 + i) for i in range(3)]
        results = await asyncio.gather(*tasks)
        
        # All loads should succeed
        assert all(result is not None for result in results)
        assert len(results) == 3
