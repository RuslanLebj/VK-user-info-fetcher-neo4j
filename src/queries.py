from config import logger
from neo4j_db import driver


def execute_query(query):
    """
    Выполняет запрос к Neo4j и возвращает результат.
    """
    with driver.session() as session:
        result = session.run(query)
        return [record for record in result]


def get_total_users():
    """
    Возвращает общее количество пользователей.
    """
    query = "MATCH (u:User) RETURN count(u) AS total_users"
    result = execute_query(query)
    total_users = result[0]["total_users"] if result else 0
    logger.info(f"Total Users retrieved.")
    return total_users


def get_total_groups():
    """
    Возвращает общее количество групп.
    """
    query = "MATCH (g:Group) RETURN count(g) AS total_groups"
    result = execute_query(query)
    total_groups = result[0]["total_groups"] if result else 0
    logger.info(f"Total Groups retrieved.")
    return total_groups


def get_top_5_users_by_followers():
    """
    Возвращает топ-5 пользователей по количеству фолловеров.
    """
    query = """
    MATCH (u:User)<-[:Follow]-(follower:User)
    RETURN u.id AS user_id, count(follower) AS followers_count
    ORDER BY followers_count DESC
    LIMIT 5
    """
    result = execute_query(query)
    logger.info("Top 5 Users by Followers retrieved.")
    return result


def get_top_5_popular_groups():
    """
    Возвращает топ-5 самых популярных групп по количеству подписчиков.
    """
    query = """
    MATCH (g:Group)<-[:Subscribe]-(u:User)
    RETURN g.id AS group_id, count(u) AS subscribers_count
    ORDER BY subscribers_count DESC
    LIMIT 5
    """
    result = execute_query(query)
    logger.info("Top 5 Popular Groups retrieved.")
    return result


def get_mutual_followers():
    """
    Возвращает всех пользователей, которые являются фолловерами друг друга.
    """
    query = """
    MATCH (u1:User)-[:Follow]->(u2:User), (u2)-[:Follow]->(u1)
    RETURN u1.id AS user1_id, u2.id AS user2_id
    """
    result = execute_query(query)
    logger.info("Mutual Followers retrieved.")
    return result
