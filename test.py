import threading
import time
from requests import async
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
session.mount("https://", adapter)

url = 'https://t.me/s/mariasimakovaacl'

_time = 0


def aget(url):
    response = session.get(url)
    print(f'{_time} {response.status_code}')

while True:
    _time += 1
    thread = threading.Thread(target=aget, args=(url,))
    thread.start()
    time.sleep(0.01)


