# coding: utf-8
import os
import subprocess


class PsqlCommander(object):
    """
    Wrapper around `psql` console programm
    """
    def __init__(self, settings, *args, **kwargs):
        self.settings = settings
        self.cmd_tmpl = \
            'psql -U {user} -d {db_name} -h {host} -c "{{cmd}}"'.format(
            **self.settings.get('psql'))

    def _call(self, cmd):
        params = dict(stderr=subprocess.STDOUT, stdin=subprocess.PIPE,
                      stdout=subprocess.PIPE, shell=True)
        popen = subprocess.Popen(cmd, **params)
        data = popen.communicate()[0]
        return data.strip().split('\n ')[2:-1]

    def get_tables(self, *args, **kwargs):
        sql = """
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'"""
        return self._call(self.cmd_tmpl.format(cmd=sql))

    def get_columns(self, table, *args, **kwargs):
        sql = """
        SELECT column_name FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = '{table}'
        """.format(table=table)
        return self._call(self.cmd_tmpl.format(cmd=sql))
