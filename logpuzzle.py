#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U;
Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib.request
import argparse
import threading
from time import sleep

__author__ = """https://stackoverflow.com/questions/7724993/
                python-using-regex-to-find-multiple-matches-and-print-them-out
https://thispointer.com/python-how-to-remove-duplicates-from-a-list/
https://www.codespeedy.com/re-dotall-in-python/
https://guide.freecodecamp.org/python/
                            is-there-a-way-to-substring-a-string-in-python/
https://stackoverflow.com/questions/36139/how-to-sort-a-list-of-strings
https://stackoverflow.com/questions/4134019/a-good-html-skeleton
Help from Jake H. and Ybrayym A."""


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    print(f'Reading file: {filename}')
    pattern = r"\S+puzzle\S+"
    with open(filename, 'r') as f:
        file_paths = f.read()
    full_urls = []
    paths_list = list(set(re.findall(pattern, file_paths, re.DOTALL)))
    for path in paths_list:
        full_urls.append("https://code.google.com" + path)
    full_urls = sorted(full_urls, key=lambda url: url[-8:].lower())
    return full_urls


def create_dest_dir(dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        os.chdir(dest_dir)
    return dest_dir


def download_image(img_url, dest_dir):
    """
    Downloads an image into the given directory.
    Creates the directory if necessary.
    Gives the images local filenames img-baaa, img-baab, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    """
    img_name = img_url.split('/')[8]
    image_name_list = []
    image = urllib.request
    print(f'Downloading {img_name} in {dest_dir}...')
    print(img_url)
    image.urlretrieve(img_url, "img-" + img_name[-8:-4] + ".jpg")
    image_name_list.append("img-" + img_name[-8:-4] + ".jpg")
    if not os.path.isfile("index.html"):
        with open("index.html", "w") as f:
            f.write("""<html>
    <head>
        <title>Image Revealed!</title>
    </head>
    <body>
    <h1>IMAGE REVEALED!</h1>


    </body>
    <footer>
        <div class="Footer">
            <b>Copyright - 2020</b>
        </div>
    </footer>
</html>""")
    else:
        with open('index.html', 'r') as f:
            data = f.readlines()
            for image in image_name_list:
                data[6] += f'<img src="{image}" />,'
        with open('index.html', 'w') as f:
            f.writelines(data)


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument(
        'logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    dest_dir = create_dest_dir(parsed_args.todir)

    if parsed_args.todir:
        threads = []
        for img_url in img_urls:
            t = threading.Thread(target=download_image, args=[
                img_url, dest_dir])
            t.start()
            sleep(.05)
            threads.append(t)
        for thread in threads:
            thread.join()
        with open('index.html', 'r') as f:
            data = f.readlines()
            img_data = data[7].split(",")
            img_data.sort(key=lambda chars: chars[-11:-8].lower())
            data[7] = "".join(img_data)
        with open('index.html', 'w') as f:
            f.writelines(data)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
