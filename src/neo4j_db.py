from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, logger

# Инициализация клиента Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def save_user(tx, user):
    """
    Сохраняет информацию о пользователе в базу данных Neo4j.
    """
    city = user.get("city", {}).get("title", "")
    home_town = user.get("home_town", "") or city
    tx.run(
        """
        MERGE (u:User {id: $id})
        SET u.screen_name = $screen_name,
            u.name = $name,
            u.sex = $sex,
            u.home_town = $home_town
        """,
        id=user["id"],
        screen_name=user.get("screen_name", ""),
        name=f"{user.get('first_name', '')} {user.get('last_name', '')}",
        sex=user.get("sex", ""),
        home_town=home_town,
    )


def save_group(tx, group):
    """
    Сохраняет информацию о группе в базу данных Neo4j.
    """
    tx.run(
        """
        MERGE (g:Group {id: $id})
        SET g.name = $name, g.screen_name = $screen_name
        """,
        id=group["id"],
        name=group.get("name", ""),
        screen_name=group.get("screen_name", ""),
    )


def create_relationship(tx, user_id, target_id, rel_type):
    """
    Создает связь между пользователем и целевым объектом в базе данных Neo4j.
    """
    tx.run(
        f"""
        MATCH (u:User {{id: $user_id}})
        MATCH (target {{id: $target_id}})
        MERGE (u)-[:{rel_type}]->(target)
        """,
        user_id=user_id,
        target_id=target_id,
    )
    logger.info(f"Связь {rel_type} создана между {user_id} и {target_id}")
