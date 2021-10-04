import requests
from datetime import date

BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
ID_GRUPO_BECD = '-1001381864619'
today = date.today().strftime('%a')

if today == 'Thu':
    msg = "Lembrem-se de marcar presença em Gestão de Qualidade no Moodle"

    requests.get(url=f'https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage?chat_id={ID_GRUPO_BECD}&text={msg}')