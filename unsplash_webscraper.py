# Author: Umberto Gherardi
#
# Last Updated: 3/23/2023
#
# Resources Used:
# https://youtu.be/SxaYl1XOC2U for unsplash-specific scraping techniques

import requests
from bs4 import BeautifulSoup
import os
import shutil
import threading
from selenium import webdriver


def get_links(url):
    webpage = requests.get(url)

    soup = BeautifulSoup(webpage.content, "html.parser")

    image_links = {}

    # finding all srcset links
    for url_links in soup.findAll('img', attrs={'srcset': True}):
        srcset_links = url_links['srcset']
        srcset_links = srcset_links.split(',')  # splitting srcset_links into an iterable list

        # loop through every srcset_link and extract the resolution and url data for that image
        for srcset_data in srcset_links:
            image_data = srcset_data.split(' ')

            link_index = 0
            resolution_index = 1

            if len(image_data) == 3:  # due to formatting, we will have some data lists with an additional empty element at the start
                image_data.pop(0)  # remove the empty data

            if not image_links.get(image_data[resolution_index]):
                image_links[image_data[resolution_index]] = []

            image_links[image_data[resolution_index]].append(image_data[link_index])

    return image_links


def download_image(url, index):
    with requests.get(url) as r:
        with open(f"{folder}/image{index}.jpg", "wb") as f:
            f.write(r.content)

    print(f"image{index} downloaded")


def initialize_threads(urls_list):
    threads = []
    index = 1
    for urls in urls_list:
        for url in urls:
            t = threading.Thread(target=download_image, args=(url, index))
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

    search_list = []
    requested_urls = []

    search_count = int(input("How many phrases would you like to search for? Phrase count: "))

    for i in range(search_count):
        search = input(f"Enter search phrase #{i+1}: ")
        search_list.append(search)

    for search_item in search_list:
        search_query_url = base_url + '-'.join(search_item.split(' '))

        links = get_links(search_query_url)

        print(f"Available resolutions for {search_item}:")
        for resolution in links:
            print(resolution)
        resolution_selection = input(f"Please choose a resolution for {search_item}: ")

        print(f"Number of images available: {len(links[resolution_selection])}")

        image_count = int(input(f"Enter the number of images you'd like to download for {search_item}: "))
        requested_urls.append(links[resolution][:image_count])

    start_download(requested_urls)
