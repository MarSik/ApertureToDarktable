from docopt import docopt
import os.path
from . import library

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
        os.symlink(os.path.join(args["<library>"], "Masters", photo.path),
                   dest)
        print((d * 2 * " ") + "  - " + photo.filename + " -> " + dest)
    for f0 in f.folders:
        process_folder(f0, d + 1, os.path.join(path, f0.name))

dest = args["<dest>"]

ap = library.ApertureLibrary(args["<library>"])
process_folder(ap.all_projects(), 0, dest)

