#!/usr/bin/env python
# encoding: utf-8

import sqlite3

class Identities(object):

    sql_get = '''SELECT identity FROM identities WHERE alias=? LIMIT 1;'''
    sql_add = '''INSERT OR REPLACE INTO identities VALUES (?, ?);'''
    sql_del = '''DELETE FROM identities WHERE alias=?;'''

    def __init__(self, db_path, schema_sql):
        self.db_path = db_path
        self.schema_sql = schema_sql

        self.db = sqlite3.connect(self.db_path)

        # Create schema
        self.initdb()

    def initdb(self):
        self.db.cursor().executescript(self.schema_sql)
        self.db.commit()

    def add(self, alias, identity):
        self.db.cursor().execute(self.sql_add, (alias, identity))
        self.db.commit()

    def get(self, alias):
        res = self.db.cursor().execute(self.sql_get, (alias,))
        res = res.fetchone()
        if not res: return False
        else: return res[0]

    def remove(self, alias):
        self.db.cursor().execute(self.sql_del, (alias,))

    def __getitem__(self, alias):
        return self.get(alias)

    def __setitem__(self, alias, identity):
        return self.set(alias, identity)

    def __delitem__(self, alias):
        return self.remove(alias)

    def __contains__(self, alias):
        pass
