# VK User Info Fetcher

## Описание
Это консольное приложение для получения информации о пользователе ВКонтакте, его фолловерах, подписках и группах через VK API.

## Требования
- Python 3.8+
- VK API Token
- Docker (для контейнеризации)

## Установка и запуск

#### Скопируйте 'template.env' и переименуйте в '.env', добавьте в '.env' свой VK апи токен

### 1. Локальный запуск

#### Установка зависимостей:
```
pip install requirements.txt
```

#### Запуск программы:

```
python vk_info.py --user_id <VK_USER_ID> --output <OUTPUT_FILE_PATH>
```

### 2. Запуск в Docker

#### Сборка Docker-образа:
```
docker build -t vk_info_fetcher .
```

#### Запуск контейнера:
```
docker run --rm -v $(pwd):/app/output vk_info_fetcher --user_id <VK_USER_ID> --output /app/output/vk_info.json
```

## Результат
После выполнения программа сохранит данные в файл в формате JSON с отступами и читаемым кириллическим текстом.
В vk_info.json уже находится пример результата работы на параметрах по умолчанию.

