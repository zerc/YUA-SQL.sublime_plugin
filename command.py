import sublime
import sublime_plugin

try:
    # Sublime 2
    from psql import PsqlCommander
    from patterns import Patterns
    st_version = 2
except (ImportError):
    # Sublime 3
    from .psql import PsqlCommander
    from .patterns import Patterns
    st_version = 3


format = lambda l: [(x.decode('utf-8'), x.decode('utf-8')) for x in l]


class YuaSqlAutocomplete(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        psql = PsqlCommander(st_version=st_version)
        self.patterns = Patterns()
        self.patterns.register('tables', psql.get_tables)
        # self.patterns.register('columns', psql.get_columns)

    def on_query_completions(self, view, prefix, locations):
        cur = view.sel()[0].begin()
        
        row, col = view.rowcol(cur)
        line_substr = view.substr(view.line(cur))

        result = self.patterns.match(line_substr[:col], line_substr[col:])
        # result = patterns.match(line_substr)
        return format(result) if result else None
