""" sublime-yasi

Date: 19th January 2016
Author: nkmathew <kipkoechmathew@gmail.com>
"""

import sublime         # pylint: disable=import-error
import sublime_plugin  # pylint: disable=import-error
import re

# pylint: disable=unused-import
from pprint import pprint

try:
    import yasi
except ImportError:
    from . import yasi

__version__ = '0.1.2'


def log(msg):
    """ Logging """
    print('yasi: %s' % msg)


class IndentSexpCommand(sublime_plugin.TextCommand):
    """ Handles indent_sexp command """
    def __init__(self, view):
        """ init """
        self.view = view

    def get_line(self, lnum=None):
        """ Returns contents of a certain line. Supports negative indexing """
        lnum = lnum or self.curr_line()
        if lnum < 0:
            lnum = self.curr_line() + lnum
        lnum = lnum if lnum >= 0 else 0
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

    def caret_offset(self):
        """
        Cursor position in terms of the number of characters from the start of
        the file
        """
        return self.view.sel()[0].begin()

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

    def prev_lines(self, nlines, line_number=None):
        """
        Returns a list of the previous specified number of lines with their
        line ends from the specified line number including the current line.
        Starts counting from the current line if the second argument is not provided
        """
        line_number = line_number or self.curr_line()
        x_lines = []
        count = 0
        while line_number >= 0 and count <= nlines:
            x_lines.insert(0, self.get_line(line_number))
            line_number -= 1
            count += 1
        return x_lines

    def indent_line(self, linenum, context_lines):
        """
        Returns info on the current indented line
        """
        prev_x_lines = ''.join(self.prev_lines(context_lines, linenum))
        dialect = self.dialect()
        yasi_args = '--no-compact --dialect={0}'.format(dialect)
        result = yasi.indent_code(prev_x_lines, yasi_args)
        return result

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
                    yasi_args = '--no-compact -ic --dialect={0}'.format(dialect)
                    result = yasi.indent_code(selection, yasi_args)
                    indented_code = ''.join(result[-1])
                    # Replace the selection with transformed text
                    self.view.replace(edit, region, indented_code)
        else:
            # Indent current line if command is invoked when there's no selection
            indented_line = self.indent_line(self.curr_line(), 50)[-1]
            if indented_line:
                indented_line = indented_line[-1]
            else:
                indented_line = ''
            curr_line_region = self.line_region(self.curr_line())
            self.view.replace(edit, curr_line_region, indented_line)


class IndentSexpNewlineCommand(IndentSexpCommand):
    """ Handles indent_sexp_newline command """
    def run(self, edit):
        """ Called when the enter key is pressed in a lisp file """
        offset = self.caret_offset()
        start_pos = offset - 2000
        start_pos = start_pos if start_pos >= 0 else 0
        pair = [start_pos, offset]
        code = ''
        seen_string = True
        rx_str_comment = re.compile('comment\.|string\.')
        curr_line = self.get_line()
        curr_indent = re.search('^\s*', curr_line).end()
        while start_pos != offset:
            # Build a string with the previous 2000 or so characters with any
            # strings and comments ignored(replaced with some dummy primitive)
            scope_name = self.view.scope_name(start_pos)
            curr_char = self.view.substr(start_pos)
            start_pos += 1
            if rx_str_comment.search(scope_name):
                if not seen_string:
                    code += '999'
                seen_string = True
            else:
                code += curr_char
                seen_string = False
        dialect = self.dialect()
        yasi_args = '--no-compact --dialect={0}'.format(dialect)
        result = yasi.indent_code(code, yasi_args)
        open_brackets = result[-4]
        if open_brackets:
            indent_level = open_brackets[-1]['indent_level']
            self.view.insert(edit, offset, '\n' + ' ' * indent_level)
        elif rx_str_comment.search(self.view.scope_name(offset)):
            self.view.insert(edit, offset, '\n' + '  ' * curr_indent)
        else:
            self.view.insert(edit, offset, '\n')
