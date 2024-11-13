import requests
from config import VK_API_BASE_URL, VK_API_TOKEN, VK_API_VERSION, MAX_ITEMS, logger


def vk_api_request(method, params):
    """
    Выполняет запрос к VK API.
    """
    params["access_token"] = VK_API_TOKEN
    params["v"] = VK_API_VERSION
    response = requests.get(VK_API_BASE_URL + method, params=params)
    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            logger.error(f"VK API error: {data['error']}")
            return None
        return data.get("response")
    else:
        logger.error(f"HTTP error: {response.status_code} - {response.text}")
        return None


def get_user_data(user_id):
    """
    Получает данные пользователя по его ID.
    """
    params = {
        "user_ids": user_id,
        "fields": "first_name,last_name,sex,home_town,city,screen_name",
    }
    return vk_api_request("users.get", params)


def get_followers(user_id):
    """
    Получает ID подписчиков пользователя.
    """
    params = {"user_id": user_id, "count": MAX_ITEMS}
    return vk_api_request("users.getFollowers", params)


def get_followers_info(follower_ids):
    """
    Получает информацию о подписчиках по их ID.
    """
    params = {
        "user_ids": ",".join(map(str, follower_ids)),
        "fields": "first_name,last_name,sex,home_town,city,screen_name",
    }
    return vk_api_request("users.get", params)


def get_subscriptions(user_id):
    """
    Получает список подписок пользователя.
    """
    params = {"user_id": user_id, "count": MAX_ITEMS, "extended": 1}
    return vk_api_request("users.getSubscriptions", params)


def get_groups_info(group_ids):
    """
    Получает информацию о группах по их ID.
    """
    params = {"group_ids": ",".join(map(str, group_ids)), "fields": "name,screen_name"}
    return vk_api_request("groups.getById", params)
