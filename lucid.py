import requests
import json


class Sdk:
    def __init__(self, login_key, token='', save_token_trigger=None, base_url="https://api.leaptheory.com/v2/"):
        self.login_key = str(login_key)
        self.token = token
        self.save_token_trigger = save_token_trigger
        self.base_url = base_url

    def __get_token(self):
        if not isinstance(self.token, str) or self.token == '':
            self.__login()
        return self.token

    def __login(self):
        res = requests.post(
            self.base_url + "auth/get-token",
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'loginKey': f'{self.login_key}'
            }))

        if res.status_code == 200:
            jres = json.loads(res.text)
            if 'token' not in jres:
                raise Exception("login error: token not found")

            self.token = jres['token']
            if callable(self.save_token_trigger):
                if 'expiresIn' in jres:
                    self.save_token_trigger(self.token, ex=int(jres["expiresIn"]) - 1)
                else:
                    self.save_token_trigger(self.token)
            return self.token
        else:
            raise Exception("login error")

    def payday_score(self, request, relogin=True):
        token = self.__get_token()
        res = requests.post(
            self.base_url + "buyer/score/payday",
            headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
            data=json.dumps(request))

        if relogin and res.status_code == 401:
            self.__login()
            return self.payday_score(request, relogin=False)
        elif res.status_code == 200:
            jres = json.loads(res.text)
            if 'status' in jres and 'value' in jres and 'prob' in jres and jres['status'] == 'ok':
                return jres

        raise Exception("paydayScore error")
