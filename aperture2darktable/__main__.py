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
from . import library
from . import xmp

DOC = """
Usage: aperture2darktable <library> <dest>
"""

args = docopt(DOC)
print(args)

def process_folder(f, d, path):
    print((d * 2 * " ") + "- " + f.name)
    if not os.path.exists(path):
        os.makedirs(path)
        
    for photo in f.photos:
        dest = os.path.join(path, photo.filename)
        if os.path.exists(dest):
            os.unlink(dest)

        abs_dest = os.path.join(args["<library>"], "Masters", photo.path)
        start_path = os.path.dirname(dest)
        link_dest = os.path.relpath(abs_dest, start=start_path)
        os.symlink(link_dest,
                   dest)

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

