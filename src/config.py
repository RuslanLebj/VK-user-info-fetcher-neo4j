import os
import logging

# Конфигурации логирования
# Устанавливает уровень логирования и формат вывода логов
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Константы для настройки API ВКонтакте и базы данных Neo4j

# VK API Token: токен для аутентификации запросов к API ВКонтакте
VK_API_TOKEN = os.getenv("VK_API_TOKEN")

# Версия API ВКонтакте, используемая в запросах
VK_API_VERSION = "5.199"

# Базовый URL для запросов к API ВКонтакте
VK_API_BASE_URL = "https://api.vk.com/method/"

# URI для подключения к базе данных Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")

# Имя пользователя для доступа к базе данных Neo4j
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")

# Пароль для доступа к базе данных Neo4j
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Максимальное количество элементов, которое будет запрашиваться у API ВКонтакте
# Значение ограничивает количество подписчиков и подписок, чтобы избежать перегрузки данных
MAX_ITEMS = 10

# Максимальная глубина обработки данных
# Определяет количество уровней, до которого будет происходить рекурсивный сбор данных
MAX_DEPTH = 2

# ID пользователя ВКонтакте по умолчанию, используемого для запуска анализа
DEFAULT_USER_ID = os.getenv("VK_USER_ID", "1")
