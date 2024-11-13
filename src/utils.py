def show_query_results(results):
    print("\n--- Результаты запросов ---\n")

    print(f"Всего пользователей: {results['total_users']}")
    print(f"Всего групп: {results['total_groups']}")

    print("\nТоп-5 пользователей по количеству фолловеров:")
    for i, record in enumerate(results['top_users_by_followers'], 1):
        print(f"  {i}. User ID: {record['user_id']}, Followers Count: {record['followers_count']}")

    print("\nТоп-5 самых популярных групп:")
    for i, record in enumerate(results['top_popular_groups'], 1):
        print(f"  {i}. Group ID: {record['group_id']}, Subscribers Count: {record['subscribers_count']}")

    print("\nВзаимные фолловеры:")
    if results['mutual_followers']:
        for record in results['mutual_followers']:
            print(f"  User1 ID: {record['user1_id']} ↔ User2 ID: {record['user2_id']}")
    else:
        print("  Нет взаимных фолловеров.")