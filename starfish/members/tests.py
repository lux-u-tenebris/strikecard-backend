import os
from pathlib import PurePath

from django.core.management import call_command
from django.test import TestCase
from members.forms import PendingMemberForm

start_dir = PurePath(os.getcwd())
if start_dir.name != "starfish":
    start_dir /= "starfish"


# Create your tests here.
class TestPendingMemberForm(TestCase):
    REGIONS_JSON = start_dir / "regions/fixtures/regions.json"
    DEFAULT_FORM_DATA = {
        "name": "name",
        "email": "email@domain.com",
        "zip_code": "00501",
        "phone": "4054054050",
    }

    @classmethod
    def setUpTestData(cls) -> None:
        call_command("loaddata", cls.REGIONS_JSON)

    def test_phone(self):
        EXPECTED_PHONE_ERROR = r"""Please enter a 10-digit phone number."""
        success_phones = {
            "202 212 2220": "2022122220",
            "404 444 4040": "4044444040",
            "4054054050": "4054054050",
            "(405) 405-4050": "4054054050",
            "405-405-4050": "4054054050",
            "405.405.4050": "4054054050",
            "\t405&&405+4050": "4054054050",
        }
        failure_phones = {
            # GENERAL ERRORS
            "": EXPECTED_PHONE_ERROR,
            "1": EXPECTED_PHONE_ERROR,
            "22": EXPECTED_PHONE_ERROR,
            "203": EXPECTED_PHONE_ERROR,
            "2034": EXPECTED_PHONE_ERROR,
            "20345": EXPECTED_PHONE_ERROR,
            "203456": EXPECTED_PHONE_ERROR,
            "2034567": EXPECTED_PHONE_ERROR,
            "20345678": EXPECTED_PHONE_ERROR,
            "203456789": EXPECTED_PHONE_ERROR,
            "a": EXPECTED_PHONE_ERROR,
            # AREA CODE ERRORS
            "012 345 6789": EXPECTED_PHONE_ERROR,  # leading 0
            "102 345 6789": EXPECTED_PHONE_ERROR,  # leading 1
            "370 234 5678": EXPECTED_PHONE_ERROR,  # 370-379
            "371 234 5678": EXPECTED_PHONE_ERROR,  # 370-379
            "372 234 5678": EXPECTED_PHONE_ERROR,  # 370-379
            "373 234 5678": EXPECTED_PHONE_ERROR,  # 370-379
            "374 234 5678": EXPECTED_PHONE_ERROR,  # 370-379
            "375 234 5678": EXPECTED_PHONE_ERROR,  # 370-379
            "376 234 5678": EXPECTED_PHONE_ERROR,  # 370-379
            "377 234 5678": EXPECTED_PHONE_ERROR,  # 370-379
            "378 234 5678": EXPECTED_PHONE_ERROR,  # 370-379
            "379 234 5678": EXPECTED_PHONE_ERROR,  # 370-379
            "960 234 5678": EXPECTED_PHONE_ERROR,  # 960-969
            "961 234 5678": EXPECTED_PHONE_ERROR,  # 960-969
            "962 234 5678": EXPECTED_PHONE_ERROR,  # 960-969
            "963 234 5678": EXPECTED_PHONE_ERROR,  # 960-969
            "964 234 5678": EXPECTED_PHONE_ERROR,  # 960-969
            "965 234 5678": EXPECTED_PHONE_ERROR,  # 960-969
            "966 234 5678": EXPECTED_PHONE_ERROR,  # 960-969
            "967 234 5678": EXPECTED_PHONE_ERROR,  # 960-969
            "968 234 5678": EXPECTED_PHONE_ERROR,  # 960-969
            "969 234 5678": EXPECTED_PHONE_ERROR,  # 960-969
            "950 234 5678": EXPECTED_PHONE_ERROR,  # 950
            "958 234 5678": EXPECTED_PHONE_ERROR,  # 958
            "959 234 5678": EXPECTED_PHONE_ERROR,  # 959
            "911 345 6789": EXPECTED_PHONE_ERROR,  # 2nd & 3rd same
            "888 234 5678": EXPECTED_PHONE_ERROR,  # 2nd & 3rd same
            "290 234 5678": EXPECTED_PHONE_ERROR,  # middle 9
            # PREFIX ERRORS
            "202 012 5678": EXPECTED_PHONE_ERROR,  # leading 0
            "202 102 5678": EXPECTED_PHONE_ERROR,  # leading 1
            "202 555 5678": EXPECTED_PHONE_ERROR,  # 555
            "202 911 5678": EXPECTED_PHONE_ERROR,  # 2nd & 3rd same
        }

        def create_form(phone: str) -> PendingMemberForm:
            d = self.DEFAULT_FORM_DATA.copy()
            d["phone"] = phone
            return PendingMemberForm(d)

        for actual, expected in success_phones.items():
            pcf = create_form(actual)
            is_valid = pcf.is_valid()
            if not is_valid:
                raise RuntimeError(actual, pcf.errors)
            self.assertEqual(pcf.cleaned_data["phone"], expected)

        for failure_phone, expected_error in failure_phones.items():
            pcf = create_form(failure_phone)
            self.assertFalse(pcf.is_valid())
            self.assertEqual(len(pcf.errors), 1)
            self.assertIn("phone", pcf.errors)
            errors = pcf.errors["phone"]
            self.assertEqual(len(errors), 1)
            self.assertEqual(errors[0], expected_error)
