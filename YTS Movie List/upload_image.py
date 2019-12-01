#coding=utf-8
import requests
import json
import mimetypes
import glob
import datetime


def upload(link):
    APIKey = "27a82cb936a91b3eaf9e020a20c608d9"
    format_type = "json"    
    url = "http://extraimage.com/api/1/upload/?key=" + APIKey + "&source=" + link + "&format=" + format_type        
    r = requests.post(url)
    json_data = json.loads(r.text)
    # return json_data
    return json_data['image']['url_viewer']


def formatSource(filename):
    imageList = []
    type_extension = mimetypes.guess_type(filename)[0]
    # print(type_extension)
    imageList.append(('source', (filename, open(filename, 'rb'), type_extension)))
    # print(imageList)
    return imageList


if __name__ == "__main__":
    link = "https://us.123rf.com/450wm/oldwhitewolf/oldwhitewolf1703/oldwhitewolf170300003/72976213-vector-illustration-of-star-icon-flat-imae-on-the-orange-bakground-.jpg?ver=6"
    print(upload(link))


    # file_path = 'movies/Ma 2019'
    # images = glob.glob(file_path + '/*.jpg')
    # for img in images:
        # print(img)
        # k = upload(formatSource(img))
        # print(k)
    
