import os
import re
import urllib.request
from os import listdir
from os.path import isfile, join

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# current directory path
dir_path = os.path.dirname(os.path.realpath(__file__))

# website url & send get request to url
url = 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/kenkou_iryou/shokuhin/yunyu_kanshi/index_00017.html'
response = requests.get(url)

# read in the url via the "BeautifulSoup"
soup = BeautifulSoup(response.text, 'html.parser')

# filter the HTML object for links
link_objs = soup.find_all('a', href=re.compile('/content'))

# collect existing files to existing_files list
existing_files = []
for f in listdir(join(dir_path, "data")):
    if isfile(join(dir_path, "data", f)):
        existing_files.append(f)

# keep xls files only if they don t exist
list_with_xls = []
for link in link_objs:
    # ex link = <a href="/content/000782851.pdf">PDF</a>
    file = link.attrs.get("href").split("/")[2]  # '/content/000782851.pdf' -> 000782851.pdf
    if file.endswith('.xls') and file not in existing_files:
        list_with_xls.append(file)

if list_with_xls:  # if list_with_xls is not empty
    for xls in tqdm(list_with_xls):
        url = f'https://www.mhlw.go.jp/content/{xls}'
        # download xls files from url
        urllib.request.urlretrieve(url, os.path.join(dir_path, "data", xls))
