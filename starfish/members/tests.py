import os
from pathlib import PurePath

from django.test import TestCase
from members.forms import PendingMemberForm
from regions.models import State, Zip

start_dir = PurePath(os.getcwd())
if start_dir.name != "starfish":
    start_dir /= "starfish"


# Create your tests here.
class TestPendingMemberForm(TestCase):
    SUCCESS_ZIP_CODE = "00501"
    FAILURE_ZIP_CODE = "00000"
    DEFAULT_FORM_DATA = {
        "name": "name",
        "email": "email@domain.com",
        "zip_code": SUCCESS_ZIP_CODE,
        "phone": "4054054050",
    }

    @classmethod
    def setUpTestData(cls) -> None:
        state_fixture = {
            "code": "NY",
            "name": "New York",
        }
        state = State.objects.create(**state_fixture)
        zip_fixture = {
            "code": cls.SUCCESS_ZIP_CODE,
            "state": state,
            "type": "UNIQUE",
            "primary_city": "Holtsville",
            "acceptable_cities": None,
            "county": "Suffolk County",
            "timezone": "America/New_York",
            "area_codes": "631",
            "latitude": 40.81,
            "longitude": -73.04,
            "population": 562,
        }
        Zip.objects.create(**zip_fixture)

    def test_zip(self):
        def create_form(zip_code: str) -> PendingMemberForm:
            d = self.DEFAULT_FORM_DATA.copy()
            d["zip_code"] = zip_code
            return PendingMemberForm(d)

        # PASSING EXAMPLE
        success_zip = self.SUCCESS_ZIP_CODE
        pcf = create_form(success_zip)
        is_valid = pcf.is_valid()
        if not is_valid:
            raise RuntimeError(success_zip, pcf.errors)
        self.assertEqual(pcf.cleaned_data["zip_code"].code, success_zip)

        # FAILING EXAMPLE
        failure_zip = self.FAILURE_ZIP_CODE
        pcf = create_form(failure_zip)
        self.assertFalse(pcf.is_valid())
        self.assertEqual(len(pcf.errors), 1)
        self.assertIn("zip_code", pcf.errors)
        errors = pcf.errors["zip_code"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0], "Please enter a valid 5-digit ZIP Code.")

    def test_email(self):
        """Tests behavior of form with respect to PendingMember and Member."""

        def create_form(email: str) -> PendingMemberForm:
            d = self.DEFAULT_FORM_DATA.copy()
            d["email"] = email
            return PendingMemberForm(d)

        # PASSING EXAMPLES
        success_emails = {"name@domain.com", "first.last@google.com", "a@a.co"}

        ## FILL OUT THE FORM, DO NOT CREATE PENDING MEMBERS
        for success_email in success_emails:
            pcf = create_form(success_email)
            is_valid = pcf.is_valid()
            if not is_valid:
                raise RuntimeError(success_email, pcf.errors)
            self.assertEqual(pcf.cleaned_data["email"], success_email)

        ## CREATE PENDING MEMBERS
        for email in success_emails:
            create_form(email).save()

        ## FILL OUT THE FORM AGAIN, PASSES BECAUSE PENDING MEMBER EXISTS
        for repeat_pending_email in success_emails:
            pcf = create_form(repeat_pending_email)
            is_valid = pcf.is_valid()
            if not is_valid:
                raise RuntimeError(repeat_pending_email, pcf.errors)
            self.assertEqual(pcf.cleaned_data["email"], repeat_pending_email)

        ## VALIDATE PENDING MEMBERS AS MEMBERS
        for email in success_emails:
            create_form(email).save().validate_member()

        ## FILL OUT THE FORM AGAIN, FAILS BECAUSE MEMBER EXISTS
        for repeat_member_email in success_emails:
            pcf = create_form(repeat_member_email)
            self.assertFalse(pcf.is_valid())
            self.assertEqual(len(pcf.errors), 1)
            self.assertIn("email", pcf.errors)
            errors = pcf.errors["email"]
            self.assertEqual(len(errors), 1)
            self.assertEqual(
                errors[0],
                "The email address entered is already registered.",
            )

        # FAILING EXAMPLES
        failure_emails = {"", "name", "name@", "@", "@domain.com", "a@a.c"}
        for failure_email in failure_emails:
            pcf = create_form(failure_email)
            self.assertFalse(pcf.is_valid())
            self.assertEqual(len(pcf.errors), 1)
            self.assertIn("email", pcf.errors)
            errors = pcf.errors["email"]
            self.assertEqual(len(errors), 1)
            # no need to test django built-in error text

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
