from __future__ import absolute_import, division, print_function, unicode_literals  # isort:skip # noqa

import unittest
from textwrap import dedent
from typing import DefaultDict, Dict, List, Mapping, Tuple, Union

import six

from python_to_typescript.base import generate_interfaces

LONG_TYPE = long if six.PY2 else int  # noqa


class SomeOtherType(object):
    pass


class BaseTypeConversionTestCase(unittest.TestCase):
    def test_basic_types(self):
        actual = generate_interfaces([
            ('SomeName', {
                'foo': six.binary_type,
                'bar': six.text_type,
                'an_int': int,
                'a_long': LONG_TYPE,
                'anything_else': SomeOtherType,
                'named_type': 'SomeOtherName',
                'named_bytes_type': b'SomeOtherName',
                'list_type': list,
                'object_type': dict,
                'string_or_number': (six.text_type, int),
                'null_type': None,
                'list_or_null': (None, list),
                'list_or_null_or_null': (None, list, None),
            }),
        ])
        expected = """\
        interface SomeName {
          a_long: number
          an_int: number
          anything_else: any
          bar: string
          foo: string
          list_or_null: any[] | null
          list_or_null_or_null: any[] | null
          list_type: any[]
          named_bytes_type: SomeOtherName
          named_type: SomeOtherName
          null_type: null
          object_type: object
          string_or_number: number | string
        }
        """

        assert actual == dedent(expected)

    def test_multiple_interfaces(self):
        actual = generate_interfaces([
            ('FirstInterface', {
                'x': six.binary_type,
            }),
            ('SecondInterface', {
                'y': int,
            }),
        ])
        expected = """\
        interface FirstInterface {
          x: string
        }

        interface SecondInterface {
          y: number
        }
        """

        assert actual == dedent(expected)

    def test_generic_types(self):
        actual = generate_interfaces([
            ('SomeOtherName', {
                'float_list': List[float],
                'number_or_string_list': List[Union[six.text_type, int]],
                'various_redundant_unions': (
                    Union[str, str, int],
                    int,
                    str,
                    Union[int, str],
                ),
                'redundant_union_of_lists': (
                    List[str],
                    Union[List[str], List[int]],
                    List[int],
                ),
                'list_of_lists': List[List[str]],
                'map_to_numbers': Mapping[str, int],
                'map_to_union': Mapping[int, Union[int, List[str]]],
                'dict': Dict[int, List[str]],
                'default_dict': DefaultDict[int, List[str]],
                'simple_tuple': Tuple[int, str, int],
                'complex_tuple': Tuple[
                    Tuple[int, str],
                    Union[List[str], List[int]],
                ],
            }),
        ])
        expected = """\
        interface SomeOtherName {
          complex_tuple: [[number, string], number[] | string[]]
          default_dict: {[key: string]: string[]}
          dict: {[key: string]: string[]}
          float_list: number[]
          list_of_lists: string[][]
          map_to_numbers: {[key: string]: number}
          map_to_union: {[key: string]: number | string[]}
          number_or_string_list: (number | string)[]
          redundant_union_of_lists: number[] | string[]
          simple_tuple: [number, string, number]
          various_redundant_unions: number | string
        }
        """

        assert actual == dedent(expected)
