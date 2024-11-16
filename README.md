# folder_share


Порядок разворачивания:
1. Создать внешнюю сеть
```commandline
sudo docker network create eco-backend-network
```
2. Volume должен быть уже создать (от другого docker compose)
3. Запустить docker compose
```commandline
sudo docker compose up -d --build
```