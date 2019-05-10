
# =========================================
#       IMPORTS
# --------------------------------------

import re
import sys
import traceback
import inspect
import inspecta
import json

from termcolor import colored as color

from os import environ as env
from os import path

from attributedict.collections import AttributeDict


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

class BaseError(Exception):

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

        details = details or {}

        if not isinstance(details, dict):
            raise TypeError('Expected argument {klass}(details = <details>) to be a `{expected_type}`, but was `{actual_type}`.'.format(
                klass = self.__class__.__name__,
                expected_type = type({}),
                actual_type = type(details),
            ))

        stackframes = inspect.stack()[1:]
        stacktrace = ''.join(traceback.format_exception(*sys.exc_info()))

        self._error = error
        self._id = id
        self._key = key
        self._code = code
        self._message = message
        self._details = details
        self._stackframes = stackframes
        self._stacktrace = stacktrace

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def details(self):
        return self._details or {}

    @property
    def stack(self):
        return self.stacktrace

    @property
    def stacktrace(self):
        return self._stacktrace

    @property
    def stackframes(self):
        return self._stackframes

    @property
    def stackobjects(self):
        stackobjects = []

        for stackframe in self.stackframes:
            (
                frame,
                filename,
                line_number,
                function_name,
                lines,
                index
            ) = stackframe

            file = path.abspath(filename)
            function = function_name
            line = line_number
            column = None
            source = '\n'.join(list(lines))

            stackobject = dict(
                file = file,
                function = function,
                line = line,
                column = column,
                source = source,
            )

            is_internal_stack_file = (__file__.replace('.pyc', '.py') in stackobject['file'])
            is_internal_stack_function = (stackobject['function'] in dir(self))
            is_internal_stack_object = is_internal_stack_file and is_internal_stack_function

            if not is_internal_stack_object:
                stackobjects.append(stackobject)

        return stackobjects

    @property
    def data(self):
        return AttributeDict({
            'type': self.__class__.__name__,
            'id': self.id,
            'code': self.code,
            'key': self.key,
            'message': self.message,
            'details': self.details,
            'stack': self.stackobjects,
        })

    def json(self,
        indent = None,
    ):
        if indent is None:
            indent = DEFAULT_ERROR_INDENT

        return json.dumps(AttributeDict.dict(self.data),
            default = repr,
            indent = indent,
        )

    def inspect(self,
        colors = None,
        verbose = None,
    ):
        if colors is None:
            colors = DEFAULT_ERROR_COLORS

        if verbose is None:
            verbose = DEFAULT_ERROR_VERBOSE

        return inspecta.inspect(self.data,
            colors = colors,
        )

    def format(self,
        colors = None,
        verbose = None,
    ):
        if colors is None:
            colors = DEFAULT_ERROR_COLORS

        if verbose is None:
            verbose = DEFAULT_ERROR_VERBOSE

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

        has_details = isinstance(self.details, dict) and len(self.details.keys())

        _message = ' - '.join(list(filter(bool, [
            _message,
            (has_details and _details),
        ])))

        return _message

    def __repr__(self):
        return '{}'.format(self.__str__())

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

        string = self.format(
            colors = colors,
            verbose = verbose
        )

        string = string.strip()

        return string

    def __nonzero__(self):
        return self.__bool__()

    def __bool__(self):
        return True

    @staticmethod
    def cast(error):
        if isinstance(error, Error):
            return error

        else:
            return Error(error)

    @staticmethod
    def object(error, **attrs):
        extended_error = BaseError.cast(error)

        return AttributeDict({
            'type': error.__class__.__name__,
            'id': extended_error.id,
            'code': extended_error.code,
            'key': extended_error.key,
            'message': extended_error.message,
            'details': extended_error.details,
            'stack': extended_error.stackobjects,
        }, **attrs)


# =========================================
#       ERRORS
# --------------------------------------

Error = BaseError

__all__ = [
    'Error',
]
