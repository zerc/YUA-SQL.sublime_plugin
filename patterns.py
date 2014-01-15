# coding: utf-8
import os
import re


class Patterns(object):
    """
    Object for call specified functions for patterns
    """
    def __init__(self, *args, **kwargs):
        self._re = dict(
            tables=dict(
                func=None,
                patterns=[
                    ('left', re.compile("(INTO|FROM|UPDATE) \"\w+$"))
                ]
            ),

            columns=dict(
                func=None,
                patterns=[
                    ('both', re.compile('INTO "(\w+)" \(')),
                    ('both', re.compile('FROM "(\w+)"')),
                    ('both', re.compile('UPDATE "(\w+)"')),
                ]
            )
        )

    def register(self, pattern_name, func):
        if pattern_name not in self._re.keys():
            return
        self._re[pattern_name]['func'] = func

    def match(self, l_string, r_string):
        for _re in self._re.values():
            for row in _re['patterns']:
                use, p = row

                if use == 'left':
                    s = l_string
                elif use == 'right':
                    s = r_string
                else:
                    s = l_string + r_string

                result = p.findall(s)

                if result and result[0]:
                    return _re['func'](result[0])
