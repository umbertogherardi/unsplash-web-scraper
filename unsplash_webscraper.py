# Author: Umberto Gherardi
#
# Last Updated: 3/28/2023
#
# Resources Used:
# https://youtu.be/SxaYl1XOC2U for unsplash-specific scraping techniques

import requests
from bs4 import BeautifulSoup
import os
import shutil
import threading
import time

#
# get_links: Takes an Unsplash url as an argument, generates a BeautifulSoup element from the url's webpage using requests, and searches for all 'img' links on in the BS element. 
# Returns a dictionary with a string key and an array value; the string is a given resolution, whereas the array contians all image links corresponding to the resolution. 
#
def get_links(url):

    webpage = requests.get(url)

    soup = BeautifulSoup(webpage.content, "html.parser")

    image_links = {} # empty dictionary to hold resolutions with their corresponding links

    # finding all srcset links
    for url_links in soup.findAll('img', attrs = {'srcset' : True}):
        srcset_links = url_links['srcset']
        srcset_links = srcset_links.split(',') # splitting srcset_links into an iterable list

        # loop through every srcset_link and extract the resolution and url data for that image
        for srcset_data in srcset_links:
            image_data = srcset_data.split(' ')

            link_index = 0
            resolution_index = 1

            if len(image_data) == 3: # due to html formatting, we will have some data lists with an additional empty element at the start
                image_data.pop(0) # remove the empty data

            # if our resolution is not properly formatted, skip it and continue on to th next resolution
            if not ('w' in image_data[resolution_index]):
                continue

            # if we do not have a particular resolution encoded as a key in our image_links dictionary...
            if not image_links.get(image_data[resolution_index]): 
                image_links[image_data[resolution_index]] = [] # ... set-up that key by giving it an empty array value
            
            image_links[image_data[resolution_index]].append(image_data[link_index]) # for a given resolution key, append a corresponding link to it's array in the dictionary

    return image_links

#
# download_image: Downloads a image urls to a specified folder. Image urls are named as follows: image<download_number>.jpg
#
def download_image(url, index):
    with requests.get(url) as r:
        with open(f"{folder}/image{index}.jpg", "wb") as f:
            f.write(r.content)

    print(f"image{index} downloaded")

#
# download_with_threads: Given a two-dimensional urls list, we loop through each url in a group of urls and start a new thread that calls download_image on that url. Allows
# for parallelized image downloading which speeds up download time.
#
def download_with_threads(urls_list):
    threads = []
    index = 1
    for urls in urls_list:
        for url in urls:
            t = threading.Thread(target=download_image, args=(url, index))
            threads.append(t)
            index += 1

    for thread in threads:
        thread.start()

#
# Our main method; calls the previously declared functions to scrape one or severl Unsplash photos pages.
#
if __name__ == '__main__':

    folder = "unsplash" # setting the name of the folder the images will be downloaded to

    if os.path.exists(folder): # if the folder already exists, we'll recursively delete it 
        shutil.rmtree(folder)

    os.mkdir(folder) # creating a fresh folder for our images

    base_url = "https://unsplash.com/s/photos/" # the base url required to scrape Unsplash photos

    search_list = [] # a list to hold all the phrases a user would like to scrape images for
    requested_urls = [] # a list to hold all the image urls returned from get_links()
 
    search_count = int(input("How many phrases would you like to search for? Phrase count: ")) # prompting the user for the number of phrases they'd like to search for

    for i in range(search_count): # prompt the user for the specified number of search phrases
        search = input(f"Enter search phrase #{i+1}: ")
        search_list.append(search)

    for search_item in search_list: 
        search_query_url = base_url + '-'.join(search_item.split(' ')) # converting the user search phrase into the url for the webpage that needs to be scraped

        links = get_links(search_query_url) # store the image links for a given search url into a list

        print(f"Available resolutions for '{search_item}':")

        for resolution in links: # for each resolution key in our links dictionary, print all available resolutions and prompt the user to select a resolution from the list
            print(resolution)
        resolution_selection = input(f"Please choose a resolution for '{search_item}': ")

        while not (resolution_selection in links.keys()): # continue prompting the user for resolutions if they enter in a resolution that does not exist
            print("Invalid resolution entered. Please choose from the following list of resolutions:")
            for resolution in links:
                print(resolution)
            resolution_selection = input(f"Please choose a resolution for '{search_item}': ")

        print(f"Number of images available: {len(links[resolution_selection])}")

        image_count = int(input(f"Enter the number of images you'd like to download for '{search_item}': "))
        requested_urls.append(links[resolution_selection][:image_count]) # add the specified number of images from a given link's resolution to the list of urls to download

    download_with_threads(requested_urls) # call download_threads() on the specified image urls
