# Author: Umberto Gherardi
#
# Last Updated: 3/21/2023
#
# Resources Used:
# https://youtu.be/SxaYl1XOC2U for unsplash-specific scraping techniques

import requests
from bs4 import BeautifulSoup
import os
import shutil
import threading
import time
from selenium import webdriver


def get_links(url):

    webpage = requests.get(url)

    soup = BeautifulSoup(webpage.content, "html.parser")

    image_links = {}

    # finding all srcset links
    for url_links in soup.findAll('img', attrs = {'srcset' : True}):
        srcset_links = url_links['srcset']
        srcset_links = srcset_links.split(',') # splitting srcset_links into an iterable list

        # loop through every srcset_link and extract the resolution and url data for that image
        for srcset_data in srcset_links:
            image_data = srcset_data.split(' ')

            link_index = 0
            resolution_index = 1

            if len(image_data) == 3: # due to formatting, we will have some data lists with an additional empty element at the start
                image_data.pop(0) # remove the empty data

            if not image_links.get(image_data[resolution_index]):
                image_links[image_data[resolution_index]] = []
            
            image_links[image_data[resolution_index]].append(image_data[link_index])

    return image_links


def download_image(url, index):
    with requests.get(url) as r:
        with open(f"{folder}/image{index}.jpg", "wb") as f:
            f.write(r.content)

    print(f"image{index} downloaded")


def initialize_threads(urls):
    threads = []
    index = 1
    for url in urls:
        t = threading.Thread(target= download_image, args=(url, index))
        threads.append(t)
        index += 1

    for thread in threads:
        thread.start()


def start_download(urls):
    initialize_threads(urls)
    

if __name__ == '__main__':

    folder = "unsplash"

    if os.path.exists(folder):
        shutil.rmtree(folder)

    os.mkdir(folder)

    base_url = "https://unsplash.com/s/photos/"

    search = input("Enter search phrase: ")

    search_query_url = base_url + '-'.join(search.split(' '))

    links = get_links(search_query_url)

    print("Available resolutions:")
    for resolution in links:
        print(resolution)
    resolution_selection = input("Please choose a resolution: ")

    print(f"Number of images available: {len(links[resolution_selection])}")

    image_count = int(input("Enter the number of images you'd like to download: "))
    requested_urls = links[resolution][:image_count]

    start_download(requested_urls)
