import time
import requests

#from config.settings import APPLIKATOR_TENANT, APPLIKATOR_BASE_URL, APPLIKATOR_USERNAME, APPLIKATOR_PASSWORD
APPLIKATOR_TENANT = APPLIKATOR_BASE_URL = APPLIKATOR_USERNAME = APPLIKATOR_PASSWORD = None

class TokenManager:
    def __init__(self):
        self._token_expiry_time = None
        self._token = None
        self._refresh_token = None
        self.base_url = APPLIKATOR_BASE_URL + '/security/authentication'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logout()

    def get_token(self):
        if self._token_expiry_time is None or time.time() > self._token_expiry_time:
            if self._token is None or (self._refresh_token_expiry_time is not None and time.time() > self._refresh_token_expiry_time):
                self.retrieve_initial_token()
            else:
                self._refresh_token()
        return self._token

    def set_token(self, token, refresh_token, expiry_duration, refresh_token_expiry_duration):
        self._token = token
        self._token_expiry_time = time.time() + expiry_duration
        self._refresh_token = refresh_token
        self._refresh_token_expiry_time = time.time() + refresh_token_expiry_duration

    def retrieve_initial_token(self):
        login_url = self.base_url + '/login'
        payload = {
            "userNameOrEMail": APPLIKATOR_USERNAME,
            "password": APPLIKATOR_PASSWORD,
            "tenantDomainName": APPLIKATOR_TENANT
        }
        response = requests.post(login_url, json=payload)
        if response.status_code == 200:
            json_response = response.json()
            token = json_response.get("errorOrValue", {}).get("value", {}).get("token")
            refresh_token = json_response.get("errorOrValue", {}).get("value", {}).get("refreshTokenInfo", {}).get("token")
            expiry_duration = self.calculate_expiry_duration(json_response)
            refresh_token_expiry_duration = self.calculate_refresh_token_expiry_duration(json_response)
            if token and refresh_token and expiry_duration and refresh_token_expiry_duration:
                self.set_token(token, refresh_token, expiry_duration, refresh_token_expiry_duration)
            else:
                raise Exception("Token, refresh token, or expiry duration not found in initial login response")
        else:
            raise Exception("Initial token retrieval failed")
    
    def refresh_token(self):
        refresh_token_url = self.base_url + '/loginWithRefreshToken'
        payload = {
            "tenantDomainName": "<tenant>",
            "refreshToken": self._refresh_token,
            "issueRefreshToken": True
        }
        response = requests.post(refresh_token_url, json=payload)
        if response.status_code == 200:
            json_response = response.json()
            token = json_response.get("errorOrValue", {}).get("value", {}).get("token")
            new_refresh_token = json_response.get("errorOrValue", {}).get("value", {}).get("refreshTokenInfo", {}).get("token")
            expiry_duration = self.calculate_expiry_duration(json_response)
            refresh_token_expiry_duration = self.calculate_refresh_token_expiry_duration(json_response)
            if token and new_refresh_token and expiry_duration and refresh_token_expiry_duration:
                self.set_token(token, new_refresh_token, expiry_duration, refresh_token_expiry_duration)
            else:
                raise Exception("Token, refresh token, or expiry duration not found in refresh token response")
        else:
            raise Exception("Token refresh failed")

    def calculate_expiry_duration(self, response):
        expiry_time = response.get("errorOrValue", {}).get("value", {}).get("expiresIn")
        if expiry_time:
            expiry_timestamp = time.mktime(time.strptime(expiry_time, "%Y-%m-%dT%H:%M:%S.%f%z"))
            current_timestamp = time.time()
            return expiry_timestamp - current_timestamp
        else:
            raise Exception("Expiry duration not found in response")
        
    def calculate_refresh_token_expiry_duration(self, response):
        expiry_time = response.get("errorOrValue", {}).get("value", {}).get("refreshTokenInfo", {}).get("expiresIn")
        if expiry_time:
            expiry_timestamp = time.mktime(time.strptime(expiry_time, "%Y-%m-%dT%H:%M:%S.%f%z"))
            current_timestamp = time.time()
            return expiry_timestamp - current_timestamp
        else:
            raise Exception("Refresh token expiry duration not found in response")
        
    def logout(self):
        logout_url = self.base_url + '/logout'
        payload = {
            "logoutAllSessions": {
                "value": True
            }
        }
        response = requests.post(logout_url, json=payload)
        if response.status_code == 200:
            # Reset token and expiry time after successful logout
            self._token = None
            self._refresh_token = None
            self._token_expiry_time = None
            self._refresh_token_expiry_time = None
        else:
            raise Exception("Logout failed")