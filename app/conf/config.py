from aiohttp import BasicAuth
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "IntegrationGateway"

    jira_url: str = 'https://support.ai-mark.info'
    jira_login: str = 'support_l3'
    jira_pass: str = 'Ya4ScWZ8'

    zendesk_url: str = 'https://turon.zendesk.com'
    zendesk_login: str = 'n.kiselev@ai-mark.ru/token'
    zendesk_pass: str = '5E6EvFz2KpPFx9nUzxcSGdliutX2ruwa5TkUVYJn'

    def jira_auth(self):
        return BasicAuth(self.jira_login, self.jira_pass)

    def zd_auth(self):
        return BasicAuth(self.zendesk_login, self.zendesk_pass)


settings = Settings()
