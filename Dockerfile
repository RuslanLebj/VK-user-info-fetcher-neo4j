# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 80
EXPOSE 80

# Запускаем скрипт vk_info.py при запуске контейнера
CMD ["python", "vk_info.py"]

