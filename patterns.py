# coding: utf-8
import os
import re

tables_re = re.compile("(INTO|FROM|UPDATE) \"\w+$")
columns_re = re.compile("(INTO|FROM|UPDATE) \"(\w+)\" ")

def is_table_request(s, col):
    """
    Test what `s` is are string for fetching tables
    """
    return not not tables_re.findall(s[:col])


def is_columns_request(s, col):
    """
    Test what `s` is are string for fetching columns
    """
    return not not columns_re.findall(s)


def get_table_name(s, col):
    """
    Extract table_name from s
    """
    result = columns_re.findall(s)
    return result[0][1]
