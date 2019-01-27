
# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()


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

        print('PRINT {0}'.format(''.join(stash)))

    except Exception as error:
        raise ToMuchError(error,
            message = "Out of money printing ink...",
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

    print_money(amount)

