import sublime
import sublime_plugin

try:
    # Sublime 2
    from psql import PsqlCommander
    from patterns import is_table_request, is_columns_request, get_table_name
    st_version = 2
except (ImportError):
    # Sublime 3
    from .psql import PsqlCommander
    from .patterns import is_table_request, is_columns_request, get_table_name
    st_version = 3


format = lambda l: [(x.decode('utf-8'), '"{0}"'.format(x.decode('utf-8'))) for x in l]


class YuaSqlAutocomplete(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        self.psql = PsqlCommander(st_version=st_version)
        # self.patterns.register('columns', psql.get_columns)

    def on_query_completions(self, view, prefix, locations):
        cur = view.sel()[0].begin()
        
        row, col = view.rowcol(cur)
        line_substr = view.substr(view.line(cur))

        if is_table_request(line_substr, col):
            result = self.psql.get_tables()
        elif is_columns_request(line_substr, col):
            table_name = get_table_name(line_substr, col)
            result = self.psql.get_columns(table_name)
        else:
            result = []

        return format(result)
