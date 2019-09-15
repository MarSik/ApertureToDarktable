# Aperture to Darktable

Apple Aperture 3 is a no longer maintained product. I wanted to move to a fully opensource solution and still retain access to my Aperture libraries.

This tool takes an Aperture library and creates Darktable compatible parallel directory structure using symlinks and metadata files. The original Aperture library is not modified in any way!

## Requirements

- Python 3

## How to use this tool

1. First clone the git repository
2. Install pipenv
   ```pip3 install --user pipenv```
3. Install all dependencies
   ```pipenv install```
4. Execute the script
   ```pipenv run python3 -m aperture2darktable <library> <destination>```

This will read the Aperture library <library> and create the directory with symlinks at `<destination>`.

