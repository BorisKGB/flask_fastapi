import threading
from multiprocessing import Process
import asyncio
import aiohttp
import requests
import time
from urls import urls

"""
Задание №1
🐀 Написать программу, которая считывает список из 10 URL-
адресов и одновременно загружает данные с каждого
адреса.
🐀 После загрузки данных нужно записать их в отдельные
файлы.
🐀 Используйте потоки.
Задание №2
🐀 Используйте процессы.
Задание №3
🐀 Используйте асинхронный подход.
"""


def download(url):
    response = requests.get(url)
#    print(response.status_code)


def timed(func):
    def wrapper():
        t_start = time.time()
        func()
        t_end = time.time()
        print(t_end - t_start)
    return wrapper


@timed
def synced():
    for url in urls:
        download(url)


@timed
def threaded():
    threads = []
    for url in urls:
        thread = threading.Thread(target=download, args=[url])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


@timed
def processes():
    procs = []
    for url in urls:
        proc = Process(target=download, args=[url])
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()


async def async_download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            # print(response.status)

async def async_main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(async_download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)

@timed
def w_async():
    loop = asyncio.get_event_loop()  # method deprecated
    loop.run_until_complete(async_main())


if __name__ == '__main__':
    synced()
    threaded()
    processes()
    w_async()
