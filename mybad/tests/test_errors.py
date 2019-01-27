
# =========================================
#       IMPORTS
# --------------------------------------

from os import environ as env

import rootpath

rootpath.append()

from mybad.tests import helper

import mybad

env['COLORS'] = 'true' # lower prio
env['VERBOSE'] = 'true' # lower prio

env['ERROR_COLORS'] = 'false' # higher prio
env['ERROR_VERBOSE'] = 'false' # higher prio


# =========================================
#       TEST
# --------------------------------------

class TestCase(helper.TestCase):

    # NOTE: quite basic test right now, should add more advanced error message formatting assertions

    def test__import(self):
        self.assertModule(mybad)

    def test__instance(self):
        self.assertIsInstance(mybad.Error(), mybad.Error)

    def test_error(self):
        self.assertTrue(hasattr(mybad.Error(), 'error'))

        some_raised_error = TypeError('No good')

        with self.assertNotRaises(Exception):
            error = mybad.Error(some_raised_error)

        self.assertIsInstance(error.error, TypeError)
        self.assertEqual(str(error.error), 'No good')

    def test_id(self):
        self.assertTrue(hasattr(mybad.Error(), 'id'))

        with self.assertNotRaises(Exception):
            error = mybad.Error()

        self.assertIsInstance(error.id, type(None))
        self.assertEqual(error.id, None)

        with self.assertNotRaises(Exception):
            error = mybad.Error(id = 123)

        self.assertIsInstance(error.id, int)
        self.assertEqual(error.id, 123)

        with self.assertNotRaises(Exception):
            error = mybad.Error(id = '123')

        self.assertIsInstance(error.id, str)
        self.assertEqual(error.id, '123')

    def test_key(self):
        self.assertTrue(hasattr(mybad.Error(), 'key'))

        with self.assertNotRaises(Exception):
            error = mybad.Error()

        self.assertIsInstance(error.key, type(None))
        self.assertEqual(error.key, None)

        with self.assertNotRaises(Exception):
            error = mybad.Error(key = 123)

        self.assertIsInstance(error.key, int)
        self.assertEqual(error.key, 123)

        with self.assertNotRaises(Exception):
            error = mybad.Error(key = '123')

        self.assertIsInstance(error.key, str)
        self.assertEqual(error.key, '123')

    def test_code(self):
        self.assertTrue(hasattr(mybad.Error(), 'code'))

        error = mybad.Error()

        self.assertIsInstance(error.code, type(None))
        self.assertEqual(error.code, None)

        with self.assertNotRaises(Exception):
            error = mybad.Error(code = 123)

        self.assertIsInstance(error.code, int)
        self.assertEqual(error.code, 123)

        with self.assertNotRaises(Exception):
            error = mybad.Error(code = '123')

        self.assertIsInstance(error.code, str)
        self.assertEqual(error.code, '123')

    def test_message(self):
        self.assertTrue(hasattr(mybad.Error(), 'message'))

        with self.assertNotRaises(Exception):
            error = mybad.Error()

        self.assertIsInstance(error.message, str)
        self.assertEqual(error.message, 'Unknown')

        with self.assertNotRaises(Exception):
            error = mybad.Error(message = 123)

        self.assertIsInstance(error.message, str)
        self.assertEqual(error.message, '123')

        with self.assertNotRaises(Exception):
            error = mybad.Error(message = '123')

        self.assertIsInstance(error.message, str)
        self.assertEqual(error.message, '123')

    def test_details(self):
        self.assertTrue(hasattr(mybad.Error(), 'details'))

        with self.assertNotRaises(Exception):
            error = mybad.Error()

        self.assertIsInstance(error.details, dict)
        self.assertEqual(error.details, {})

        with self.assertRaises(TypeError):
            error = mybad.Error(details = 123)

        with self.assertRaises(TypeError):
            error = mybad.Error(details = '123')

        with self.assertNotRaises(Exception):
            error = mybad.Error(details = {})

        self.assertIsInstance(error.details, dict)
        self.assertEqual(error.details, {})

        with self.assertNotRaises(Exception):
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
        self.assertTrue(hasattr(mybad.Error(), 'stack'))

        error = mybad.Error()

        self.assertIsInstance(error.stack, list)
        self.assertGreater(len(error.stack), 0)

    def test_stacktrace(self):
        self.assertTrue(hasattr(mybad.Error(), 'stacktrace'))

        with self.assertNotRaises(Exception):
            error = mybad.Error()

        self.assertIsInstance(error.stacktrace, str)
        # self.assertEqual(error.stacktrace, 'NoneType: None')

    def test___str__(self):
        self.assertTrue(hasattr(mybad.Error(), '__str__'))

        self.assertIsInstance(str(mybad.Error()), str)
        self.assertEqual(str(mybad.Error()), 'Unknown')
        self.assertEqual(str(mybad.Error(TypeError('Boo'))), 'Boo')
        self.assertEqual(str(mybad.Error(TypeError('Boo'), message = 'Boo-hoo')), 'Boo-hoo')


# =========================================
#       MAIN
# --------------------------------------

if __name__ == '__main__':
    helper.run(TestCase)
