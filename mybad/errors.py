
# =========================================
#       IMPORTS
# --------------------------------------

import re
import traceback
import inspect
import pprint

from pygments import highlight, lexers, formatters
from termcolor import colored as color

from os import environ as env


# =========================================
#       CONSTANTS
# --------------------------------------

DEFAULT_ERROR_INDENT = 4
DEFAULT_ERROR_DEPTH = None
DEFAULT_ERROR_COLORS = True
DEFAULT_ERROR_VERBOSE = True


# =========================================
#       HELPERS
# --------------------------------------

def _inspect(
    data = None,
    indent = None,
    depth = None,
    colors = False,
):
    if indent is None:
        indent = DEFAULT_ERROR_INDENT

    if depth is None:
        depth = DEFAULT_ERROR_DEPTH

    if depth == False:
        depth = None

    if colors is None:
        colors = DEFAULT_ERROR_COLORS

    result = None

    try:
        if isinstance(data, dict):
            data = dict(data)

        result = pprint.pformat(data,
            indent = indent,
            depth = depth,
        )

        if colors:
            lexer = lexers.PythonLexer()
            formatter = formatters.TerminalFormatter()

            result = highlight(result, lexer, formatter)

    except Exception as error:
        pass

    return result


# =========================================
#       ERRORS
# --------------------------------------

class Error(Exception):

    def __init__(self,
        error = None,
        id = None,
        key = None,
        code = None,
        message = None,
        details = None,
    ):
        message = message or (error and str(error)) or 'Unknown'
        message = message and str(message)

        stack = inspect.stack()
        # REVIEW: instead serialize `inspect.stack()` into custom pretty string?
        stacktrace = '\n' + traceback.format_exc()
        details = details or {}

        if not isinstance(details, dict):
            raise TypeError('Expected argument {klass}(details = <details>) to be a `{expected_type}`, but was `{actual_type}`.'.format(
                klass = self.__class__.__name__,
                expected_type = type({}),
                actual_type = type(details),
            ))

        self.error = error
        self.id = id
        self.key = key
        self.code = code
        self.message = message
        self.details = details
        self.stack = stack
        self.stacktrace = stacktrace

    def __repr__(self):
        _name = self.__class__.__name__

        return '{} {}'.format(_name, self.__str__())

    def __str__(self):
        ERROR_COLORS = env.get('ERROR_COLORS', None)
        ERROR_COLORS = ERROR_COLORS or env.get('COLORS', None)

        if ERROR_COLORS is None:
            ERROR_COLORS = DEFAULT_ERROR_COLORS

        ERROR_COLORS = re.search(r'^true|1$', str(ERROR_COLORS), flags = re.IGNORECASE)

        ERROR_VERBOSE = env.get('ERROR_VERBOSE', None)
        ERROR_VERBOSE = ERROR_VERBOSE or env.get('VERBOSE', None)

        if ERROR_VERBOSE is None:
            ERROR_VERBOSE = DEFAULT_ERROR_VERBOSE

        ERROR_VERBOSE = re.search(r'^true|1$', str(ERROR_VERBOSE), flags = re.IGNORECASE)

        colors = ERROR_COLORS
        verbose = ERROR_VERBOSE

        string = self.inspect(
            colors = colors,
            verbose = verbose
        )

        return string

    def __nonzero__():
        return self.__bool__()

    def __bool__(self):
        return True

    def inspect(self,
        colors = None,
        verbose = None,
    ):
        if self.message is None:
            _message = '<none>'
        else:
            _message = self.message.split(' - Arguments')[0]

        if colors:
            _message = color(_message, 'red')

        if verbose:
            _details = _inspect(self.details,
                colors = colors,
            )
        else:
            _details = None

        _message = ' - '.join(list(filter(bool, [
            _message,
            _details
        ])))

        return _message

    @staticmethod
    def cast(error):
        if isinstance(error, Error):
            return error

        else:
            return Error(error)

    @staticmethod
    def object(error, attrs):
        if not isinstance(error, Error):
            error = Error(error)

        extended_error = Error.cast(error)

        return dict({
            'type': error.__class__.__name__,
            'id': extended_error.id,
            'code': extended_error.code,
            'key': extended_error.key,
            'message': extended_error.message,
            'details': extended_error.details,
            'stack': extended_error.stack,
        }, **attrs)

