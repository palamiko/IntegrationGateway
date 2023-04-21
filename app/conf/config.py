from aiohttp import BasicAuth
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "IntegrationGateway"

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
