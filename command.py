import sublime
import sublime_plugin

from psql import PsqlCommander
from patterns import Patterns

format = lambda l: [(x, x) for x in l]

psql = PsqlCommander(settings=sublime.load_settings('YUA_SQL.sublime-settings'))

patterns = Patterns()
patterns.register('tables', psql.get_tables)
patterns.register('columns', psql.get_columns)


class YuaSqlAutocomplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        cur = view.sel()[0].begin()

        row, col = view.rowcol(cur)
        line_substr = view.substr(view.line(cur))

        result = patterns.match(line_substr[:col], line_substr[col:])
        # result = patterns.match(line_substr)
        return format(result) if result else None
