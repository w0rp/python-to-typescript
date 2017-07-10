from __future__ import absolute_import, division, print_function, unicode_literals  # isort:skip # noqa

import unittest
from textwrap import dedent

from rest_framework.serializers import (
    BooleanField,
    CharField,
    ChoiceField,
    DateField,
    DateTimeField,
    DecimalField,
    DictField,
    DurationField,
    EmailField,
    FileField,
    FilePathField,
    FloatField,
    ImageField,
    IntegerField,
    IPAddressField,
    JSONField,
    ListField,
    MultipleChoiceField,
    NullBooleanField,
    RegexField,
    Serializer,
    SlugField,
    TimeField,
    URLField,
    UUIDField,
)

from ..drf import generate_interfaces_from_serializer


class DRFSerializerTestCase(unittest.TestCase):
    def test_basic_fields(self):
        class TestSerializer(Serializer):  # pylint: disable=abstract-method
            boolean_field = BooleanField()
            char_field = CharField()
            choice_field = ChoiceField([])
            date_field = DateField()
            date_time_field = DateTimeField()
            decimal_field = DecimalField(1, 1)
            dict_field = DictField()
            duration_field = DurationField()
            email_field = EmailField()
            file_field = FileField()
            file_path_field = FilePathField('')
            float_field = FloatField()
            image_field = ImageField()
            integer_field = IntegerField()
            ip_address_field = IPAddressField()
            json_field = JSONField()
            string_list_field = ListField(child=CharField())
            int_list_field = ListField(child=IntegerField())
            int_list_list_field = ListField(
                child=ListField(
                    child=IntegerField(),
                ),
            )
            multiple_choice_field = MultipleChoiceField([])
            null_boolean_field = NullBooleanField()
            regex_field = RegexField('')
            slug_field = SlugField()
            time_field = TimeField()
            url_field = URLField()
            uuid_field = UUIDField()
            nullable_char_field = CharField(allow_null=True)
            nullable_char_listfield = ListField(
                child=CharField(allow_null=True),
            )
            write_only_field = CharField(write_only=True)

        actual = generate_interfaces_from_serializer(TestSerializer)
        expected = """\
        interface Test {
          boolean_field: boolean
          char_field: string
          choice_field: string
          date_field: string
          date_time_field: string
          decimal_field: string
          dict_field: {[key: string]: any}
          duration_field: string
          email_field: string
          file_field: string
          file_path_field: string
          float_field: number
          image_field: string
          int_list_field: number[]
          int_list_list_field: number[][]
          integer_field: number
          ip_address_field: string
          json_field: any
          multiple_choice_field: string[]
          null_boolean_field: boolean | null
          nullable_char_field: string | null
          nullable_char_listfield: (string | null)[]
          regex_field: string
          slug_field: string
          string_list_field: string[]
          time_field: string
          url_field: string
          uuid_field: string
        }
        """

        assert actual == dedent(expected)

    def test_model_fields(self):
        # ModelField has the .model_field attribute
        pass
