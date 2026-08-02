import shutil
from collections import defaultdict
from datetime import UTC, datetime

from traka_automation.financial_overview.overview.get_camp_overview import (
    get_camp_overview,
)
from traka_automation.financial_overview.parser.parse_gnucash_xml import (
    parse_gnucash_xml,
)

SAVE_LOCATION = "/onedrive/data/exchange_folder"
CACHE_LOCATION = ""


def generate_overview(camp_name: str, year=None):
    """Generate the overview for a single camp."""
    if year is None:
        year = datetime.now(tz=UTC).year

    accounts, transactions = prepare_gnucash_xml()
    return get_camp_overview(accounts, camp_name, transactions, year)


def copy_gnucash_xml_to_cache_location():
    """Copy the GnuCash XML file to cache location"""
    shutil.copy(
        f"{SAVE_LOCATION}/last_boekhouding.gnucash",
        f"{CACHE_LOCATION}/scratch/database.gnucash",
    )


def prepare_gnucash_xml():
    """Prepare a GnuCash XML file for camp overview."""
    copy_gnucash_xml_to_cache_location()

    accounts, transactions = parse_gnucash_xml(
        f"{CACHE_LOCATION}/scratch/database.gnucash"
    )

    transactions_by_account = defaultdict(list)
    for t in transactions:
        transactions_by_account[t["account"]].append(t)

    return accounts, transactions_by_account
