import pytest

from traka_automation.financial_overview.camp_overview_generator import CAMPS


@pytest.fixture
def gnucash_xml_location() -> str:
    return "tests/data/last_boekhouding.gnucash"


@pytest.fixture
def example_camp():
    return CAMPS[0]
