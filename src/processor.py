from config import logger
from vk_api import (
    get_user_data,
    get_followers,
    get_followers_info,
    get_subscriptions,
    get_groups_info,
)
from neo4j_db import driver, save_user, save_group, create_relationship


def process_user(user_id, depth, max_depth):
    """
    Обрабатывает пользователя, его подписчиков и подписки, сохраняя их в базе данных.
    """
    queue = [(user_id, depth)]
    visited = set()

    while queue:
        current_id, current_depth = queue.pop(0)

        if current_id in visited or current_depth > max_depth:
            continue
        visited.add(current_id)

        user_data = get_user_data(current_id)
        if not user_data:
            logger.warning(f"Не удалось получить данные для пользователя {current_id}")
            continue
        user_info = user_data[0]

        with driver.session() as session:
            session.execute_write(save_user, user_info)
            logger.info(
                f"Добавлен пользователь {user_info['id']} на глубине {current_depth}"
            )

            followers_data = get_followers(current_id)
            if followers_data and "items" in followers_data:
                follower_ids = followers_data["items"]
                followers_info = get_followers_info(follower_ids)
                for follower in followers_info:
                    if follower["id"] not in visited:
                        session.execute_write(save_user, follower)
                        session.execute_write(
                            create_relationship, follower["id"], current_id, "Follow"
                        )
                        queue.append((follower["id"], current_depth + 1))

            subscriptions_data = get_subscriptions(current_id)
            if subscriptions_data and "items" in subscriptions_data:
                user_group_ids = [
                    sub["id"]
                    for sub in subscriptions_data["items"]
                    if sub.get("type") == "page"
                ]
                if user_group_ids:
                    groups_info = get_groups_info(user_group_ids)

                    if isinstance(groups_info, dict) and "groups" in groups_info:
                        for group in groups_info["groups"]:
                            if isinstance(group, dict) and "id" in group:
                                if group["id"] not in visited:
                                    session.execute_write(save_group, group)
                                    session.execute_write(
                                        create_relationship,
                                        current_id,
                                        group["id"],
                                        "Subscribe",
                                    )
                            else:
                                logger.warning(
                                    f"Unexpected group data format within groups: {group}"
                                )
                    else:
                        logger.warning(f"Unexpected groups_info format: {groups_info}")

        logger.info(
            f"Обработка пользователя {current_id} завершена. Переход на глубину {current_depth + 1}"
        )

    logger.info("Обработка завершена.")
