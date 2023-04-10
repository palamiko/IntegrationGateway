from aiohttp import BasicAuth
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    url_jira: str = ''
    url_zd: str = ''
    headers: dict = {"Accept": "application/json", "Content-Type": "application/json"}
    login_jira: str = ''
    pass_jira: str = ''

    def jira_auth(self):
        return BasicAuth(self.login_jira, self.pass_jira)


settings = Settings()
