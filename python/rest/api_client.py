from functools import wraps

import requests
from reqtools import RemoteApiSession
from requests import Response


def refresh_tokens_on_the_fly(request):
    @wraps(request)
    def wrapper(self, *args, **kwargs):
        resp: Response = request(self, *args, **kwargs)
        if resp.status_code == requests.codes.unauthorized:
            self.refresh_tokens()
            resp = request(self, *args, **kwargs)
        return resp

    return wrapper


class RemoteApiClient(RemoteApiSession):
    auth_api: RemoteApiSession
    access_token = None
    refresh_token = None

    def __init__(self, api_base_url, api_prefix, auth_origin, auth_prefix="/auth"):
        super().__init__(base_url=api_base_url, prefix=api_prefix)
        self.auth_api = RemoteApiSession(base_url=auth_origin, prefix=auth_prefix)


    def login(self, email, password):
        # prepare login here
        login_response = self.auth_api # login here
        login_response.raise_for_status()
        self.access_token = login_response.json()['accessToken']
        self.refresh_token = login_response.json()['refreshToken']
        return login_response

    def register_autologon(self, *args, params=None):
        params = params or {}
        # prepare register here
        auth_resp = self.auth_api # register here
        self.access_token = auth_resp.json()['logon']['accessToken']
        self.refresh_token = auth_resp.json()['logon']['refreshToken']
        return auth_resp

    def refresh_tokens(self):
        params = {
            "refreshToken": self.refresh_token
        }
        refresh_resp = self.auth_api # refresh token here
        refresh_resp.raise_for_status()
        self.access_token = refresh_resp.json()['accessToken']
        self.refresh_token = refresh_resp.json()['refreshToken']
        return refresh_resp

    @refresh_tokens_on_the_fly
    def request(self, method, url, **kwargs):
        assert self.access_token is not None, "Please login or register before the first request."

        kwargs.setdefault('headers', {})
        kwargs['headers'].setdefault('Authorization', f"Bearer {self.access_token}")
        return super().request(method, url, **kwargs)
