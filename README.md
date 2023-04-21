# IntegrationGateway
ZenDesk-Jira Gateway
Прокси для методов api при интеграции jsd и zd

В сторону jsd проксируется:
- Добавление коментария
- Смена статуса тикета
- Смена приоритета

Всторону zd проксируется:
- Загрузка файлов
- Прикрепленеие файлов к коментарию


// Собрать имейдж
docker build -t integration_gw_img:tag_name .

// Запустить с Docker HUB
docker run --name gw_cont -it --env-file env.list -p 9991:9991 palamiko/integration-gateway
