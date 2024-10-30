import requests
import json
import argparse
import os
from dotenv import load_dotenv

# Получаем токен из переменной окружения и версию API, URL
load_dotenv()
VK_API_TOKEN = os.getenv("VK_API_TOKEN")
VK_API_VERSION = '5.199'
VK_API_BASE_URL = 'https://api.vk.com/method/'

def get_vk_user_info(user_id):
    params = {
        'user_ids': user_id,
        'access_token': VK_API_TOKEN,
        'v': VK_API_VERSION,
        'fields': 'followers_count'
    }
    response = requests.get(f"{VK_API_BASE_URL}users.get", params=params)
    return response.json()

def get_vk_user_followers(user_id):
    params = {
        'user_id': user_id,
        'access_token': VK_API_TOKEN,
        'v': VK_API_VERSION
    }
    response = requests.get(f"{VK_API_BASE_URL}users.getFollowers", params=params)
    return response.json()

def get_vk_user_subscriptions(user_id):
    params = {
        'user_id': user_id,
        'access_token': VK_API_TOKEN,
        'v': VK_API_VERSION
    }
    response = requests.get(f"{VK_API_BASE_URL}users.getSubscriptions", params=params)
    return response.json()

def save_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description="VK User Info Fetcher")
    parser.add_argument('--user_id', type=str, default='1', help="VK User ID (default: '1' - Павел Дуров)")
    parser.add_argument('--output', type=str, default='vk_info.json', help="Output JSON file path (default: vk_info.json)")
    args = parser.parse_args()

    user_info = get_vk_user_info(args.user_id)
    followers = get_vk_user_followers(args.user_id)
    subscriptions = get_vk_user_subscriptions(args.user_id)

    result = {
        'user_info': user_info,
        'followers': followers,
        'subscriptions': subscriptions
    }

    save_to_json(result, args.output)
    print(f"Data successfully saved to {args.output}")

if __name__ == '__main__':
    main()
