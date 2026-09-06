import pytest

from traka_automation.financial_overview.camp_overview_generator import CAMPS
from traka_automation.financial_overview.overview.generate_overview import (
    prepare_gnucash_xml,
)


@pytest.fixture
def gnucash_xml_location() -> str:
    return "tests/data/last_boekhouding.gnucash"


@pytest.fixture
def example_camp():
    return CAMPS[0]


@pytest.fixture
def accounts_transactions(gnucash_xml_location: str):
    return prepare_gnucash_xml(gnucash_xml_location)
