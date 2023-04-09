"""
This file is use to crawl and download the CMU kitchens dataset
Link to the webpage: http://kitchen.cs.cmu.edu/
"""

import os
import time
import argparse
import shutil

import numpy as np
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import wget

parser = argparse.ArgumentParser()
parser.add_argument(
    '--link',
    default='http://kitchen.cs.cmu.edu/main.php',
    help='Link to the webpage containing data'
)
parser.add_argument(
    '--dir',
    default=os.path.join(os.getcwd(), 'videos'),
    help='Path to the directory where data is to be downloaded'
)
args = parser.parse_args()


def unzip_del(zip_file):
    dest_dir = os.path.splitext(zip_file)[0]
    if not os.path.isdir(dest_dir):
        print('[INFO] Creating {}...'.format(dest_dir))
        os.mkdir(dest_dir)
        print('[INFO] Unzipping {}'.format(zip_file))
        shutil.unpack_archive(zip_file, dest_dir)
        print('[INFO] Deleting {}...'.format(zip_file))
        os.remove(zip_file)
    else:
        print('[INFO] Files for {} already extracted...'.format(zip_file))
    return None


req = Request(args.link)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

download_link = 'http://kitchen.cs.cmu.edu/{}'

for link in links:
    if link is not None:
        if '.zip' in link and 'Video' in link:
            activity = link.split('_')[1]
            activity_dir = os.path.join(args.dir, activity)
            if os.path.isdir(activity_dir):
                pass
            else:
                os.mkdir(activity_dir)

            file_path = os.path.join(activity_dir, link.split('/')[-1])
            dir_path = os.path.splitext(file_path)[0]

            if os.path.isdir(dir_path):
                print('[INFO] {} exists...'.format(link))
                pass
            else:
                print('[INFO] Downloading {}...'.format(link))
                download_link_ = download_link.format(link)
                wget.download(download_link_, activity_dir)
                unzip_del(file_path)
                time.sleep(np.random.randint(2, 15))
