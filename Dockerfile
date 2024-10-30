# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем необходимые пакеты
RUN pip install requests

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта в контейнер
COPY vk_info.py /app/
COPY .env /app/

# Запускаем приложение
ENTRYPOINT ["python", "vk_info.py"]
