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

    assert accounts[list(accounts.keys())[0]] == {
        "name": "Root Account",
        "parent": None,
        "type": "ROOT",
    }

    assert isinstance(transactions, list)
    assert len(transactions) == 3572
    assert transactions[0] == {
        "account": "d13e8ce798cb41ec90fc81d7aa3c14e9",
        "amount": 378.69,
        "description": "Openingsbalans Betaalrekening",
        "memo": "",
        "year": "2025",
    }

def test_generate_overview(example_camp: str, gnucash_xml_location: str):
    accounts, transactions = prepare_gnucash_xml(gnucash_xml_location)
    overview = get_camp_overview(
        accounts=accounts, camp_name=example_camp, transactions=transactions, year=2025
    )
    assert isinstance(overview, dict)
    assert len(overview) == 8
    assert overview[list(overview.keys())[0]] == [
        ("Voedsel uitzetweekeind (5/11 pers) (Niels Bloemendaal)", -69.35),
        (
            "Huur Ferschweiler uitzetweekend overnachtingen  (Ortsgemeinde Ferschweiler)",
            -42.0,
        ),
        ("Huur Ferschweiler uitzetweekend gebouw (Ortsgemeinde Ferschweiler)", -17.5),
        ("Brandstof uitzetweekend Camiela (Camiela Jonker)", -42.61),
    ]
