import argparse
from urllib.parse import urlparse
from pydantic import BaseModel
import time
import requests
import threading
from multiprocessing import Process
import asyncio
import aiohttp


class PhotoUrl(BaseModel):
    url: str
    file: str


default_urls = [
    'https://i.pinimg.com/originals/17/83/6b/17836b7698244921e54d21f449512edd.jpg',
    'https://kupidonia.ru/content/puzzle/photo/big/261_1.jpg',
    'https://w.forfun.com/fetch/0e/0e1ea0a0b976ed8316835e9ad0bcde1b.jpeg',
    'https://thypix.com/wp-content/uploads/2018/05/Sommerlandschaft-Bilder-23.jpg',
    'https://www.ceskymac.cz/wp-content/uploads/2017/04/papers.co-no28-sea-tree-purple-sky-nature-3840x2400.jpg'
]


def time_count(func):
    def wrapper():
        t_start = time.time()
        func()
        t_end = time.time()
        print(f'Method {func.__name__} was executed in {t_end - t_start:.02} seconds')
    return wrapper


def write_file(path, data):
    with open(path, 'wb') as file:
        file.write(data)


def sync_download(photo: PhotoUrl):
    response = requests.get(photo.url)
    if response.status_code == 200:
        write_file(photo.file, response.content)
    else:
        print(f'Unable to download from {photo.url}, got http:{response.status_code}')


async def async_download(photo: PhotoUrl):
    async with aiohttp.ClientSession() as session:
        async with session.get(photo.url) as response:
            data = await response.read()
            write_file(photo.file, data)


@time_count
def sync_code():
    for url in urls:
        sync_download(url)


@time_count
def thread_code():
    threads = []
    for url in urls:
        thread = threading.Thread(target=sync_download, args=[url])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


@time_count
def multiprocess_code():
    procs = []
    for url in urls:
        proc = Process(target=sync_download, args=[url])
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()


async def async_main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(async_download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


@time_count
def async_code():
    loop = asyncio.get_event_loop()  # method deprecated
    loop.run_until_complete(async_main())


def urls_parse(strings: list[str]) -> list[PhotoUrl]:
    """
    Parse url list to PhotoUrl objects that contain url and file name
    :param strings: list of urls to parse
    :return: list of parsed PhotoUrl objects
    :raises: ValueError: on incorrect URL
    """
    result = list()
    for url_str in strings:
        url = urlparse(url_str)
        if url.scheme not in ['http', 'https']:
            raise ValueError(f"Incorrect url '{url_str}'")
        _file_name = url.path.split('/')[-1]
        file_name = _file_name if _file_name.count('?') else _file_name.split('?')[0]
        result.append(PhotoUrl(url=url_str, file=file_name))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download photos from URL list")
    parser.add_argument('urls', action='extend', nargs='*', help="URL картинки, можно указать несколько")
    args: argparse.Namespace = parser.parse_args()

    try:
        urls = urls_parse(args.urls) if args.urls else urls_parse(default_urls)
    except ValueError as e:
        exit(e)
    sync_code()
    thread_code()
    multiprocess_code()
    async_code()
