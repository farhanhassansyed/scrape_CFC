import json
from bs4 import BeautifulSoup
import re
import requests
import os


def find_PP():
    # content of URL
    url = "https://www.cfcunderwriting.com"
    html_page = requests.get(url)

    # Parse HTML Code
    soup = BeautifulSoup(html_page.text, 'html.parser')

    # Find all the <a> tags
    links = soup.find_all('a')

    # Iterate over the links and look for the "Privacy Policy" page
    privacy_policy_link = None
    for link in links:
        if "Privacy Policy" in link.text:
            privacy_policy_link = link["href"]
            break

    # Print the location of the "Privacy Policy" page
    if privacy_policy_link:
        privacy_policy_link = url + privacy_policy_link
        print("The Privacy Policy page is located at:", privacy_policy_link)
    else:
        print("No Privacy Policy page was found.")

    # Return link
    return privacy_policy_link

def create_dict(clean_list):
    word_count = {}
    for word in clean_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

     # Serializing json
    json_object = json.dumps(word_count, indent=4)

    # Writing to words_freq.json
    print("Creating words_freq.json ...")
    with open("words_freq.json", "w") as outfile:
        outfile.write(json_object)

def clean_wordlist(wordlist):
    clean_list = []
    for word in wordlist:
        symbols = "!@#$%^&*()_-+={[}]|/\;:\"<>?/., "
        for i in range(len(symbols)):
            word = word.replace(symbols[i], '')
        if len(word) > 0:
            clean_list.append(word)
    # Create Dictionary and write results to json
    create_dict(clean_list)

def scrape_PP():
    # Look for location of Privacy Policy in the URL
    url = find_PP() # "https://www.cfcunderwriting.com/en-gb/support/privacy-policy/"

    # Check whether Privacy Policy link exists
    if not(url):
        print("Could not find Privacy Policy")
        return

    worldlist = []
    html_page = requests.get(url)

    # Parse HTML Code
    soup = BeautifulSoup(html_page.text, 'html.parser')
    for each_text in soup.findAll('main', attrs={"class": "individual-content"}):
        content = each_text.text
        words = content.lower().split()
        for each_word in words:
            worldlist.append(each_word)
        # get rid of symbols, create a dictionary and write to json
        clean_wordlist(worldlist)

def add_to_json(images, scripts, fonts):

    # Data to be written
    dictionary = {}
    dictionary['Images'] = images
    dictionary['Scripts'] = scripts
    dictionary['Fonts'] = fonts

    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to .json
    print("Creating external_resources.json ...")
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
        src = img.get('src')
        # Uncomment part below to filter out external images
        if src: # and src.startswith(("http", "https")) and not(src.startswith(url)):
            images.append(src)
    #print("\n Images: \n", images)

    scripts = []
    # find all scripts in URL
    for script in soup.findAll('script'):
        src = script.get("src")
        if src and src.startswith(("http", "https")) and not(url in src):
            scripts.append(src)
    #print("\n Scripts here: \n", scripts)


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
    fonts = list(fonts) # Convert set to list
    #print("Fonts: ", fonts)

    add_to_json(images,scripts,fonts)

if __name__ == '__main__':
    find_resources() # 2
    scrape_PP() # 3 and 4
    print("Scraping Completed Successfully!")
