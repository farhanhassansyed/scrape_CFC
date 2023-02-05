import json
from bs4 import BeautifulSoup
import urllib
import re
import requests
import os
from collections import Counter

def add_to_json(images, scripts, fonts):

    # Data to be written
    dictionary = {}
    dictionary['Images'] = images
    dictionary['Scripts'] = scripts
    dictionary['Fonts'] = fonts

    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open("external_resources.json", "w") as outfile:
        outfile.write(json_object)

def find_resources():
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
        if src: # and src.startswith(("http", "https")):
            images.append(src)
    print("\n Images: \n", images)

    scripts = []
    # find all scripts in URL
    for script in soup.findAll('script'):
        src = script.get("src")
        if src and src.startswith(("http", "https")) and not(url in src):
            scripts.append(src)
    print("\n Scripts here: \n", scripts)


    fonts = set()
    # find all fonts in URL
    for link in soup.find_all("link", rel="stylesheet"):
        link_url = link.get("href")
        if link_url.startswith(("http", "https")):
            response = requests.get(link_url)
            style_content = response.text
            font_face_rules = re.findall(r"@font-face\s*{.*?}", style_content, re.DOTALL)
            for rule in font_face_rules:
               fonts.update(re.findall(r"font-family: \'([^\)]+)\'", rule, re.MULTILINE))
    fonts = list(fonts)
    print("\n Fonts: ", fonts)

    add_to_json(images,scripts,fonts)

if __name__ == '__main__':
    find_resources()
