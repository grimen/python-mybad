
# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()

import re
import json
import warnings

import attributedict

from attributedict.collections import AttributeDict

from os import environ as env
from os import path

from mybad.tests import helper

import mybad

env['COLORS'] = 'true' # lower prio
env['VERBOSE'] = 'true' # lower prio

env['ERROR_COLORS'] = 'false' # higher prio
env['ERROR_VERBOSE'] = 'false' # higher prio


# =========================================
#       CONSTANTS
# --------------------------------------

ROOT_PATH = path.abspath(path.join(path.dirname(__file__), '..'))


# =========================================
#       CONFIG
# --------------------------------------

warnings.simplefilter(action = 'ignore', category = FutureWarning)


# =========================================
#       HELPERS
# --------------------------------------

def strip_ansi(value):
    return re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', value)


# =========================================
#       TEST
# --------------------------------------

class TestCase(helper.TestCase):

    def test__import(self):
        self.assertModule(mybad)

    def test__instance(self):
        self.assertIsInstance(mybad.Error(), mybad.Error)

    def test_error(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'error'))

        some_raised_error = TypeError('No good')

        error = mybad.Error(some_raised_error)

        self.assertIsInstance(error.error, TypeError)
        self.assertEqual(str(error.error), 'No good')

    def test_id(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'id'))

        error = mybad.Error()

        self.assertIsInstance(error.id, type(None))
        self.assertEqual(error.id, None)

        error = mybad.Error(id = 123)

        self.assertIsInstance(error.id, int)
        self.assertEqual(error.id, 123)

        error = mybad.Error(id = '123')

        self.assertIsInstance(error.id, str)
        self.assertEqual(error.id, '123')

    def test_key(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'key'))

        self.assertIsInstance(error.key, type(None))
        self.assertEqual(error.key, None)

        error = mybad.Error(key = 123)

        self.assertIsInstance(error.key, int)
        self.assertEqual(error.key, 123)

        error = mybad.Error(key = '123')

        self.assertIsInstance(error.key, str)
        self.assertEqual(error.key, '123')

    def test_code(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'code'))

        self.assertIsInstance(error.code, type(None))
        self.assertEqual(error.code, None)

        error = mybad.Error(code = 123)

        self.assertIsInstance(error.code, int)
        self.assertEqual(error.code, 123)

        error = mybad.Error(code = '123')

        self.assertIsInstance(error.code, str)
        self.assertEqual(error.code, '123')

    def test_message(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'message'))

        self.assertIsInstance(error.message, str)
        self.assertEqual(error.message, 'Unknown')

        error = mybad.Error(message = 123)

        self.assertIsInstance(error.message, str)
        self.assertEqual(error.message, '123')

        error = mybad.Error(message = '123')

        self.assertIsInstance(error.message, str)
        self.assertEqual(error.message, '123')

    def test_details(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'details'))

        error = mybad.Error()

        self.assertIsInstance(error.details, dict)
        self.assertEqual(error.details, {})

        with self.assertRaises(TypeError):
            error = mybad.Error(details = 123)

        with self.assertRaises(TypeError):
            error = mybad.Error(details = '123')

        error = mybad.Error(details = {})

        self.assertIsInstance(error.details, dict)
        self.assertEqual(error.details, {})

        error = mybad.Error(details = {
            'foo': 'bar',
            'baz': [1, 2, 3],
        })

        self.assertIsInstance(error.details, dict)
        self.assertEqual(error.details, {
            'foo': 'bar',
            'baz': [1, 2, 3],
        })

    def test_stack(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'stack'))

        self.assertIsInstance(error.stack, str)
        self.assertGreater(len(error.stack), 0)

    def test_stacktrace(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'stacktrace'))

        self.assertIsInstance(error.stacktrace, str)
        self.assertGreater(len(error.stacktrace), 0)

    def test_stackframes(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'stackframes'))

        self.assertIsInstance(error.stackframes, list)
        self.assertGreater(len(error.stackframes), 0)

    def test_stackobjects(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'stackobjects'))

        self.assertIsInstance(error.stackobjects, list)
        self.assertGreater(len(error.stackobjects), 0)
        self.assertDeepEqual(error.stackobjects[0], [
            {
                'column': None,
                'file': '{0}/tests/test_errors.py'.format(ROOT_PATH),
                'function': 'test_stackobjects',
                'line': 209,
                'source': '        error = mybad.Error()\n',
            },
        ][0])

    def test_data(self):
        error = mybad.Error()

        self.assertTrue(hasattr(mybad.Error(), 'data'))

        self.assertIsInstance(error.data, dict)

        self.assertTrue(hasattr(error.data, 'type'))
        self.assertTrue(hasattr(error.data, 'id'))
        self.assertTrue(hasattr(error.data, 'code'))
        self.assertTrue(hasattr(error.data, 'key'))
        self.assertTrue(hasattr(error.data, 'message'))
        self.assertTrue(hasattr(error.data, 'details'))
        self.assertTrue(hasattr(error.data, 'stack'))

        self.assertEqual(error.data.type, 'BaseError')
        self.assertEqual(error.data.id, None)
        self.assertEqual(error.data.code, None)
        self.assertEqual(error.data.code, None)
        self.assertEqual(error.data.key, None)
        self.assertEqual(error.data.message, 'Unknown')
        self.assertEqual(error.data.details, {})
        self.assertDeepEqual(error.data.stack[0], [
            {
                'column': None,
                'file': '{0}/tests/test_errors.py'.format(ROOT_PATH),
                'function': 'test_data',
                'line': 226,
                'source': '        error = mybad.Error()\n',
            },
        ][0])

    def test_json(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'json'))

        _json = error.json()

        self.assertIsInstance(_json, str)

        data = AttributeDict(json.loads(_json))

        self.assertIsInstance(data, dict)

        self.assertTrue(hasattr(data, 'type'))
        self.assertTrue(hasattr(data, 'id'))
        self.assertTrue(hasattr(data, 'code'))
        self.assertTrue(hasattr(data, 'key'))
        self.assertTrue(hasattr(data, 'message'))
        self.assertTrue(hasattr(data, 'details'))
        self.assertTrue(hasattr(data, 'stack'))

        self.assertEqual(data.type, 'BaseError')
        self.assertEqual(data.id, None)
        self.assertEqual(data.code, None)
        self.assertEqual(data.code, None)
        self.assertEqual(data.key, None)
        self.assertEqual(data.message, 'Unknown')
        self.assertEqual(data.details, {})
        self.assertDeepEqual(data.stack[0], [
            {
                'column': None,
                'file': '{0}/tests/test_errors.py'.format(ROOT_PATH),
                'function': 'test_json',
                'line': 258,
                'source': '        error = mybad.Error()\n',
            },
        ][0])

    def test_inspect(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, 'inspect'))

        with self.assertNotRaises(Exception):
            error.inspect()

    def test___repr__(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, '__repr__'))

        self.assertIsInstance(repr(error), str)
        self.assertEqual(strip_ansi(repr(error)), 'Unknown')

        error = mybad.Error(TypeError('Boo'))

        self.assertIsInstance(repr(error), str)
        self.assertEqual(strip_ansi(repr(error)), 'Boo')

        error = mybad.Error(TypeError('Boo'), message = 'Boo-hoo')

        self.assertIsInstance(repr(error), str)
        self.assertEqual(strip_ansi(repr(error)), 'Boo-hoo')

    def test___str__(self):
        error = mybad.Error()

        self.assertTrue(hasattr(error, '__str__'))

        self.assertIsInstance(repr(error), str)
        self.assertEqual(strip_ansi(str(error)), 'Unknown')

        error = mybad.Error(TypeError('Boo'))

        self.assertIsInstance(repr(error), str)
        self.assertEqual(strip_ansi(str(error)), 'Boo')

        error = mybad.Error(TypeError('Boo'), message = 'Boo-hoo')

        self.assertIsInstance(repr(error), str)
        self.assertEqual(strip_ansi(str(error)), 'Boo-hoo')

    def test_cast(self):
        self.assertTrue(hasattr(mybad.Error, 'cast'))

        error = mybad.Error.cast(mybad.Error('Foo'))

        self.assertIsInstance(error, mybad.Error)

        error = mybad.Error.cast(TypeError('Foo'))

        self.assertIsInstance(error, mybad.Error)

    def test_object(self):
        self.assertTrue(hasattr(mybad.Error, 'object'))

        error_object = mybad.Error.object(mybad.Error('Foo'))

        self.assertIsInstance(error_object, attributedict.collections.AttributeDict)

        self.assertTrue(hasattr(error_object, 'type'))
        self.assertTrue(hasattr(error_object, 'id'))
        self.assertTrue(hasattr(error_object, 'code'))
        self.assertTrue(hasattr(error_object, 'key'))
        self.assertTrue(hasattr(error_object, 'message'))
        self.assertTrue(hasattr(error_object, 'details'))
        self.assertTrue(hasattr(error_object, 'stack'))

        self.assertEqual(error_object.type, 'BaseError')
        self.assertEqual(error_object.id, None)
        self.assertEqual(error_object.code, None)
        self.assertEqual(error_object.code, None)
        self.assertEqual(error_object.key, None)
        self.assertEqual(error_object.message, 'Foo')
        self.assertEqual(error_object.details, {})
        self.assertDeepEqual(error_object.stack[0], [
            {
                'column': None,
                'file': '{0}/tests/test_errors.py'.format(ROOT_PATH),
                'function': 'test_object',
                'line': 353,
                'source': '        error_object = mybad.Error.object(mybad.Error(\'Foo\'))\n',
            },
        ][0])

        class CustomError(mybad.Error):
            pass

        error_object = mybad.Error.object(CustomError('Bar'))

        self.assertIsInstance(error_object, attributedict.collections.AttributeDict)

        self.assertTrue(hasattr(error_object, 'type'))
        self.assertTrue(hasattr(error_object, 'id'))
        self.assertTrue(hasattr(error_object, 'code'))
        self.assertTrue(hasattr(error_object, 'key'))
        self.assertTrue(hasattr(error_object, 'message'))
        self.assertTrue(hasattr(error_object, 'details'))
        self.assertTrue(hasattr(error_object, 'stack'))

        self.assertEqual(error_object.type, 'CustomError')
        self.assertEqual(error_object.id, None)
        self.assertEqual(error_object.code, None)
        self.assertEqual(error_object.code, None)
        self.assertEqual(error_object.key, None)
        self.assertEqual(error_object.message, 'Bar')
        self.assertEqual(error_object.details, {})
        self.assertDeepEqual(error_object.stack[0], [
            {
                'column': None,
                'file': '{0}/tests/test_errors.py'.format(ROOT_PATH),
                'function': 'test_object',
                'line': 385,
                'source': '        error_object = mybad.Error.object(CustomError(\'Bar\'))\n',
            },
        ][0])

        error_object = mybad.Error.object(TypeError('Baz'))

        self.assertIsInstance(error_object, attributedict.collections.AttributeDict)

        self.assertTrue(hasattr(error_object, 'type'))
        self.assertTrue(hasattr(error_object, 'id'))
        self.assertTrue(hasattr(error_object, 'code'))
        self.assertTrue(hasattr(error_object, 'key'))
        self.assertTrue(hasattr(error_object, 'message'))
        self.assertTrue(hasattr(error_object, 'details'))
        self.assertTrue(hasattr(error_object, 'stack'))

        self.assertEqual(error_object.type, 'TypeError')
        self.assertEqual(error_object.id, None)
        self.assertEqual(error_object.code, None)
        self.assertEqual(error_object.code, None)
        self.assertEqual(error_object.key, None)
        self.assertEqual(error_object.message, 'Baz')
        self.assertEqual(error_object.details, {})
        self.assertDeepEqual(error_object.stack[0], [
            {
                'column': None,
                'file': '{0}/tests/test_errors.py'.format(ROOT_PATH),
                'function': 'test_object',
                'line': 414,
                'source': '        error_object = mybad.Error.object(TypeError(\'Baz\'))\n',
            },
        ][0])


# =========================================
#       MAIN
# --------------------------------------

if __name__ == '__main__':
    helper.run(TestCase)
