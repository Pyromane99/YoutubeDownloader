import os
from youtubesearchpython import SearchVideos
import music_tag
import requests
import shutil
from PyLyrics import *


def search(artist, song):
    search = artist + " " + song + " audio"
    return SearchVideos(search, offset=1, mode="dict", max_results=2).result()


def get_url(research):
    return research["search_result"][0]["link"]


def download_artwork(research):
    artwork_url = research["search_result"][0]["thumbnails"][4]
    r = requests.get(artwork_url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open("output.jpg", 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def download_song(url):
    os.system("youtube-dl -f bestaudio -o output.webm " + url)


def to_mp3(file_name, new_file_name):
    os.system("ffmpeg -i " + file_name + " " + new_file_name)
    os.system("rm " + file_name)


def delete_space(string):
    tab = string.split()
    new_string = ""
    for a in tab:
        new_string += a
        new_string += "_"
    return new_string


def tag_music(file, artist, name, album):
    song = music_tag.load_file(file)
    song["tracktitle"] = name
    song["album"] = album
    song["artist"] = artist
    with open("output.jpg", "rb") as image:
        song["artwork"] = image.read()
    with open("output.jpg", "rb") as image:
        song.append_tag('artwork', image.read())
    song.save()
    os.system("rm output.jpg")



def total(title, artist, album):
    format_title = delete_space(title)
    format_artist = delete_space(artist)
    file_name = format_title + format_artist
    file_name = file_name[:-1] + ".mp3"

    research = search(artist, title)
    download_artwork(research)
    url = get_url(research)
    download_song(url)
    to_mp3("output.webm", file_name)
    tag_music(file_name, artist, title, album)



cond = True
while cond:
    print("----------------------------------------------------------------------------------------------------------")
    title = input("Titre de la musique (pour arrêter passer): ")
    if title == "":
        cond = False
        break
    artist = input("Artiste de la musique : ")
    album = input("Album de la musique : ")
    total(title, artist, album)
