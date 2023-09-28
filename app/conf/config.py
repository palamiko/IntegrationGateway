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

    proxy_url: str | None = None
    proxy_login: str | None = None
    proxy_pass: str | None = None

    def jira_auth(self):
        return BasicAuth(self.jira_login, self.jira_pass)

    def zd_auth(self):
        return BasicAuth(self.zendesk_login, self.zendesk_pass)

    def proxy_auth(self) -> BasicAuth | None:
        if self.proxy_login is not None and self.proxy_pass is not None:
            return BasicAuth(self.proxy_login, self.proxy_pass)


settings = Settings()
