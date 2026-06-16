# Pytest Тесты для ItemManager и UserManager

## 📋 Что было создано

Созданы comprehensive pytest тесты для двух ключевых компонентов системы:

### 1. **ItemManager Tests** 
   📍 Файл: `tests/test_items/test_item_manager_comprehensive.py`
   - **25 тестов** покрывающих всю функциональность
   - Проверка загрузки предметов из JSON файлов
   - Получение предметов по ID
   - Конвертация словарей в объекты предметов
   - Обработка всех типов: Weapon, Armor, Jewelry, Item
   - Обработка ошибок и логирование

### 2. **UserManager Tests**
   📍 Файл: `tests/test_player/test_user_manager_comprehensive.py`
   - **33 теста** покрывающих все операции
   - Сохранение пользователей
   - Загрузка из памяти и БД
   - Кэширование
   - Обновление в БД
   - Конкурентные операции
   - Целостность данных

### 3. **Shared Configuration**
   📍 Файл: `tests/conftest.py`
   - Общие фиксчуры для всех тестов
   - Примеры данных (fixtures)
   - Конфигурация pytest
   - Event loop для async тестов

---

## 🚀 Быстрый старт

### Установка зависимостей

```bash
cd src
# Установить все зависимости из requirements.txt
py -m pip install -r requirements.txt

# ИЛИ минимум для тестов:
py -m pip install pytest pytest-asyncio
```

### Запуск всех тестов

```bash
# Из корня проекта
py -m pytest tests/ -v
```

### Запуск ItemManager тестов

```bash
py -m pytest tests/test_items/test_item_manager_comprehensive.py -v
```

### Запуск UserManager тестов

```bash
py -m pytest tests/test_player/test_user_manager_comprehensive.py -v
```

---

## 📊 Структура тестов

### ItemManager - 25 тестов

```
TestItemManagerInitialization (4)
├── test_item_manager_init_with_valid_path
├── test_item_manager_loads_items_on_init
└── test_item_manager_item_classes_mapping

TestItemManagerGetItem (6)
├── test_get_item_returns_item_by_id
├── test_get_item_returns_none_for_nonexistent_id
├── test_get_item_returns_weapon
├── test_get_item_returns_armor
├── test_get_item_returns_jewelry
└── test_get_item_returns_simple_item

TestItemManagerDictToItem (8)
├── test_dict_to_item_converts_weapon_dict
├── test_dict_to_item_converts_armor_dict
├── test_dict_to_item_converts_jewelry_dict
├── test_dict_to_item_converts_simple_item_dict
├── test_dict_to_item_returns_none_for_missing_id
├── test_dict_to_item_returns_none_for_missing_type
├── test_dict_to_item_returns_none_for_unknown_type
└── test_dti_is_overload_for_dict_to_item

TestItemManagerEdgeCases (3)
├── test_item_manager_with_multiple_items_same_type
├── test_item_with_all_attributes
└── test_item_equality_after_load_and_retrieve

TestItemManagerItemIntegrity (2)
├── test_item_properties_preserved_after_load
└── test_dict_to_item_preserves_all_data

TestItemManagerLoggingAndErrors (2)
├── test_warning_logged_for_missing_id_in_dict
└── test_warning_logged_for_unknown_type
```

### UserManager - 33 теста

```
TestUserManagerInitialization (3)
├── test_user_manager_init
├── test_user_manager_has_empty_users_dict
└── test_user_manager_stores_db_executor

TestUserManagerSaveUser (5)
├── test_save_user_adds_new_user
├── test_save_user_updates_existing_user
├── test_save_user_calls_update_in_db
├── test_save_user_returns_true
└── test_save_multiple_users

TestUserManagerLoadUser (5)
├── test_load_user_from_memory_cache
├── test_load_user_from_database
├── test_load_user_caches_user_after_loading
├── test_load_user_returns_none_when_not_found
└── test_load_user_calls_database_get

TestUserManagerUpdateUserInDb (4)
├── test_update_user_in_db_calls_executor
├── test_update_user_in_db_with_nonexistent_user
├── test_update_user_in_db_logs_error_for_missing_user
└── test_update_multiple_users_in_db

TestUserManagerSaveData (3)
├── test_save_data_updates_all_users
├── test_save_data_with_no_users
└── test_save_data_logs_success

TestUserManagerCaching (2)
├── test_user_caching_prevents_duplicate_db_calls
└── test_user_caching_allows_direct_modification

TestUserManagerIntegration (3)
├── test_full_user_lifecycle_new_user
├── test_save_and_load_user
└── test_multiple_users_independent_management

TestUserManagerEdgeCases (4)
├── test_save_user_with_same_id_twice
├── test_load_user_zero_id
├── test_update_user_with_zero_id
└── test_save_data_with_single_user

TestUserManagerDataConsistency (2)
├── test_user_data_not_lost_after_save
└── test_multiple_save_operations_preserve_users

TestUserManagerConcurrency (2)
├── test_concurrent_user_saves
└── test_concurrent_user_loads_from_cache
```

---

## 🔍 Примеры команд

### Запуск одного класса тестов
```bash
py -m pytest tests/test_items/test_item_manager_comprehensive.py::TestItemManagerGetItem -v
```

### Запуск одного конкретного теста
```bash
py -m pytest tests/test_items/test_item_manager_comprehensive.py::TestItemManagerGetItem::test_get_item_returns_item_by_id -v
```

### Запуск с подробным выводом (с print statements)
```bash
py -m pytest tests/ -v -s
```

### Запуск с отчётом о покрытии кода
```bash
py -m pip install pytest-cov
py -m pytest tests/ -v --cov=src/game/manager --cov-report=html
```

### Запуск с более подробным выводом ошибок
```bash
py -m pytest tests/ -v --tb=long
```

### Запуск параллельно (ускорение)
```bash
py -m pip install pytest-xdist
py -m pytest tests/ -v -n auto
```

### Запуск только быстрых тестов
```bash
py -m pytest tests/ -v -m "not slow"
```

---

## 🧪 Типы тестов

### Unit Tests
- Тестирование отдельных методов в изоляции
- Использование Mock объектов
- Быстрое выполнение

### Integration Tests
- Тестирование взаимодействия компонентов
- Проверка работы с реальными файлами (для ItemManager)
- Проверка кэширования и БД операций

### Edge Cases Tests
- Обработка нулевых значений
- Отсутствующие данные
- Неизвестные типы
- Конкурентные операции

---

## 📝 Фиксчуры (Fixtures)

### ItemManager Fixtures

```python
# Временная директория с JSON предметами
@pytest.fixture
def temp_items_dir(tmp_path):
    # Создаёт структуру:
    # weapon/sword.json
    # armor/leather.json
    # jewelry/ring.json
    # another/potion.json
```

### UserManager Fixtures

```python
# Mock БД executor
@pytest.fixture
def mock_db_executor():
    return AsyncMock(spec=DB)

# Mock Player
@pytest.fixture
def mock_player():
    return MagicMock(spec=Player)

# Mock User
@pytest.fixture
def mock_user(mock_player):
    return Mock(spec=User)

# UserManager с mock БД
@pytest.fixture
def user_manager(mock_db_executor):
    return UserManager(mock_db_executor)
```

### Shared Fixtures (conftest.py)

```python
# Sample данные
sample_item_dict
sample_weapon_dict
sample_armor_dict
sample_user_dict

# Утилиты
mock_logger
event_loop (для async тестов)
```

---

## 🎯 Покрытие функциональности

### ItemManager
- ✅ Загрузка предметов из JSON файлов
- ✅ Кэширование предметов в памяти
- ✅ Получение предметов по ID
- ✅ Конвертация словарей в объекты
- ✅ Поддержка всех типов предметов
- ✅ Обработка ошибок
- ✅ Логирование

### UserManager
- ✅ Сохранение пользователей
- ✅ Загрузка пользователей
- ✅ Кэширование в памяти
- ✅ Обновление в БД
- ✅ Сохранение всех пользователей
- ✅ Обработка ошибок
- ✅ Логирование
- ✅ Конкурентные операции

---

## 🔧 Возможные проблемы и решения

### Ошибка: "ModuleNotFoundError: No module named 'aiogram'"
```bash
# Решение: Установить зависимости
cd src
py -m pip install -r requirements.txt
```

### Ошибка: "No module named 'pytest_asyncio'"
```bash
# Решение:
py -m pip install pytest-asyncio
```

### Тесты медленные
```bash
# Решение: Запустить параллельно
py -m pip install pytest-xdist
py -m pytest tests/ -n auto
```

---

## 📚 Дополнительные ресурсы

- [Pytest документация](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Pytest fixtures](https://docs.pytest.org/en/stable/fixtures.html)

---

## 📄 Файлы

- `tests/test_items/test_item_manager_comprehensive.py` - 25 тестов ItemManager
- `tests/test_player/test_user_manager_comprehensive.py` - 33 теста UserManager
- `tests/conftest.py` - Конфигурация и общие фиксчуры
- `TESTS_DOCUMENTATION.md` - Подробная документация
- `pytest.ini` - Конфигурация pytest

---

## ✨ Особенности

### ItemManager Tests
- 📁 Использует временные директории (pytest `tmp_path`)
- 📄 Создаёт реальные JSON файлы
- 🔄 Тестирует полный цикл загрузки
- 🎯 Проверяет целостность данных

### UserManager Tests
- 🔐 Использует Mock объекты (изоляция от БД)
- ⚡ Поддерживает async/await
- 🔄 Проверяет кэширование
- 🚀 Поддерживает конкурентные операции
- 📊 Тестирует целостность данных

---

## 🎓 Примеры использования

### Пример 1: Базовый запуск
```bash
py -m pytest tests/test_items/test_item_manager_comprehensive.py -v
```

### Пример 2: С фильтром
```bash
py -m pytest tests/ -v -k "save_user"
```

### Пример 3: С отчётом
```bash
py -m pytest tests/ -v --html=report.html
```

### Пример 4: Параллельно
```bash
py -m pytest tests/ -v -n 4
```

---

## 👨‍💻 Автор
Тесты созданы с помощью GitHub Copilot

**Дата создания:** 16 июня 2026 г.

---

Удачи в тестировании! 🎉
