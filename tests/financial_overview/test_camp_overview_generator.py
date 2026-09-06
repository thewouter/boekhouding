from pathlib import Path
from typing import Any

import traka_automation.financial_overview.parser.copy_xml_file_to_location as xml_module
from traka_automation.financial_overview.camp_overview_generator import process_camp
from traka_automation.financial_overview.overview.generate_overview import (
    prepare_gnucash_xml,
)
from traka_automation.financial_overview.overview.get_camp_overview import (
    get_camp_overview,
)
from traka_automation.financial_overview.overview.save_camp_overview import (
    save_camp_overview,
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


def test_save_overview(
    tmp_path: Path,
    example_camp: str,
    accounts_transactions: tuple[dict[Any, Any], list[Any]],
):
    accounts, transactions = accounts_transactions
    overview = get_camp_overview(
        accounts=accounts, camp_name=example_camp, transactions=transactions, year=2026
    )
    overview_file_path = tmp_path / f"overzicht_{example_camp}.txt"
    save_camp_overview(overview, overview_file_path)

    assert overview_file_path.exists()
    with open(overview_file_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert " (Test test - 2)" in content
        assert "-€2500.00" in content
        for tag in [
            "Voorbereidingen",
            "Vervoerskosten",
            "Gebouwen en terreinen",
            "Programmakosten",
            "Voeding",
            "Organisatiekosten",
            "Deelnemersbijdragen",
            "Stafbijdragen",
        ]:
            assert tag in content


def test_process_camp(
    accounts_transactions: tuple[dict[Any, Any], list[Any]],
    example_camp: str,
    tmp_path: Path,
):
    xml_module.SAVE_LOCATION = tmp_path  # type: ignore
    assert xml_module.SAVE_LOCATION.exists()  # type: ignore
    (xml_module.SAVE_LOCATION / "kampoverzichten").mkdir(parents=True, exist_ok=True)  # type: ignore
    process_camp(example_camp, *accounts_transactions)
    assert (
        xml_module.SAVE_LOCATION / f"kampoverzichten/overzicht_{example_camp}.txt"  # type: ignore
    ).exists()
