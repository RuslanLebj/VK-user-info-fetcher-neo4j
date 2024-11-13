# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы конфигурации Poetry в контейнер
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости через Poetry
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Копируем остальные файлы проекта
COPY . /app

# Открываем порт 80
EXPOSE 80

# Запускаем скрипт vk_info.py при запуске контейнера
CMD ["python", "src/main.py"]

