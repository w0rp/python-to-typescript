"""
Basic functions for generating TypeScript interfaces from Python types.
"""
from __future__ import absolute_import, division, print_function, unicode_literals  # isort:skip # noqa

import itertools
from typing import Mapping, Sequence, Set, Tuple, Union

import six

NUMBER_TYPES = (int, float)

if six.PY2:  # pragma: no cover
    NUMBER_TYPES += (long,)  # noqa


class JSONTypeClass(object):
    pass


# A special type for denoting something is JSON.
JSON_TYPE = JSONTypeClass()


def uniq(iterable, key=None):
    """
    Generate items where subsequent duplicates are eliminated.
    """
    return (x[0] for x in itertools.groupby(iterable, key))


def group_type(type_string):
    """
    Surround a type with parentheses as needed.
    """
    return (
        '(' + type_string + ')'
        if '|' in type_string else
        type_string
    )


def _get_type_name_list(type_or_tuple):
    name_list = []
    field_types = (
        type_or_tuple
        if isinstance(type_or_tuple, tuple) else
        (type_or_tuple,)
    )

    for some_type in field_types:
        if some_type is None or some_type is type(None): # noqa
            name_list.append('null')
        elif getattr(some_type, '__origin__', None) is Union:
            for union_type in some_type.__args__:
                name_list.extend(_get_type_name_list(union_type))
        elif issubclass(getattr(some_type, '__origin__', type), Tuple):
            tuple_types = (type_name(x) for x in some_type.__args__)
            name_list.append('[{}]'.format(', '.join(tuple_types)))
        elif issubclass(getattr(some_type, '__origin__', type), Sequence):
            name_list.append(
                group_type(type_name(some_type.__args__[0])) + '[]'
            )
        elif issubclass(getattr(some_type, '__origin__', type), Set):
            name_list.append(
                group_type(type_name(some_type.__args__[0])) + '[]'
            )
        elif issubclass(getattr(some_type, '__origin__', type), Mapping):
            # The key type always has to be a number or string for JS.
            # Serialized as JSON, we'll only ever have strings as keys.
            name_list.append(
                '{{[key: string]: {}}}'
                .format(type_name(some_type.__args__[1]))
            )
        elif isinstance(some_type, six.binary_type):
            name_list.append(some_type.decode('utf-8'))
        elif isinstance(some_type, six.text_type):
            name_list.append(some_type)
        # Check this first to avoid exceptions with issubclass
        elif not issubclass(type(some_type), type):
            name_list.append('any')
        elif issubclass(some_type, six.binary_type):
            name_list.append('string')
        elif issubclass(some_type, six.text_type):
            name_list.append('string')
        elif issubclass(some_type, bool):
            name_list.append('boolean')
        elif issubclass(some_type, NUMBER_TYPES):
            name_list.append('number')
        elif issubclass(some_type, list):
            name_list.append('any[]')
        elif issubclass(some_type, dict):
            name_list.append('object')
        else:
            name_list.append('any')

    return list(
        # Sort types, and put null last
        uniq(sorted(name_list, key=lambda name: (name == 'null', name)))
    )


def type_name(type_or_tuple):
    """
    Given some Python type or a string for naming another TypeSscript
    interface, return a string representing the type in TypeScript.
    """
    return ' | '.join(_get_type_name_list(type_or_tuple))


def generate_interfaces(python_types, indentation=2, newline='\n'):
    """
    Generate TypeScript interfaces from python types. python_types must
    be in the format [(interface_name, type_mapping), ...]

    For example:
    >>> print(generate_interfaces([('SomeInterface', {'b': str, 'a': int})]))
    interface SomeInterface {
      a: number
      b: string
    }

    The members of the interface will be sorted by name.
    """
    lines = []

    indentation_text = ' ' * indentation

    for index, (interface_name, field_dict) in enumerate(python_types):
        if index > 0:
            lines.append('')

        lines.append('interface {} {{'.format(interface_name))

        for field_name, type_or_tuple in sorted(
            six.iteritems(field_dict),
            key=lambda x: x[0]
        ):
            lines.append('{}{}: {}'.format(
                indentation_text,
                field_name,
                type_name(type_or_tuple),
            ))

        lines.append('}')

    return newline.join(lines) + newline
