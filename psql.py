# coding: utf-8
import os
import subprocess

import sublime


class PsqlCommander(object):
    """
    Wrapper around `psql` console programm
    """
    def __init__(self, st_version, *args, **kwargs):
        self.st_version = st_version
        self.cmd_tmpl = 'psql -U {user} -d {db_name} -h {host} -c "{cmd}"'

    def _load_settings(self):
        self.settings = sublime.load_settings('YUA_SQL.sublime-settings').get('psql')

    def _clean(self, data):
        return [x.strip() for x in data.strip().split(b'\n')[2:-1]]

    def _call(self, cmd):
        self._load_settings()
        if not self.settings:
            return []

        params = dict(stderr=subprocess.STDOUT, stdin=subprocess.PIPE,
                      stdout=subprocess.PIPE, shell=True)

        popen = subprocess.Popen(
            self.cmd_tmpl.format(cmd=cmd, **self.settings), **params)
        data = popen.communicate()[0]
        
        return self._clean(data)


    def get_tables(self, *args, **kwargs):
        sql = """
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'"""
        return self._call(cmd=sql)

    def get_columns(self, table, *args, **kwargs):
        sql = """
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = '{table}'
        """.format(table=table)
        return self._call(cmd=sql)
