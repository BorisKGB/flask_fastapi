# Задание
* Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
* Например URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
* Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
* Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
* Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.

# Usage

## Basic usage
Use `-h` to get help page

`$ python3 ./url_downloader.py`
Will download 5 files and measure download time

## examples
```
$ python3 ./url_downloader.py 'https://i.pinimg.com/originals/17/83/6b/17836b7698244921e54d21f449512edd.jpg' 'https://thypix.com/wp-content/uploads/2018/05/Sommerlandschaft-Bilder-23.jpg'
Method sync_code was executed in 0.83 seconds
Method thread_code was executed in 1.2 seconds
Method multiprocess_code was executed in 0.54 seconds
Method async_code was executed in 0.5 seconds
```
