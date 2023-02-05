import json
from bs4 import BeautifulSoup
import urllib
import re
import requests
import os
from collections import Counter



def find_images():
    # content of URL
    url = "https://www.cfcunderwriting.com"
    html_page = requests.get(url)

    # Parse HTML Code
    soup = BeautifulSoup(html_page.text, 'html.parser')

    # find all images in URL
    images = []
    for img in soup.findAll('img'):
        #print(img.get('src'), "\n")
        #if url in img.get('src'):
         #   print("Image from page\n")
        #else:
        src = img.get('src')
        if src and src.startswith(("http", "https")):
            images.append(src)
    print(images)

    scripts = []
    # find all scripts in URL
    for script in soup.findAll('script'):
        src = script.get("src")
        if src and src.startswith(("http", "https")) and not(url in src):
            scripts.append(src)
    print("\n \n \n External Scripts here:")
    print(scripts, "\n")


if __name__ == '__main__':
    find_images()
