import sqlite3
import os

class ApertureDbBase(object):
    def __init__(self, basedir=None, db=None):
        if db:
            self.db = db
        elif basedir:
            self.db = sqlite3.connect(os.path.join(basedir, "Database", "Library.apdb"))
        else:
            pass # nothing


class Photo(ApertureDbBase):
    def __init__(self, uuid, db=None):
        super().__init__(db=db)
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
    def score(self):
        c = self.db.cursor()
        c.execute("SELECT max(mainRating) FROM RKVersion WHERE masterUuid='%s' GROUP BY masterUuid" % self.uuid)
        ret = c.fetchone()
        return ret[0]


class Folder(ApertureDbBase):
    def __init__(self, uuid, db=None):
        super().__init__(db=db)
        self.uuid = uuid

    @classmethod
    def all_projects(cls, db=None):
        return cls("AllProjectsItem", db=db)

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
        return [Photo(row[0], db=self.db) for row in ret]

    @property
    def folders(self):
        c = self.db.cursor()
        ret = c.execute("SELECT uuid FROM RKFolder WHERE parentFolderUuid='%s'" % self.uuid)
        return [Folder(row[0], db=self.db) for row in ret]
        

class ApertureLibrary(ApertureDbBase):
    def __init__(self, basedir, db=None):
        super().__init__(basedir=basedir, db=db)

    def all_projects(self):
        return Folder.all_projects(db=self.db)

