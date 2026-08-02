import shutil
from collections import defaultdict
from datetime import UTC, datetime

from traka_automation.financial_overview.overview.get_camp_overview import (
    get_camp_overview,
)
from traka_automation.financial_overview.parser.copy_xml_file_to_location import (
    CACHE_LOCATION,
)
from traka_automation.financial_overview.parser.parse_gnucash_xml import (
    parse_gnucash_xml,
)


def prepare_gnucash_xml(filename: str = f"{CACHE_LOCATION}/scratch/database.gnucash"):
    """Prepare a GnuCash XML file for camp overview."""

    accounts, transactions = parse_gnucash_xml(filename)

    transactions_by_account = defaultdict(list)
    for t in transactions:
        transactions_by_account[t["account"]].append(t)

    return accounts, transactions_by_account


def generate_overview(camp_name: str, year=None):
    """Generate the overview for a single camp."""
    if year is None:
        year = datetime.now(tz=UTC).year

    accounts, transactions = prepare_gnucash_xml()
    return get_camp_overview(accounts, camp_name, transactions, year)
