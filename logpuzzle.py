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

__author__ = """https://stackoverflow.com/questions/7724993/
                python-using-regex-to-find-multiple-matches-and-print-them-out
https://thispointer.com/python-how-to-remove-duplicates-from-a-list/
https://www.codespeedy.com/re-dotall-in-python/
https://guide.freecodecamp.org/python/
                            is-there-a-way-to-substring-a-string-in-python/
https://stackoverflow.com/questions/36139/how-to-sort-a-list-of-strings
Help from Jake H."""


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    print(f'Reading file: {filename}')
    pattern = r"\S+puzzle\S+"
    with open(filename, 'r') as f:
        paths = f.read()
    full_urls = []
    paths_list = list(set(re.findall(pattern, paths, re.DOTALL)))
    for path in paths_list:
        full_urls.append("https://code.google.com" + path)
    full_urls = sorted(full_urls, key=lambda url: url[-8:].lower())
    return full_urls


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    print(f'Downloading files in {dest_dir}...')
    image = urllib.request
    image_name_list = []
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        os.chdir(dest_dir)
    for idx, url in enumerate(img_urls):
        print(url)
        image.urlretrieve(url, "img" + str(idx) + ".jpg")
        image_name_list.append("img" + str(idx) + ".jpg")
    with open("index.html", "w") as f:
        f.write(f"""<html>
    <head>
        <rel="stylesheet" type="text/css" href="css/main.css" />
        <meta http-equiv="content-type" content="text/php; charset=utf-8" />

        <title>Image Revealed!</title>
    </head>

    <body>
    <h1>IMAGE REVEALED!</h1>
        <div class="Container">
            <div class="Header">

            </div>

            <div class="Main">
""")
        for image in image_name_list:
            f.write(f'<img src="{image}" />')
        f.write("""
            </div>
    </body>

    <footer>
        <div class="Footer">
            <b>Copyright - 2020</b>
        </div>
    </footer>
</html>
                """)


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
