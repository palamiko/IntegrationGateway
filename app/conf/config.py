from aiohttp import BasicAuth
from pydantic import BaseSettings

ERROR_MESSAGE = 'вы пытались выполнить операцию бизнес-процесса (В очереди) которая не действительна для ' \
                'текущего состояния запроса'


class Settings(BaseSettings):
    app_name: str = "IntegrationGateway"
    headers: dict = {"Accept": "application/json", "Content-Type": "application/json"}

    jira_url: str = ''
    jira_login: str = ''
    jira_pass: str = ''

    zendesk_url: str = ''
    zendesk_login: str = ''
    zendesk_pass: str = ''

    def jira_auth(self):
        return BasicAuth(self.jira_login, self.jira_pass)

    def zd_auth(self):
        return BasicAuth(self.zendesk_login, self.zendesk_pass)


settings = Settings()
