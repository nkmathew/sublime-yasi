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

__version__ = '0.4.2'


def log(msg):
    """ Logs messages to Sublime console """
    print('yasi: %s' % msg)


def get_syntax(view):
    """ get_syntax(view : sublime.View) -> str

    >>> get_syntax(view)
    'newLISP'

    >>> get_syntax(view)
    'Lisp'

    Retuns current file syntax/language
    """
    syntax = view.settings().get('syntax')
    syntax = syntax.split('/')[-1].replace('.tmLanguage', '')
    return syntax


def get_dialect(view):
    """ get_dialect(view : sublime.View) -> str

    >>> get_dialect(view)
    'clojure'

    Translate current language setting to a dialect recognized by yasi """
    syntax = get_syntax(view)
    dialect = ''
    if re.match('newlisp', syntax, re.I):
        dialect = 'newlisp'
    elif re.match('clojure', syntax, re.I):
        dialect = 'clojure'
    elif re.match('scheme', syntax, re.I):
        dialect = 'scheme'
    elif re.match('lisp', syntax, re.I):
        dialect = 'lisp'
    return dialect


def is_lisp_like(view):
    """ Check for a lisp like file using the current language/syntax setting """
    return get_dialect(view) != ''


class SexpIndentCommand(sublime_plugin.TextCommand):
    """ Handles indent_sexp command """

    def __init__(self, view):
        """ init """
        self.view = view

    def indent_file_on_save(self):
        """ Reads user setting on whether the file should be indented on save """
        gsettings = sublime.load_settings('yasi-indenter.sublime-settings')
        gindent = gsettings.get('indent_sexp_on_save', True)
        indent = self.view.settings().get('indent_sexp_on_save', gindent)
        return indent and isinstance(indent, bool)

    def get_line(self, lnum=None):
        """ get_line(lnum : int) -> str

        >>> get_line(-1)
        >>> get_line()

        Returns contents of a certain line. Supports negative indexing
        """
        if lnum is None:
            lnum = self.curr_line()
        if lnum < 0:
            lnum = self.curr_line() + lnum
        lnum = lnum if lnum >= 0 else 0
        region = self.line_region(lnum)
        text = self.view.substr(region)
        return text

    def line_region(self, lnum=None):
        """ line_region(lnum : int) -> sublime.Region

        >>> line_region(0) ## Doesn't support indexing btw
        (0, 9)
        >>> line_region(0).begin()
        0
        >>> line_region(0).end()
        9

        Returns region bounds for supplied line number """
        if lnum is None:
            lnum = self.curr_line()
        if lnum < 0:
            lnum = self.curr_line() + lnum
        lnum = lnum if lnum >= 0 else 0
        point = self.view.text_point(lnum, 0)
        region = self.view.full_line(sublime.Region(point, point))
        return region

    def caret_pos(self):
        """ caret_pos() -> tuple

        >>> caret_pos()
        (11, 2)

        Current cursor position in row-column tuple """
        return self.view.rowcol(self.view.sel()[0].begin())

    def caret_offset(self):
        """ caret_offset() -> int

        >>> caret_offset()
        1345

        Current cursor position in terms of the number of characters from the start of
        the file
        """
        return self.view.sel()[0].begin()

    def file_contents(self):
        """ file_contents() -> str

        Returns contents of the whole file
        """
        return self.view.substr(sublime.Region(0, self.view.size()))

    def curr_line(self):
        """ curr_line() -> int

        >>> curr_line()
        25

        Returns the line number of the current line """
        return self.caret_pos()[0]

    def is_enabled(self):
        """ is_enabled() -> bool

        Returns True or False on whether the current file is a lisp or lisp-like
        language handled by yasi

        The method is called by the editor to determine whether to disable the
        'Indent S-expression' menu command
        """
        syntax = get_syntax(self.view)
        match = re.match('newlisp|clojure|lisp|scheme', syntax, re.I)
        return bool(match)

    def prev_lines(self, nlines, line_number=None):
        """ prev_lines(nlines : int) -> [str]

        Arguments:
        nlines: Number of lines to get
        line_number: The starting line number. Defaults to the current line

        >>> prev_lines(5)
        ['(defn get-neighbors [[x y] v]\n',
        '  (for [y1\n',
        '       ss\n',
        '       \n',
        '       (range (dec y) (+ y 2))\n',
        '       x1 (range (dec x) (+ x 2))\n']

        Returns a list of the previous specified number of lines including the
        contents of the specified line number
        """
        line_number = line_number or self.curr_line()
        x_lines = []
        count = 0
        # log('nlines: %d' % nlines)
        while line_number >= 0 and count <= nlines:
            line = self.get_line(line_number)
            x_lines.insert(0, line)
            line_number -= 1
            count += 1
        return x_lines

    def indent_line(self, linenum, context_lines):
        """ indent_line(linenum : int, context_lines : int) -> [...]

        Indents the last x number of lines and returns information on the current
        state e.g open brackets, the indented code, string/comment states
        """
        prev_x_lines = ''.join(self.prev_lines(context_lines, linenum))
        dialect = get_dialect(self.view)
        yasi_args = '--no-compact --dialect={0}'.format(dialect)
        result = yasi.indent_code(prev_x_lines, yasi_args)
        return result


class IndentSexpCommand(SexpIndentCommand):
    """ Command to indent sexp selections and single lines """

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
                    dialect = get_dialect(self.view)
                    yasi_args = '--no-compact -ic --dialect={0}'.format(dialect)
                    result = yasi.indent_code(selection, yasi_args)
                    indented_code = ''.join(result['indented_code'])
                    # Replace the selection with transformed text
                    self.view.replace(edit, region, indented_code)
        else:
            # Indent current line if command is invoked when there's no selection
            indented_lines = self.indent_line(self.curr_line(), 50)['indented_code']
            indented_line = ''
            if indented_lines:
                indented_line = indented_lines[-1]
            curr_line_region = self.line_region(self.curr_line())
            self.view.replace(edit, curr_line_region, indented_line)


class IndentSexpAutoCommand(SexpIndentCommand):
    """ Handles indent_sexp_auto command """
    def run(self, edit):
        """ Called when the enter key is pressed in a lisp file """
        offset = self.caret_offset()
        start_pos = offset - 2000
        start_pos = start_pos if start_pos >= 0 else 0
        code = ''
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
                code += '0'
            else:
                code += curr_char
        dialect = get_dialect(self.view)
        yasi_args = '--no-compact --dialect={0}'.format(dialect)
        result = yasi.indent_code(code, yasi_args)
        open_brackets = result['bracket_locations']
        indent_level = 0
        if open_brackets:
            indent_level = open_brackets[-1]['indent_level']
        elif rx_str_comment.search(self.view.scope_name(offset)):
            indent_level = curr_indent
        else:
            indent_level = 0
        self.view.insert(edit, offset, '\n' + ' ' * indent_level)


class IndentSexpFileCommand(SexpIndentCommand):
    """ Indents the whole file """

    def run(self, edit):
        """ Entry point """
        if not self.indent_file_on_save():
            return
        contents = self.file_contents()
        dialect = get_dialect(self.view)
        yasi_args = '--no-compact -ic --dialect={0}'.format(dialect)
        result = yasi.indent_code(contents, yasi_args)
        indented_code = ''.join(result['indented_code'])
        file_region = sublime.Region(0, self.view.size())
        self.view.replace(edit, file_region, indented_code)


class OnSaveListener(sublime_plugin.EventListener):
    """ Before save event listener """

    def __init__(self):
        self.command_name = 'indent_sexp_file'

    def on_pre_save(self, view):
        """ Handler method """
        view.window().run_command(self.command_name)


class EnterKeyListener(sublime_plugin.EventListener):
    """ Enter key context listener """

    def __init__(self):
        self.context_name = 'in_lisp_like_file'

    # pylint: disable=unused-argument
    def on_query_context(self, view, key, operator, operand, match_all):
        """ Releases enter key when not editing a lisp-like file """
        if key == self.context_name:
            enable = is_lisp_like(view)
            return enable
