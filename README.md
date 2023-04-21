# IntegrationGateway
ZenDesk-Jira Gateway

// Собрать имейдж
docker build -t integration_gw_img:tag_name .

// Запустить с Docker HUB
docker run --name gw_cont -it --env-file env.list -p 9991:9991 palamiko/integration-gateway
