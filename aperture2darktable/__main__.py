# Copyright 2019 Martin Sivak
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from docopt import docopt
import os.path
import pprint
import shutil
import unicodedata
from . import library
from . import xmp

DOC = """
Usage: aperture2darktable [options] <library> <dest>

Options:
  --relative  Use relative symlinks (breaks when links are moved)
  --copy      Copy files
"""

args = docopt(DOC)
print(args)

def try_copy(src, dest):
    global link_method
    try:
        shutil.copyfile(src, dest)
    except Exception as e:
        print(e)

def try_hardlink(src, dest):
    global link_method
    try:
        os.link(src, dest)
    except Exception as e:
        print(e)
        link_method = try_copy
        link_method(src, dest)

def try_symlink(src, dest):
    global link_method
    try:
        if args["--relative"]:
            start_path = os.path.dirname(dest)
            src = os.path.relpath(src, start=start_path)
        os.symlink(src, dest)
    except Exception as e:
        print(e)
        link_method = try_none
        link_method(src, dest)

def try_none(src, dest):
    pass

if args["--copy"]:
    link_method = try_copy
elif args["--relative"]:
    link_method = try_symlink
else:
    link_method = try_hardlink

def process_folder(f, d, path):
    print((d * 2 * " ") + "- " + f.name)
    if not os.path.exists(path):
        os.makedirs(path)
        
    for photo in f.photos:
        dest = os.path.join(path, photo.filename)
        if os.path.exists(dest):
            os.unlink(dest)

        src = os.path.join(args["<library>"], "Masters", photo.path)

        # At least on ext4 this was necessary when accessing data
        # copied from HFS+
        src = unicodedata.normalize("NFKC", src)

        try:
            link_method(src, dest)
        except FileNotFoundError as e:
            print(e)

        for idx, ver in enumerate(photo.versions):
            xmp_content = xmp.generate_xmp_rating(photo.filename, ver.rating)
            xmp_fullpath = os.path.join(path, xmp.xmp_filename(photo.filename, idx))
            with open(xmp_fullpath, "w") as xmp_file:
                xmp_file.write(xmp_content)

            metafile = xmp_fullpath + ".pprint.txt"
            with open(metafile, "w") as meta_file:
                meta_file.write(pprint.pformat(ver.content))

            print((d * 2 * " ") + f"  - {photo.filename} [{idx}] " + "*" * photo.rating)

    for f0 in f.folders:
        process_folder(f0, d + 1, os.path.join(path, f0.name))

dest = args["<dest>"]

ap = library.ApertureLibrary(args["<library>"])
process_folder(ap.all_projects(), 0, dest)

