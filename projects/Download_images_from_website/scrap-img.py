from selenium import webdriver
import requests as rq
import os
from bs4 import BeautifulSoup
import time
import html
import urllib.parse

# path= E:\web scraping\chromedriver_win32\chromedriver.exe
path = input("Enter Path : ").strip()
url = input("Enter URL : ").strip()

output = "output"


def get_url(path, url):
    driver = webdriver.Chrome(executable_path=r"{}".format(path))
    driver.get(url)
    print("loading.....")
    res = driver.execute_script("return document.documentElement.outerHTML")

    return res


def get_img_links(res):
    soup = BeautifulSoup(res, "lxml")
    imglinks = soup.find_all("img", src=True)
    return imglinks


def download_img(img_link, index):
    try:
        extensions = [".jpeg", ".jpg", ".png", ".gif"]
        extension = ".jpg"
        for exe in extensions:
            if img_link.find(exe) > 0:
                extension = exe
                break

        img_data = rq.get(img_link, timeout=10).content
        # Sanitize output path
        output_path = os.path.join(os.getcwd(), output)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Sanitize filename
        filename = str(index + 1) + extension
        filename = urllib.parse.quote_plus(filename)
        filepath = os.path.join(output_path, filename)

        with open(filepath, "wb+") as f:
            f.write(img_data)

    except rq.exceptions.RequestException as e:
        print(f"Error downloading image {img_link}: {e}")
        pass


try:
    # Sanitize input directory
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(os.getcwd()):
        raise ValueError("Invalid directory")

    # Validate URL
    parsed_url = urllib.parse.urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise ValueError("Invalid URL")

    result = get_url(path, url)
    time.sleep(60)
    img_links = get_img_links(result)

    for index, img_link in enumerate(img_links):
        img_link = img_link["src"]
        print("Downloading...")
        if img_link:
            img_link = html.escape(img_link)
            download_img(img_link, index)

    print("Download Complete!!")

except Exception as e:
    print(f"Error: {e}")
