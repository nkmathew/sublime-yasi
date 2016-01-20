""" sublime-yasi

Date: 19th January 2016
Author: nkmathew <kipkoechmathew@gmail.com>
"""

import sublime
import sublime_plugin
import re

try:
    import yasi
except ImportError:
    from . import yasi

__version__ = '0.1.2'

class IndentSexpCommand(sublime_plugin.TextCommand):
    """ Handles indent_sexp command """
    def __init__(self, view):
        """ init """
        self.view = view

    def get_line(self, lnum):
        """ Returns contents of a certain line """
        region = self.line_region(lnum)
        text = self.view.substr(region)
        return text

    def line_region(self, lnum):
        """ Returns region bounds for supplied line number """
        point = self.view.text_point(lnum, 0)
        region = self.view.full_line(sublime.Region(point, point))
        return region

    def caret_pos(self):
        """ Cursor position in row-column tuple """
        return self.view.rowcol(self.view.sel()[0].begin())

    def curr_line(self):
        """ Returns the line number of the current line """
        return self.caret_pos()[0]

    def get_syntax(self):
        """ Retuns current file syntax/language """
        syntax = self.view.settings().get('syntax')
        syntax = syntax.split('/')[-1].replace('.tmLanguage', '')
        return syntax

    def dialect(self):
        """ Translate language name setting to a recognized dialect by yasi """
        syntax = self.get_syntax()
        dialect = 'all'
        if re.match('newlisp', syntax, re.I):
            dialect = 'newlisp'
        elif re.match('clojure', syntax, re.I):
            dialect = 'clojure'
        elif re.match('scheme', syntax, re.I):
            dialect = 'scheme'
        elif re.match('lisp', syntax, re.I):
            dialect = 'lisp'
        return dialect

    def is_enabled(self):
        """
        Disables command when not editing a lisp or lisp-like language
        """
        syntax = self.get_syntax()
        match = re.match('newlisp|clojure|lisp|scheme', syntax, re.I)
        return bool(match)

    def run(self, edit):
        """ Entry point """
        regions = self.view.sel()
        if len(regions) > 1 or not regions[0].empty():
            # Indent selected code
            for region in regions:
                if not region.empty():
                    # Get the selected text
                    selection = self.view.substr(region)
                    # Indent it with yasi
                    dialect = self.dialect()
                    yasi_args = '--no-compact --dialect={0}'.format(dialect)
                    result = yasi.indent_code(selection, yasi_args)
                    indented_code = ''.join(result[-1])
                    # Replace the selection with transformed text
                    self.view.replace(edit, region, indented_code)
        else:
            # Indent current line if command is invoked when there's no selection
            last_50_lines = ''
            line_number = self.caret_pos()[0]
            count = 0
            while line_number >= 0 and count <= 50:
                last_50_lines = self.get_line(line_number) + last_50_lines
                line_number -= 1
                count += 1
            dialect = self.dialect()
            yasi_args = '--no-compact --dialect={0}'.format(dialect)
            result = yasi.indent_code(last_50_lines, yasi_args)
            if result:
                curr_line_region = self.line_region(self.curr_line())
                curr_indented_line = result[-1][-1]
                self.view.replace(edit, curr_line_region, curr_indented_line)
