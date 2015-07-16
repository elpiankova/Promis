from django.test import TestCase
from .models import Request
import datetime
from decimal import Decimal
from django.core.exceptions import ValidationError
class RequestValidatorTests(TestCase):






    def setUp(self):
        self.list_number = [1233, 12333]
        self.list_date_start = [datetime.datetime.now()] * 2
        self.list_date_end = [datetime.datetime.now()] * 2
        self.list_latitude_start = [Decimal("23.1"), Decimal("233.1")]
        self.list_longitude_left = [Decimal("233.1"), Decimal("2333.1")]
        self.list_longitude_right = [Decimal("233.1"), Decimal("2333.1")]
        self.list_device_amount = [1, 9]
        self.list_request_file = ["KNA3012170000.zp", "KNA3212170000"]

    def test_limitation_validator(self):

        normal_validation = Request(number=self.list_number[0], date_start=self.list_date_start[0],
                                    date_end=self.list_date_end[0], latitude_start=self.list_latitude_start[0],
                                    longitude_left=self.list_longitude_left[0],
                                    longitude_right=self.list_longitude_right[0],
                                    device_amount=self.list_device_amount[0],
                                    request_file=self.list_request_file[0])

        normal_validation.save()

    def test_limitation_validation_number(self):

        bad_validation_number = Request(number=self.list_number[1], date_start=self.list_date_start[0],
                                        date_end=self.list_date_end[0], latitude_start=self.list_latitude_start[0],
                                        longitude_left=self.list_longitude_left[0],
                                        longitude_right=self.list_longitude_right[0],
                                        device_amount=self.list_device_amount[0],
                                        request_file=self.list_request_file[0])
        try:
            bad_validation_number.save()
        except ValidationError as err:
            self.assertEqual(str(err), "{'number': ['Request number must be less than 9999']}")

    def test_limitation_validation_latitude_start(self):

        bad_validation_latitude_start = Request(
            number=self.list_number[0], date_start=self.list_date_start[0],
            date_end=self.list_date_end[0], latitude_start=self.list_latitude_start[1],
            longitude_left=self.list_longitude_left[0],
            longitude_right=self.list_longitude_right[0],
            device_amount=self.list_device_amount[0],
            request_file=self.list_request_file[0]
        )
        try:
            bad_validation_latitude_start.save()
        except ValidationError as err:
            self.assertEqual(str(err), "{'latitude_start': ['Request latitude start must be less then 82.0']}")

    def test_limitation_validation_longitude_left(self):

        bad_validation_longitude_left = Request(
            number=self.list_number[0], date_start=self.list_date_start[0],
            date_end=self.list_date_end[0], latitude_start=self.list_latitude_start[0],
            longitude_left=self.list_longitude_left[1],
            longitude_right=self.list_longitude_right[0],
            device_amount=self.list_device_amount[0],
            request_file=self.list_request_file[0]
        )
        try:
            bad_validation_longitude_left.save()
        except ValidationError as err:
            self.assertEqual(str(err), "{'longitude_left': ['Request longitude stop must be less then 359.0']}")

    def test_limitation_validation_longitude_right(self):

        bad_validation_longitude_right = Request(
            number=self.list_number[0], date_start=self.list_date_start[0],
            date_end=self.list_date_end[0], latitude_start=self.list_latitude_start[0],
            longitude_left=self.list_longitude_left[0],
            longitude_right=self.list_longitude_right[1],
            device_amount=self.list_device_amount[0],
            request_file=self.list_request_file[0]
        )
        try:
            bad_validation_longitude_right.save()
        except ValidationError as err:
            self.assertEqual(str(err), "{'longitude_right': ['Request longitude stop must be less then 359.0']}")

    def test_limitation_validation_device_amount(self):

        bad_validation_device_amount = Request(
            number=self.list_number[0], date_start=self.list_date_start[0],
            date_end=self.list_date_end[0], latitude_start=self.list_latitude_start[0],
            longitude_left=self.list_longitude_left[0],
            longitude_right=self.list_longitude_right[0],
            device_amount=self.list_device_amount[1],
            request_file=self.list_request_file[0]
        )
        try:
            bad_validation_device_amount.save()
        except ValidationError as err:
            self.assertEqual(str(err), "{'device_amount': ['Request device amount must be in range 1-8']}")

    def test_limitation_validation_request_file(self):

        bad_validation_request_file = Request(
            number=self.list_number[0], date_start=self.list_date_start[0],
            date_end=self.list_date_end[0], latitude_start=self.list_latitude_start[0],
            longitude_left=self.list_longitude_left[0],
            longitude_right=self.list_longitude_right[0],
            device_amount=self.list_device_amount[0],
            request_file=self.list_request_file[1]
        )
        try:
            bad_validation_request_file.save()
        except ValidationError as err:
            self.assertEqual(str(err), "{'request_file': ['Request file name should be KNAddmmyynnnn.zp']}")
# Create your tests here.



