import requests
import threading
from multiprocessing import Process
import asyncio
import aiohttp
import time

urls = [
    'www.google.ru',
    'gb.ru',
    'ya.ru',
    'www.python.org',
    'habr.com'
]


def download(url):
    response = requests.get(url)
    print(response.status_code)


async def async_download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            print(response.status)

async def main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(async_download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

# sync
download('url')
# threading
thread = threading.Thread(target=download, args=['url'])
thread.start()
thread.join()
# multiprocessing
#  in __main__ block
process = Process(target=download, args=('url',))
process.start()
process.join()
# asyncio
#  in __main__ block
loop = asyncio.get_event_loop()  # method deprecated
loop.run_until_complete(main())
