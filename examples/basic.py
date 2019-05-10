
# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()

import json


# =========================================
#       EXAMPLE
# --------------------------------------

# NOTE: just a very simple maybe non-saying example for now, should add more advanced examples eventually

from mybad import Error

class ToMuchError(Error):
    pass

def print_money(stash):
    try:
        if isinstance(stash, str) and len(stash) > 13:
            raise Exception('Too much money to print: {0}'.format(stash))

        print('PRINT {0}'.format(stash))

    except Exception as error:
        raise ToMuchError(error,
            message = 'Out of money printing ink...',
            id = hash(stash),
            key = 'too_much',
            code = 400,
            details = dict(
                stash = stash,
            )
        )

amount = ''

for dollar in range(42):
    amount += '$'

    try:
        print_money(amount)

    except Exception as error:
        print('===============================')
        print('     str(error)')
        print('---------------------------')
        print(str(error))
        print()

        print('===============================')
        print('     error.stack')
        print('---------------------------')
        print(error.stack)

        print('===============================')
        print('     error.inspect()')
        print('---------------------------')
        print(error.inspect(colors = True, verbose = True))
        print()

        print('===============================')
        print('     error.json()')
        print('---------------------------')
        print(error.json())
        print()

        break
