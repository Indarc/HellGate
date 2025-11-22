FROM python:3.12-slim

# Установка зависимостей, включая Firefox
RUN apt-get update && \
    apt-get install -y libpq-dev gcc postgresql-client wget gnupg && \
    apt-get clean

WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипт ожидания БД
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Копируем остальные файлы
COPY . .

CMD ["sh", "-c", "/wait-for-db.sh postgres 5432 && aerich upgrade && python ."]