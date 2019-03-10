
# `mybad` [![PyPI version](https://badge.fury.io/py/mybad.svg)](https://badge.fury.io/py/mybad) [![Build Status](https://travis-ci.com/grimen/python-mybad.svg?branch=master)](https://travis-ci.com/grimen/python-mybad) [![Coverage Status](https://codecov.io/gh/grimen/python-mybad/branch/master/graph/badge.svg)](https://codecov.io/gh/grimen/python-mybad)

*My friendly error base class - for Python.*

## Introduction

One in general always needs a application/library specific error base class, but the native errors are very limited in what meta/debugging information they can hold at time they are raised. For better debugging and error reporting/inspection this error base class allows to attach some additonal error context information that can be used to better understand the issue - without having to create custom error formatters, or run debugger.


## Install

Install using **pip**:

```sh
$ pip install mybad
```


## Use

Very basic **[example](https://github.com/grimen/python-mybad/tree/master/examples/basic.py)**:

```python
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

```

Run this with optional environment variables `COLORS` / `ERROR_COLORS` and/or `VERBOSE` / `ERROR_VERBOSE` set too truthy or falsy values, so see various error info formatting in terminal.

Something like this (imagine some colorized formatting):

```bash
PRINT $
PRINT $$
PRINT $$$
PRINT $$$$
PRINT $$$$$
PRINT $$$$$$
PRINT $$$$$$$
PRINT $$$$$$$$
PRINT $$$$$$$$$
PRINT $$$$$$$$$$
PRINT $$$$$$$$$$$
PRINT $$$$$$$$$$$$
PRINT $$$$$$$$$$$$$
Traceback (most recent call last):
  File "examples/basic.py", line 25, in print_money
    raise Exception('Too much money to print: {0}'.format(stash))
Exception: Too much money to print: $$$$$$$$$$$$$$

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "examples/basic.py", line 45, in <module>
    print_money(amount)
  File "examples/basic.py", line 36, in print_money
    stash = stash,
__main__.ToMuchError: Out of money printing ink... - {'stash': '$$$$$$$$$$$$$$'}
```


## Test

Clone down source code:

```sh
$ make install
```

Run **colorful tests**, with only native environment (dependency sandboxing up to you):

```sh
$ make test
```

Run **less colorful tests**, with **multi-environment** (using **tox**):

```sh
$ make test-tox
```


## Related

- [**`mybase`**](https://github.com/grimen/python-mybase) - *"My friendly library base class - for Python"*


## About

This project was mainly initiated - in lack of solid existing alternatives - to be used at our work at **[Markable.ai](https://markable.ai)** to have common code conventions between various programming environments where **Python** (research, CV, AI) is heavily used.


## License

Released under the MIT license.
