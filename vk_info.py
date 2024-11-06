import requests
import os
import logging
from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Константы
VK_API_TOKEN = os.getenv("VK_API_TOKEN")
VK_API_VERSION = "5.199"
VK_API_BASE_URL = "https://api.vk.com/method/"
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")
MAX_ITEMS = 10  # Максимальное количество подписчиков и подписок для обработки
DEFAULT_USER_ID = os.getenv(
    "VK_USER_ID", "1"
)  # ID пользователя по умолчанию, если не указан в .env


# Функция для выполнения запросов к VK API с обработкой ошибок
def request_vk_api(method, params):
    try:
        response = requests.get(f"{VK_API_BASE_URL}{method}", params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        if "error" in data:
            logger.error(f"Ошибка VK API: {data['error']}")
            return None
        return data
    except requests.RequestException as e:
        logger.error(f"Ошибка запроса к VK API: {e}")
        return None


# Функция для получения информации о пользователе
def get_vk_user_info(user_id):
    params = {
        "user_ids": user_id,
        "access_token": VK_API_TOKEN,
        "v": VK_API_VERSION,
        "fields": "followers_count,city,sex",
    }
    return request_vk_api("users.get", params)


# Функция для получения ограниченного количества подписчиков пользователя
def get_vk_user_followers(user_id):
    params = {
        "user_id": user_id,
        "access_token": VK_API_TOKEN,
        "v": VK_API_VERSION,
        "count": MAX_ITEMS,  # Ограничиваем количество подписчиков
    }
    return request_vk_api("users.getFollowers", params)


# Функция для получения ограниченного количества подписок пользователя
def get_vk_user_subscriptions(user_id):
    params = {
        "user_id": user_id,
        "access_token": VK_API_TOKEN,
        "v": VK_API_VERSION,
        "count": MAX_ITEMS,  # Ограничиваем количество подписок
    }
    return request_vk_api("users.getSubscriptions", params)


# Функция для сохранения данных в Neo4j
def save_to_neo4j(driver, user_info, followers, subscriptions):
    try:
        with driver.session() as session:
            user_data = user_info["response"][0]
            user_id = user_data["id"]
            user_name = (
                f"{user_data.get('first_name', '')} {user_data.get('last_name', '')}"
            )
            city = user_data.get("city", {}).get("title", "Unknown")
            sex = "Male" if user_data.get("sex") == 2 else "Female"

            # Создаем узел для пользователя
            session.run(
                "MERGE (u:User {id: $id}) "
                "SET u.screen_name = $screen_name, u.name = $name, u.sex = $sex, u.city = $city",
                id=user_id,
                screen_name=user_data.get("screen_name", ""),
                name=user_name,
                sex=sex,
                city=city,
            )
            logger.info(f"Узел для пользователя {user_id} создан.")

            # Создаем связи для подписчиков
            for follower in followers.get("response", {}).get("items", []):
                session.run(
                    "MERGE (f:User {id: $follower_id}) " "MERGE (f)-[:FOLLOWS]->(u)",
                    follower_id=follower,
                    u_id=user_id,
                )
            logger.info(f"Связи подписчиков для пользователя {user_id} созданы.")

            # Создаем связи для подписок
            for subscription in subscriptions.get("response", {}).get("groups", []):
                session.run(
                    "MERGE (g:Group {id: $group_id, name: $group_name}) "
                    "MERGE (u)-[:SUBSCRIBES_TO]->(g)",
                    group_id=subscription["id"],
                    group_name=subscription["name"],
                    u_id=user_id,
                )
            logger.info(f"Связи подписок для пользователя {user_id} созданы.")

    except Neo4jError as e:
        logger.error(f"Ошибка при сохранении данных в Neo4j: {e}")


def main():
    # Используем `DEFAULT_USER_ID` из переменной окружения, если она задана
    user_id = os.getenv("VK_USER_ID", DEFAULT_USER_ID)
    user_info = get_vk_user_info(user_id)
    if not user_info:
        logger.error("Не удалось получить информацию о пользователе.")
        return

    followers = get_vk_user_followers(user_id)
    if followers is None:
        logger.error("Не удалось получить подписчиков пользователя.")
        return

    subscriptions = get_vk_user_subscriptions(user_id)
    if subscriptions is None:
        logger.error("Не удалось получить подписки пользователя.")
        return

    # Подключение к Neo4j
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        save_to_neo4j(driver, user_info, followers, subscriptions)
        logger.info(f"Данные для пользователя {user_id} успешно сохранены в Neo4j.")
    except Neo4jError as e:
        logger.error(f"Ошибка подключения к Neo4j: {e}")
    finally:
        driver.close()


if __name__ == "__main__":
    main()
