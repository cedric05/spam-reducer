from app import *
import os
from unittest import TestCase

test_email = "kesavarapu.siva@gmail.com"
invalid_email = "haha.com"


class TestSpam(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(SQLITE_STORE)

    def test_a1_validate_email(self):
        self.assertTrue(validate_email(test_email))
        self.assertFalse(validate_email(invalid_email))

    def test_a2_register_emaiL(self):
        registerEmail(test_email)
        try:
            check_email_exists(email=test_email)
        except:
            self.fail("should not fail")
        self.assertFalse(check_email_exists(email=test_email + "test"))

    def test_a3_generate_email(self):
        generateEmail(test_email, "test usecases")
        list_emails = listEmail(test_email)
        self.generated = list_emails.get("filters")[0]["generated"]
        enableEmail(test_email, self.generated, False) # disabled
        list_emails = listEmail(test_email)
        self.assertFalse(list_emails.get('filters')[0]['enabled'])
        enableEmail(test_email, self.generated, True)
        list_emails = listEmail(test_email)
        self.assertTrue(list_emails.get('filters')[0]['enabled'])
