import datetime

import jwt
from extra_settings.models import Setting
import requests

from conf.settings import ESKIZ_LOGIN, ESKIZ_PASSWORD


class EskizService:
    DOMAIN = 'https://notify.eskiz.uz'

    @staticmethod
    def generate_auth_sms(code: str):
        return f"El-xizmati ilovasiga kirish uchun bir martalik kod: {code}. Uni hech kim bilan ulashmang."

    def send_sms(self, phone_number: str, message: str):
        url = f"{self.DOMAIN}/api/message/sms/send"
        token = self.fetch_token()
        payload = {
            'mobile_phone': phone_number,
            'message': message,
            'from': '4546',
        }
        headers = {
            "Authorization": f"Bearer {token}",
        }
        return requests.request("POST", url, headers=headers, data=payload)

    def fetch_token(self):
        current_token = Setting.get("ESKIZ_ACCESS_TOKEN", default="")
        if current_token not in ['', None]:
            if self.is_token_expired(current_token):
                return self.generate_token()
            else:
                return current_token
        else:
            return self.generate_token()

    def generate_token(self):
        url = f"{self.DOMAIN}/api/auth/login"
        payload = {
            'email': ESKIZ_LOGIN,
            'password': ESKIZ_PASSWORD
        }
        response = requests.request("POST", url, data=payload)
        if response.status_code != 200:
            # todo need set sentry
            pass
        token = response.json().get('data', {}).get("token")
        Setting.objects.update_or_create(
            name="ESKIZ_ACCESS_TOKEN",
            defaults={"value": token}
        )
        return token

    @staticmethod
    def is_token_expired(access_token):

        algorithm = jwt.get_unverified_header(access_token).get('alg')
        decoded_token = jwt.decode(
            jwt=access_token, verify=False, algorithms=algorithm, options={"verify_signature": False})
        exp_timestamp = decoded_token.get('exp')

        # Токен недействителен, если в нем не указано время истечения срока действия
        if not exp_timestamp:
            return True

        exp_datetime = datetime.datetime.fromtimestamp(exp_timestamp, tz=datetime.timezone.utc)
        now_datetime = datetime.datetime.now(tz=datetime.timezone.utc)

        return now_datetime >= exp_datetime
