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


    fonts = set()
    # find all fonts in URL
    for link in soup.find_all("link", rel="stylesheet"):
        link_url = link.get("href")
        if link_url.startswith(("http", "https")):
            response = requests.get(link_url)
            style_content = response.text
            #print("Style Content printing: \n", style_content)
            font_face_rules = re.findall(r"@font-face\s*{.*?}", style_content, re.DOTALL)
            #print("\n \n Font Face Rules Printing:", font_face_rules)
            for rule in font_face_rules:
                #print("rule is: ", rule)
                #print("only url: ", re.findall(r"url\(([^\)]+)\)", rule, re.MULTILINE))
                fonts.update(re.findall(r"font-family: \'([^\)]+)\'", rule, re.MULTILINE))
    fonts = list(fonts)
    print(fonts)


if __name__ == '__main__':
    find_images()
