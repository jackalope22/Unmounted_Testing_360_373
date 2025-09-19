__doc__ = '''
CEnum is a (Python 3) Enum subclass which behaves like C/C++ enums --
anyway, as much like them as an Enum subclass can.
See the class docstring for usage and examples (doctests).

The Enum docs contain an example class AutoNumber:
    https://docs.python.org/3/library/enum.html?highlight=enum#autonumber
which lacks some important functionality of C/C++ enums. CEnum gets
closer to the mark.

This class is for Python 3 only -- the doctests fail in Py2.7.12,
and presently I'm uninterested in figuring out why.


License -- MIT License
----------------------
Copyright (c) 2014-2016 Brian O'Neill

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:
The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
__author__ = 'brianoneill'
__version__ = '1.0'

import sys
from enum import IntEnum
if sys.version_info.major <= 2:
    raise NotImplementedError("CEnum doesn't work properly under Python 2.")


class CEnum(IntEnum):
    """
    An Enum subclass that behaves like C/C++ enums.
    Assign a value of `None` (or any falsy value other than `False`) to
        * an enum member whose value is to be 1 greater than that of
          its predecessor, or
        * to the first enum member, to make its value 0.
    Assigning a value of `False` to an enum member *skips that enum member* (!)

    >>> class Color(CEnum):
    ...     red = 107
    ...     green = None
    ...     blue = 0
    ...     cyan = None
    ...     purple = None
    >>> [e for e in Color]
    [<Color.red: 107>, <Color.green: 108>, <Color.blue: 0>, <Color.cyan: 1>, <Color.purple: 2>]

    >>> class Errors(CEnum):
    ...     OK = None
    ...     FILE_NOT_FOUND = None
    ...     ERROR_OPENING_FILE = None
    ...     ERROR_READING_FILE = 8
    ...     ERROR_WRITING_FILE = None
    ...     ERROR_CLOSING_FILE = None
    >>> Errors.OK.value
    0
    >>> Errors.ERROR_OPENING_FILE.value
    2
    >>> Errors.ERROR_WRITING_FILE.value
    9

    >>> class FalseValSkipped(CEnum):
    ...     first = None
    ...     skipped = False
    ...     two = []
    >>> [(e.name, e.value) for e in FalseValSkipped]
    [('first', 0), ('two', 1)]

    >>> class BadVal(CEnum):
    ...     huh = 'say what?'       # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Bad value: 'say what?'
    """
    def __new__(cls, value_param=None):
        is_int = isinstance(value_param, int)
        #obj = object.__new__(cls)  # 'not safe' warning issued, use int.__new__() instead!
        obj = int.__new__(cls)

        if is_int:
            value = int(value_param)
        elif not value_param:
            # Note, this allows (), [], and other falsy values.
            # But if value_param is False, this member won't be added.
            members = cls.__members__
            if members:       # new val = prev val + 1
                prev_member = tuple(members.values())[-1]
                value = prev_member.value + 1
            else:             # adding first member
                value = 0
        else:
            raise ValueError("Bad value: %r" % value_param)

        obj._value_ = value
        return obj

    # need this method to make the enum c_types compatible
    @classmethod
    def from_param(cls, obj):
        if hasattr(obj, "value"): # if enum is initialized by an enum value
            return obj.value
        else:                     # if enum is initialized by an int
            return obj

    def __eq__(self, other):
        if hasattr(self, "value") and hasattr(other, "value"):
            return self.value == other.value
        elif hasattr(self, "value"):
            return self.value == other  # allow comparing a c_enum to an integer
        else:
            return self == other

    def __ne__(self, other):
        return not self == other

if __name__ == '__main__':
    import doctest
    doctest.testmod()
