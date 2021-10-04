import requests
from datetime import date
import random

BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
ID_GRUPO_BECD = '-1001381864619'
today = date.today().strftime('%a')


frases = [
        'Bom dia, familia!!',
        'Acordar foi a pior decisão que você tomou hoje. Bom dia!',
        'Ainda não é dia de glória, continuemos na luta. Bom dia!',
        'Cansei, não sou obrigado a dar bom dia todo dia não'
    ]

msg = random.choice(frases)

requests.get(url=f'https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage?chat_id={ID_GRUPO_BECD}&text={msg}')