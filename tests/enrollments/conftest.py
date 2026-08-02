import json

import pytest

from traka_automation.util.config import secrets_config  # noqa: F401


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    secrets_config = { # noqa: F811,F841
        "ms_graph": {
            "tenant_id": "your-tenant-id",
            "client_id": "your-client-id",
            "client_secret": "your-client-secret",
        },
        "mollie": {
            "api_key": "xxxxx",
        },
        "dev": True
    }


@pytest.fixture
def enrollment_json():
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
