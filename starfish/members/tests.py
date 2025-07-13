import json
import os
from pathlib import Path, PurePath

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

    def test_zip(self):
        with Path(self.REGIONS_JSON).open("r") as f:
            regions_json = json.load(f)

        success_zips = {x["pk"] for x in regions_json if x["model"] == "regions.zip"}
        failure_zips = set(str(x).zfill(5) for x in range(100_000)) - success_zips

        def create_form(zip_code: str) -> PendingMemberForm:
            d = self.DEFAULT_FORM_DATA.copy()
            d["zip_code"] = zip_code
            return PendingMemberForm(d)

        for success_zip in success_zips:
            pcf = create_form(success_zip)
            is_valid = pcf.is_valid()
            if not is_valid:
                raise RuntimeError(success_zip, pcf.errors)
            self.assertEqual(pcf.cleaned_data["zip_code"].code, success_zip)

        EXPECTED_ZIP_ERROR = "Please enter a valid 5-digit ZIP Code."
        for failure_zip in failure_zips:
            pcf = create_form(failure_zip)
            self.assertFalse(pcf.is_valid())
            self.assertEqual(len(pcf.errors), 1)
            self.assertIn("zip_code", pcf.errors)
            errors = pcf.errors["zip_code"]
            self.assertEqual(len(errors), 1)
            self.assertEqual(errors[0], EXPECTED_ZIP_ERROR)

    def test_email(self):
        success_emails = {"name@domain.com", "first.last@google.com", "a@a.co"}
        failure_emails = {"", "name", "name@", "@", "@domain.com", "a@a.c"}

        def create_form(email: str) -> PendingMemberForm:
            d = self.DEFAULT_FORM_DATA.copy()
            d["email"] = email
            return PendingMemberForm(d)

        # FILL OUT THE FORM
        for success_email in success_emails:
            pcf = create_form(success_email)
            is_valid = pcf.is_valid()
            if not is_valid:
                raise RuntimeError(success_email, pcf.errors)
            self.assertEqual(pcf.cleaned_data["email"], success_email)

        # CREATE PENDING MEMBERS
        for email in success_emails:
            create_form(email).save()

        # FILL OUT THE FORM AGAIN, ALLOWED BECAUSE STILL PENDING
        for repeat_pending_email in success_emails:
            pcf = create_form(repeat_pending_email)
            is_valid = pcf.is_valid()
            if not is_valid:
                raise RuntimeError(repeat_pending_email, pcf.errors)
            self.assertEqual(pcf.cleaned_data["email"], repeat_pending_email)

        # VALIDATE PENDING MEMBERS
        for email in success_emails:
            create_form(email).save().validate_member()

        # FILL OUT THE FORM AGAIN, NOT ALLOWED BECAUSE MEMBER EXISTS
        EXPECTED_EMAIL_ALREADY_REGISTERED_ERROR = (
            "The email address entered is already registered."
        )
        for repeat_member_email in success_emails:
            pcf = create_form(repeat_member_email)
            is_valid = pcf.is_valid()
            if is_valid:
                raise RuntimeError(repeat_member_email)
            for field, errors in pcf.errors.items():
                if field != "email" or len(errors) != 1:
                    raise RuntimeError(repeat_member_email)
                actual_error = errors[0]
                self.assertEqual(actual_error, EXPECTED_EMAIL_ALREADY_REGISTERED_ERROR)

        # INVALID EMAILS
        for failure_email in failure_emails:
            pcf = create_form(failure_email)
            self.assertFalse(pcf.is_valid())
            self.assertEqual(len(pcf.errors), 1)
            self.assertIn("email", pcf.errors)
            errors = pcf.errors["email"]
            self.assertEqual(len(errors), 1)

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
