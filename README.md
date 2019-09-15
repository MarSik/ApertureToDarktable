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

## Licensing

Copyright 2019 Martin Sivak

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

