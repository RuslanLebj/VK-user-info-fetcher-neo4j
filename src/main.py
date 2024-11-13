from config import DEFAULT_USER_ID, MAX_DEPTH, logger
from processor import process_user
from neo4j_db import driver
from queries import (
    get_total_users,
    get_total_groups,
    get_top_5_users_by_followers,
    get_top_5_popular_groups,
    get_mutual_followers,
)
from utils import show_query_results


def main():
    """
    Основная функция запуска, инициирует процесс обработки пользователя.
    """
    # Запуск обработки данных
    user_id = DEFAULT_USER_ID
    process_user(user_id, 0, MAX_DEPTH)
    logger.info("Парсинг завершен.")

    # Сохранение результатов запросов в словарь
    results = {
        "total_users": get_total_users(),
        "total_groups": get_total_groups(),
        "top_users_by_followers": get_top_5_users_by_followers(),
        "top_popular_groups": get_top_5_popular_groups(),
        "mutual_followers": get_mutual_followers(),
    }

    logger.info(f"Запросы выполнены")

    show_query_results(results)

    # Закрытие подключения к базе данных
    driver.close()


if __name__ == "__main__":
    main()
