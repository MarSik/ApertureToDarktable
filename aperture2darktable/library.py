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

import sqlite3
import os
import pprint

from . import bplist

class ApertureDbBase(object):
    def __init__(self, basedir=None, db=None):
        if db:
            self.db = db
        elif basedir:
            self.db = sqlite3.connect(os.path.join(basedir, "Database", "Library.apdb"))

        self.basedir = basedir

class Version(ApertureDbBase):
    def __init__(self, uuid, basedir=None, db=None):
        super().__init__(basedir=basedir, db=db)
        self.uuid = uuid

    @property
    def filename(self):
        c = self.db.cursor()
        c.execute("SELECT masterUuid FROM RKVersion WHERE uuid='%s'" % self.uuid)
        ret = c.fetchone()
        photo = Photo(ret[0], basedir=self.basedir, db=self.db)
        path = os.path.join(os.path.dirname(photo.path), photo.uuid, f"Version-{self.version}.apversion")
        return os.path.join(self.basedir, "Database", "Versions", path)

    @property
    def name(self):
        c = self.db.cursor()
        c.execute("SELECT name FROM RKVersion WHERE uuid='%s'" % self.uuid)
        ret = c.fetchone()
        return ret[0]

    @property
    def content(self):
        try:
            with open(self.filename, "rb") as fl:
                data = bplist.BPListReader(fl.read()).parse()
                if b"RKImageAdjustments" in data:
                    for adj in data[b"RKImageAdjustments"]:
                        if b"data" in adj:
                            adj[b"data"] = bplist.BPListReader(adj[b"data"]).parse()
                return data

        except FileNotFoundError as ex:
            print(ex)
            return {}

    @property
    def rating(self):
        c = self.db.cursor()
        c.execute("SELECT mainRating FROM RKVersion WHERE uuid='%s'" % self.uuid)
        ret = c.fetchone()
        return ret[0] if ret else 0

    @property
    def version(self):
        c = self.db.cursor()
        c.execute("SELECT versionNumber FROM RKVersion WHERE uuid='%s'" % self.uuid)
        ret = c.fetchone()
        return ret[0] if ret else 0


class Photo(ApertureDbBase):
    def __init__(self, uuid, basedir=None, db=None):
        super().__init__(basedir=basedir, db=db)
        self.uuid = uuid

    @property
    def name(self):
        c = self.db.cursor()
        c.execute("SELECT name FROM RKMaster WHERE uuid='%s'" % self.uuid)
        ret = c.fetchone()
        return ret[0]

    @property
    def filename(self):
        c = self.db.cursor()
        c.execute("SELECT fileName FROM RKMaster WHERE uuid='%s'" % self.uuid)
        ret = c.fetchone()
        return ret[0]

    @property
    def path(self):
        c = self.db.cursor()
        c.execute("SELECT imagePath FROM RKMaster WHERE uuid='%s'" % self.uuid)
        ret = c.fetchone()
        return ret[0]
    
    @property
    def rating(self):
        c = self.db.cursor()
        c.execute("SELECT max(mainRating) FROM RKVersion WHERE masterUuid='%s' GROUP BY masterUuid" % self.uuid)
        ret = c.fetchone()
        return ret[0] if ret else 0

    @property
    def versions(self):
        c = self.db.cursor()
        ret = c.execute("SELECT uuid FROM RKVersion WHERE masterUuid='%s' AND isHidden=0 AND isInTrash=0 AND showInLibrary=1" % self.uuid)
        return [Version(row[0], db=self.db, basedir=self.basedir) for row in ret]


class Folder(ApertureDbBase):
    def __init__(self, uuid, basedir=None, db=None):
        super().__init__(basedir=basedir, db=db)
        self.uuid = uuid

    @classmethod
    def all_projects(cls, basedir=None, db=None):
        return cls("AllProjectsItem", db=db, basedir=basedir)

    @property
    def name(self):
        c = self.db.cursor()
        c.execute("SELECT name FROM RKFolder WHERE uuid='%s'" % self.uuid)
        ret = c.fetchone()
        return ret[0]

    @property
    def photos(self):
        c = self.db.cursor()
        ret = c.execute("SELECT uuid FROM RKMaster WHERE projectUuid='%s' AND isInTrash=0" % self.uuid)
        return [Photo(row[0], db=self.db, basedir=self.basedir) for row in ret]

    @property
    def folders(self):
        c = self.db.cursor()
        ret = c.execute("SELECT uuid FROM RKFolder WHERE parentFolderUuid='%s'" % self.uuid)
        return [Folder(row[0], db=self.db, basedir=self.basedir) for row in ret]
        

class ApertureLibrary(ApertureDbBase):
    def __init__(self, basedir, db=None):
        super().__init__(basedir=basedir, db=db)

    def all_projects(self):
        return Folder.all_projects(db=self.db, basedir=self.basedir)

