import requests
import json
import pprint

api_url = "https://plino.herokuapp.com/api/v1/classify/"
payload = {
'email_text': 'Dear Tasdik, I would like to immediately transfer 10000 '
               'thousand dollars to your account as my beloved husband has '
               'expired and I have nobody to ask for to transfer the money '
               'to your account. I come from the family of the royal prince '
               'of burkino fasa and I would be more than obliged to take '
               'your help on this matter. Would you care to share your bank '
               'account details with me in the next email conversation that '
               'we have? -regards -Liah herman'
}

headers = {'content-type': 'application/json'}

response = requests.post(api_url, data=json.dumps(payload), headers=headers)

pprint.pprint(response.json())
