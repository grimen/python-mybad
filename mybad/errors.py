
# =========================================
#       IMPORTS
# --------------------------------------

import re
import traceback
import inspect
import inspecta

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
        colors = env.get('ERROR_COLORS', None)
        colors = colors or env.get('COLORS', None)

        if colors is None:
            colors = DEFAULT_ERROR_COLORS

        colors = re.search(r'^true|1$', str(colors), flags = re.IGNORECASE)

        verbose = env.get('ERROR_VERBOSE', None)
        verbose = verbose or env.get('VERBOSE', None)

        if verbose is None:
            verbose = DEFAULT_ERROR_VERBOSE

        verbose = re.search(r'^true|1$', str(verbose), flags = re.IGNORECASE)

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
            _details = inspecta.inspect(self.details,
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

