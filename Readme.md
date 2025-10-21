# Wallet API

REST API для управления кошельками с поддержкой race condition

# Запуск в docker

docker-compose up --built

# API будет доступно по http://localhost:8000
# Документация: http://localhost:8000/docs

# API endpoints

POST /api/v1/wallets - Создать кошелек
GET /api/v1/wallets/{wallet_id} - Получить баланс
POST /api/v1/wallets/{wallet_id}/operation - Операция (DEPOSIT/WITHDRAW)

# Тестирование

Через докер: docker-compose run tests

