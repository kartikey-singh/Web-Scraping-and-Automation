import os
import requests
import random
import requests
import shutil
import urllib.request
import json
from lxml import html
from bs4 import BeautifulSoup

'''
A Gift to Remember (2017) [WEBRip] [1080p] English

A Gift to Remember (2017)

IMDB...............: https://www.imdb.com/title/tt7006938/
FORMAT.............: MP4
CODEC..............: X264 
GENRE..............: Drama / Romance
FILE SIZE..........: 1.48 GB
RESOLUTION.........: 1920*1072
FRAME RATE.........: 23.976 fps
AUDIO..............: AAC 2CH
LANGUAGE...........: English 
RUNTIME............: 1hr 30 min
'''

URL = "https://yts.lt/rss/0/all/all/0"
PATH = 'movies/'
HEADERS = ['IMDB...............:', 'FORMAT.............:',
           'CODEC..............:', 'GENRE..............:', 'FILE SIZE..........:',
           'RESOLUTION.........:', 'FRAME RATE.........:', 'AUDIO..............:',
           'LANGUAGE...........:', 'RUNTIME............:']


def get_links(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'xml')

    movie_links = set()

    for link in soup.find_all('link'):
        movie_links.add(link.text)

    links = []
    for link in movie_links:
        links.append(link)

    return links


def file_exists(path):
    return os.path.exists(path) is not True


def xpath_to_string(tree, xpath):
    data = tree.xpath(xpath)
    data_string = ''.join(data)
    return data_string.strip()


def download_torrent(file_url, filepath):
    if file_exists(filepath):
        r = requests.get(file_url, stream=True)
        with open(filepath, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def is_empty(data):
    if data:
        return True
    return False


def upload(link):
    APIKey = "27a82cb936a91b3eaf9e020a20c608d9"
    format_type = "json"
    url = "http://extraimage.com/api/1/upload/?key=" + \
        APIKey + "&source=" + link + "&format=" + format_type
    r = requests.post(url)
    json_data = json.loads(r.text)
    return json_data['image']['url_viewer']


def process(tree, title, year, movie_path, imdb_link, genre):
    format_movie = 'MP4'
    codec = 'X264'
    audio = 'AAC 2CH'
    file_paths = []
    # movie_type = xpath_to_string(
    #     tree, '//*[@id="movie-info"]/p/a[1]/text()')
    index = 1
    while True:
        movie_type = xpath_to_string(
            tree, '//*[@id= "movie-tech-specs"]/span[' + str(index) + ']/text()')
        if is_empty(movie_type):
            i = str(index)
            movie_type = xpath_to_string(
                tree, '//*[@id= "movie-tech-specs"]/span[' + i + ']/text()')
            file_size = xpath_to_string(
                tree, '//*[@id = "movie-tech-specs"]/div[' + i + ']/div[1]/div[1]/text()')
            resolution = xpath_to_string(
                tree, '//*[@id="movie-tech-specs"]/div[' + i + ']/div[1]/div[2]/text()')
            frame_rate = xpath_to_string(
                tree, '//*[@id="movie-tech-specs"]/div[' + i + ']/div[2]/div[2]/text()')
            language = xpath_to_string(
                tree, '//*[@id="movie-tech-specs"]/div[' + i + ']/div[1]/div[3]/text()')
            runtime = xpath_to_string(
                tree, '//*[@id="movie-tech-specs"]/div[' + i + ']/div[2]/div[3]/text()')

            data = (imdb_link, format_movie, codec, genre, file_size,
                    resolution, frame_rate, audio, language, runtime)

            torrent_link = xpath_to_string(
                tree, '// *[@id="movie-info"]/div[2]/p/a[' + i + ']/@href')
            torrent_text = xpath_to_string(
                tree, '// *[@id="movie-info"]/div[2]/p/a[' + i + ']/text()')

            try:
                types = movie_type.split('.')
                if types[1] == "WEB":
                    types[1] = "WEBRip"
                if types[1] == "BLU":
                    types[1] = "BLURay"

                types_t = torrent_text.split('.')
                if types_t[1] == "WEB":
                    types_t[1] = "WEBRip"
                if types_t[1] == "BLU":
                    types_t[1] = "BLURay"

                main_heading = title + \
                    ' (' + year + ') [' + types[1] + \
                    '] [' + types[0] + '] ' + language

                sub_heading = title + ' (' + year + ')'

                torrent_heading = title + \
                    ' (' + year + ') [' + types_t[1] + \
                    '] [' + types_t[0] + '] [YTS.LT]'

                torrent_path = movie_path + '/' + torrent_heading + '.torrent'

                if file_exists(torrent_path):
                    download_torrent(torrent_link, torrent_path)

                zipped = zip(HEADERS, data)
                file_path = movie_path + "/" + main_heading + ".txt"
                if file_exists(file_path):
                    with open(file_path, 'w') as fp:
                        fp.write(main_heading + "\n\n")
                        fp.write(sub_heading + "\n\n")
                        fp.write(''.join('%s %s\n' %
                                         x for x in zipped))

                    file_paths.append(file_path)
            except:
                print(
                    "Couldn't download torrent and it's details after : ", main_heading)
        else:
            break
        index = index + 1
    return file_paths


def get_data(links):
    for link in links:
        try:
            page = requests.get(link)
            tree = html.fromstring(page.content)
            title = xpath_to_string(
                tree, '//*[@id="mobile-movie-info"]/h1/text()')

            if len(title) is not 0:
                imdb_link = xpath_to_string(
                    tree, '//*[@id="movie-info"]/div[2]/div[2]/a/@href')
                genre = xpath_to_string(
                    tree, '//*[@id = "mobile-movie-info"]/h2[2]/text()')
                year = xpath_to_string(
                    tree, '//*[@id = "movie-info"]/div[1]/h2[1]/text()')

                movie_path = PATH + title + ' ' + year

                if file_exists(movie_path):
                    os.mkdir(movie_path)

                file_paths = process(
                    tree, title, year, movie_path, imdb_link, genre)

                img_file_count = len([f for f in os.listdir(movie_path)
                                      if f.endswith('.jpg') and os.path.isfile(os.path.join(movie_path, f))])

                if img_file_count != 3:
                    # Image Download
                    image_urls = [
                        # xpath_to_string(tree, '//*[@id = "movie-poster"]/img/@src'),
                        xpath_to_string(
                            tree, '//*[@id = "screenshots"]/div[1]/a[2]/img/@src'),
                        xpath_to_string(
                            tree, '//*[@id="screenshots"]/div[2]/a/img/@src'),
                        xpath_to_string(tree, '//*[@id="screenshots"]/div[3]/a/img/@src')]

                    for index, image in enumerate(image_urls):
                        image = image.replace('medium', 'large')

                        num = random.randrange(10**14, 10**15 - 1, 3)
                        image_path = movie_path + "/" + str(num) + ".jpg"
                        try:
                            if file_exists(image_path):
                                urllib.request.urlretrieve(image, image_path)
                                image_link = upload(image)
                                for file_path in file_paths:
                                    with open(file_path, 'a') as fp:
                                        fp.write("\n" + image_link + "\n")

                        except:
                            print("Couldn't download image: ", index)

        except Exception as e:
            print(e)
            print("Couldn't download :", link)


LINKS = get_links(URL)
get_data(LINKS)
