import requests
from django.conf import settings

class Paystack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co"
    def verify_payment(self,ref,*args, **kwargs):
        path = f"/transaction/verify/{ref}"
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        url = self.base_url + path
        response = requests.get(url, headers=headers)
        if requests.status_code == 200:
            response_data =  response.json()
            if response_data.get("data"):
                return True, response_data['data']
            return False, response_data.get('message, "No data found"')
        return False, "Failed to verify payment"
      