import argparse
from urllib.parse import urlparse
from pydantic import BaseModel


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
    print(urls)
