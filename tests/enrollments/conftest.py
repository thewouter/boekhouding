import json

import pytest

from traka_automation.enrollments.enrollment.camp import Camp
from traka_automation.enrollments.enrollment.enrollment_web_form import (
    EnrollmentWebForm,
)


@pytest.fixture
def example_enrollment_json() -> dict:
    return json.loads("""{
      "$schema": "https://www.trapperskamp.com/schemas/signup.json",
      "type": "SignupForm",
      "activity": {
        "type": "Activity",
        "name": "Jungle Adventure",
        "edition": 42,
        "startDate": "2027-07-12",
        "endDate": "2027-07-19",
        "price": 175.5
     },
      "participants": [
        {
          "type": "Participant",
          "name": "Jan Jansen",
          "birthDate": "2016-03-15",
          "emailAddress": "wouter@woutervanharten.nl",
          "address": "Voorbeeldstraat 1",
          "zipCode": "1234 AB",
          "city": "Voorbeeldstad",
          "telephoneMobile": "06-12345678",
          "dietaryRestrictions": "Ik mag geen rijst op woensdagen",
          "backupName": "Papa of Mama",
          "photo": "fotodieiknetgenomenheb.jpg",
          "backupPhone": "06-12345688",
          "backupEmailAddress": "backup1@test.nl",
          "membership": {
            "type": "Membership",
            "memberId": "SN-98765",
            "group": {
              "type": "Group",
              "city": "Delft",
              "name": "Scouting Orion"
           },
            "ageGroup": "Welpen"
         }
       },
        {
          "type": "Participant",
          "name": "Piet Jansen",
          "birthDate": "1940-03-15",
          "emailAddress": "wouter.van.harten@trapperskamp.com",
          "address": "Voorbeeldstraat 3",
          "zipCode": "1234 AC",
          "city": "Voorbeeldstad",
          "telephoneMobile": "06-12345678",
          "dietaryRestrictions": "Ik mag geen rijst op dinsdagen",
          "backupName": "Mijn echtgenoot of echtgenote",
          "photo": "fotodieiknetgenomenheb.jpg",
          "backupPhone": "06-12345688",
          "backupEmailAddress": "backup1@test.nl",
          "membership": {
            "type": "Membership",
            "memberId": "SN-98765",
            "group": {
              "type": "Group",
              "city": "Delft",
              "name": "Scouting Orion"
           },
            "ageGroup": "Welpen"
         }
       }
     ],
      "consent": {
        "type": "ParentalConsent",
        "given": true
     },
      "origin": {
        "type": "Meta",
        "originatingAddress": "198.51.100.10",
        "timestamp": "2025-11-05T17:35:17.123Z"
     }
    }""")


@pytest.fixture
def example_enrollment_web_form(example_enrollment_json: dict) -> EnrollmentWebForm:
    return EnrollmentWebForm.from_json(example_enrollment_json, uuid="test-uuid")


@pytest.fixture
def example_camp(example_enrollment_web_form: EnrollmentWebForm) -> Camp:
    return example_enrollment_web_form.camp
