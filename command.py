import sublime, sublime_plugin
import os
import re

sql = """echo "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';" | psql -U aiw_user -d alli"""
f = os.popen(sql)
raw = f.read()
a = raw.strip().split('\n ')[2:-1]


def get_columns(table):
    cmd = """ echo "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '%s';" | psql -U aiw_user -d alli """ % table
    f = os.popen(cmd)
    raw = f.read()
    return raw.strip().split('\n ')[2:-1]


class YuaSqlAutocomplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        row, col = view.rowcol(view.sel()[0].begin())
        line_substr = view.substr(view.line(view.sel()[0].begin()))

        if re.findall("INSERT INTO \"\w*$", line_substr[:col]):
            return [(x, x) for x in a]

        table_name = re.findall("INSERT INTO \"(\w*)\" \([\w\s,\"]*$", line_substr[:col])

        if table_name and table_name[0]:
            result = get_columns(table_name[0])
            return [(x, x) for x in result]
