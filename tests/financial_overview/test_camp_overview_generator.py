from traka_automation.financial_overview.overview.generate_overview import (
    prepare_gnucash_xml,
)
from traka_automation.financial_overview.overview.get_camp_overview import (
    get_camp_overview,
)
from traka_automation.financial_overview.parser.parse_gnucash_xml import (
    parse_gnucash_xml,
)


def test_parse_gnucash_xml(gnucash_xml_location: str):
    accounts, transactions = parse_gnucash_xml(gnucash_xml_location)
    assert isinstance(accounts, dict)
    assert len(accounts) == 213

    assert accounts[next(iter(accounts.keys()))] == {
        "name": "Root Account",
        "parent": None,
        "type": "ROOT",
    }

    assert isinstance(transactions, list)
    assert len(transactions) == 12
    assert transactions[0] == {
        "account": "d13e8ce798cb41ec90fc81d7aa3c14e9",
        "amount": 50000.0,
        "memo": "",
        "description": "Test test",
        "year": "2026",
    }


def test_generate_overview(example_camp: str, gnucash_xml_location: str):
    accounts, transactions = prepare_gnucash_xml(gnucash_xml_location)
    overview = get_camp_overview(
        accounts=accounts, camp_name=example_camp, transactions=transactions, year=2026
    )
    assert isinstance(overview, dict)
    assert len(overview) == 8
    assert overview[next(iter(overview.keys()))] == [(" (Test test - 2)", -2500.0)]
