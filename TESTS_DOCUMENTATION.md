# Документация по Pytest тестам для ItemManager и UserManager

## Обзор

В этом документе описаны comprehensive pytest тесты для двух основных менеджеров системы:
- **ItemManager** - управление игровыми предметами
- **UserManager** - управление пользователями

## Структура тестов

### 1. ItemManager Tests (`tests/test_items/test_item_manager_comprehensive.py`)

#### Тестовые классы и их назначение:

**TestItemManagerInitialization** (4 теста)
- `test_item_manager_init_with_valid_path` - проверяет инициализацию с корректным путём
- `test_item_manager_loads_items_on_init` - проверяет загрузку предметов при инициализации
- `test_item_manager_item_classes_mapping` - проверяет правильное отображение типов предметов

**TestItemManagerGetItem** (6 тестов)
- `test_get_item_returns_item_by_id` - получение предмета по ID
- `test_get_item_returns_none_for_nonexistent_id` - возврат None для несуществующего ID
- `test_get_item_returns_weapon` - проверка типа Weapon
- `test_get_item_returns_armor` - проверка типа Armor
- `test_get_item_returns_jewelry` - проверка типа Jewelry
- `test_get_item_returns_simple_item` - проверка простого Item

**TestItemManagerDictToItem** (8 тестов)
- `test_dict_to_item_converts_weapon_dict` - конвертация словаря в Weapon
- `test_dict_to_item_converts_armor_dict` - конвертация словаря в Armor
- `test_dict_to_item_converts_jewelry_dict` - конвертация словаря в Jewelry
- `test_dict_to_item_converts_simple_item_dict` - конвертация в простой Item
- `test_dict_to_item_returns_none_for_missing_id` - обработка отсутствующего ID
- `test_dict_to_item_returns_none_for_missing_type` - обработка отсутствующего типа
- `test_dict_to_item_returns_none_for_unknown_type` - обработка неизвестного типа
- `test_dti_is_overload_for_dict_to_item` - проверка метода dti

**TestItemManagerEdgeCases** (3 теста)
- `test_item_manager_with_multiple_items_same_type` - загрузка нескольких предметов одного типа
- `test_item_with_all_attributes` - проверка наличия всех атрибутов
- `test_item_equality_after_load_and_retrieve` - проверка консистентности данных

**TestItemManagerItemIntegrity** (2 теста)
- `test_item_properties_preserved_after_load` - сохранение свойств после загрузки
- `test_dict_to_item_preserves_all_data` - сохранение всех данных при конвертации

**TestItemManagerLoggingAndErrors** (2 теста)
- `test_warning_logged_for_missing_id_in_dict` - логирование ошибок
- `test_warning_logged_for_unknown_type` - логирование для неизвестных типов

**Итого: 25 тестов для ItemManager**

---

### 2. UserManager Tests (`tests/test_player/test_user_manager_comprehensive.py`)

#### Тестовые классы и их назначение:

**TestUserManagerInitialization** (3 теста)
- `test_user_manager_init` - проверка инициализации менеджера
- `test_user_manager_has_empty_users_dict` - проверка пустого словаря пользователей
- `test_user_manager_stores_db_executor` - проверка сохранения BD executor

**TestUserManagerSaveUser** (5 тестов)
- `test_save_user_adds_new_user` - сохранение нового пользователя
- `test_save_user_updates_existing_user` - обновление существующего пользователя
- `test_save_user_calls_update_in_db` - проверка вызова обновления БД
- `test_save_user_returns_true` - проверка возвращаемого значения
- `test_save_multiple_users` - сохранение нескольких пользователей

**TestUserManagerLoadUser** (5 тестов)
- `test_load_user_from_memory_cache` - загрузка из памяти
- `test_load_user_from_database` - загрузка из базы данных
- `test_load_user_caches_user_after_loading` - кэширование после загрузки
- `test_load_user_returns_none_when_not_found` - возврат None если не найден
- `test_load_user_calls_database_get` - проверка вызова БД

**TestUserManagerUpdateUserInDb** (4 теста)
- `test_update_user_in_db_calls_executor` - вызов executor для обновления
- `test_update_user_in_db_with_nonexistent_user` - обработка несуществующего пользователя
- `test_update_user_in_db_logs_error_for_missing_user` - логирование ошибок
- `test_update_multiple_users_in_db` - обновление нескольких пользователей

**TestUserManagerSaveData** (3 теста)
- `test_save_data_updates_all_users` - сохранение всех пользователей
- `test_save_data_with_no_users` - сохранение без пользователей
- `test_save_data_logs_success` - логирование успеха

**TestUserManagerCaching** (2 теста)
- `test_user_caching_prevents_duplicate_db_calls` - кэширование предотвращает дублирование запросов
- `test_user_caching_allows_direct_modification` - прямое изменение кэшированного пользователя

**TestUserManagerIntegration** (3 теста)
- `test_full_user_lifecycle_new_user` - полный жизненный цикл нового пользователя
- `test_save_and_load_user` - сохранение и загрузка
- `test_multiple_users_independent_management` - независимое управление несколькими пользователями

**TestUserManagerEdgeCases** (4 теста)
- `test_save_user_with_same_id_twice` - сохранение пользователя с одинаковым ID дважды
- `test_load_user_zero_id` - загрузка пользователя с ID 0
- `test_update_user_with_zero_id` - обновление пользователя с ID 0
- `test_save_data_with_single_user` - сохранение данных одного пользователя

**TestUserManagerDataConsistency** (2 теста)
- `test_user_data_not_lost_after_save` - данные не потеряны после сохранения
- `test_multiple_save_operations_preserve_users` - множественные операции сохранения сохраняют пользователей

**TestUserManagerConcurrency** (2 теста)
- `test_concurrent_user_saves` - одновременное сохранение пользователей
- `test_concurrent_user_loads_from_cache` - одновременная загрузка из кэша

**Итого: 33 теста для UserManager**

---

## Использование фиксчур (Fixtures)

### ItemManager тесты

```python
@pytest.fixture
def temp_items_dir(tmp_path):
    """Создание временной директории с примерами JSON предметов"""
    # Создаёт структуру:
    # - weapon/sword.json
    # - armor/leather.json
    # - jewelry/ring.json
    # - another/potion.json
```

### UserManager тесты

```python
@pytest.fixture
def mock_db_executor():
    """Mock для database executor"""
    return AsyncMock(spec=DB)

@pytest.fixture
def mock_player():
    """Mock для Player объекта"""
    return MagicMock(spec=Player)

@pytest.fixture
def mock_user(mock_player):
    """Mock для User объекта"""
    return Mock(spec=User)

@pytest.fixture
def user_manager(mock_db_executor):
    """Инстанс UserManager с mock БД"""
    return UserManager(mock_db_executor)
```

---

## Запуск тестов

### Запуск всех тестов ItemManager:
```bash
py -m pytest tests/test_items/test_item_manager_comprehensive.py -v
```

### Запуск всех тестов UserManager:
```bash
py -m pytest tests/test_player/test_user_manager_comprehensive.py -v
```

### Запуск конкретного класса тестов:
```bash
py -m pytest tests/test_items/test_item_manager_comprehensive.py::TestItemManagerGetItem -v
```

### Запуск конкретного теста:
```bash
py -m pytest tests/test_items/test_item_manager_comprehensive.py::TestItemManagerGetItem::test_get_item_returns_item_by_id -v
```

### Запуск всех тестов с отчётом о покрытии:
```bash
py -m pytest tests/ -v --cov=src/game/manager --cov-report=html
```

### Запуск с выводом print statements:
```bash
py -m pytest tests/ -v -s
```

---

## Зависимости

Убедитесь, что установлены следующие зависимости:

```bash
py -m pip install pytest pytest-asyncio
```

---

## Предусловия

### Для ItemManager тестов:
- Pytest создаёт временные директории с JSON файлами
- Не требует реальных файлов в файловой системе
- Изолированные тесты (не влияют друг на друга)

### Для UserManager тестов:
- Используются Mock объекты для изоляции от БД
- Поддерживают async/await операции
- Тесты работают параллельно благодаря AsyncMock

---

## Покрытие функциональности

### ItemManager (25 тестов):
- ✅ Инициализация с загрузкой предметов из JSON
- ✅ Получение предметов по ID
- ✅ Конвертация словарей в объекты предметов
- ✅ Поддержка всех типов предметов (Weapon, Armor, Jewelry, Item)
- ✅ Обработка ошибок (отсутствующие данные, неизвестные типы)
- ✅ Логирование ошибок
- ✅ Целостность данных

### UserManager (33 теста):
- ✅ Инициализация менеджера
- ✅ Сохранение новых и существующих пользователей
- ✅ Загрузка из памяти и БД
- ✅ Кэширование пользователей
- ✅ Обновление пользователей в БД
- ✅ Сохранение всех пользователей
- ✅ Обработка ошибок (отсутствующие пользователи)
- ✅ Логирование
- ✅ Целостность данных
- ✅ Конкурентные операции

---

## Примеры использования

### Пример 1: Проверка загрузки предметов
```python
def test_item_manager_loads_items(temp_items_dir):
    manager = ItemManager(temp_items_dir)
    assert len(manager.items) > 0
    assert manager.get_item(1).name == "Iron Sword"
```

### Пример 2: Проверка сохранения пользователя
```python
@pytest.mark.asyncio
async def test_save_user(user_manager, mock_user):
    result = await user_manager.save_user(mock_user)
    assert result is True
    assert 123 in user_manager.users
```

---

## Дополнительные ресурсы

- [Pytest документация](https://docs.pytest.org/)
- [pytest-asyncio документация](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock документация](https://docs.python.org/3/library/unittest.mock.html)

---

## Автор

Тесты созданы с использованием GitHub Copilot
Date: 2026-06-16
