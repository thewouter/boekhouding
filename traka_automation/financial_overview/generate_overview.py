import shutil
from collections import defaultdict
from datetime import datetime, UTC

from traka_automation.financial_overview.parse_gnucash_xml import parse_gnucash_xml

SAVE_LOCATION = "/onedrive/data/exchange_folder"
CACHE_LOCATION = ""


def copy_gnucash_xml_to_cache_location():
    shutil.copy(
        f"{SAVE_LOCATION}/last_boekhouding.gnucash",
        f"{CACHE_LOCATION}/scratch/database.gnucash",
    )


def generate_overview(camp_name: str, year=None):
    """Generate the overview for a single camp."""
    if year is None:
        year = datetime.now(tz=UTC).year

    posten: dict = {}

    copy_gnucash_xml_to_cache_location()

    accounts, transactions = parse_gnucash_xml(
        f"{CACHE_LOCATION}/scratch/database.gnucash"
    )

    transactions_by_account = defaultdict(list)
    for t in transactions:
        transactions_by_account[t["account"]].append(t)

    for type in ["EXPENSE", "INCOME"]:
        handle_expense_income(
            type, accounts, camp_name, posten, transactions_by_account, year
        )

    return posten


def handle_expense_income(
    type: str, accounts, camp_name, posten, transactions_by_account, year
):
    print(f"--{type}--")

    # find camp account
    camp_uuid = next(
        guid
        for guid, acc in accounts.items()
        if acc["name"] == camp_name and acc["type"] == type
    )

    # find children
    child_posts = [
        (guid, acc["name"])
        for guid, acc in accounts.items()
        if acc["parent"] == camp_uuid
    ]

    for child_guid, child_name in child_posts:
        if child_name not in posten:
            posten[child_name] = []

        print(f"<{child_name}>:")

        for entry in transactions_by_account[child_guid]:
            add_entry_to_posten(posten, entry, child_name, year)


def add_entry_to_posten(posten, entry, child_name, year):
    if entry["year"] == str(year):
        amount = -entry["amount"]  # keep your sign convention
        label = f"{entry['memo']} ({entry['description']})"

        print(f"{label} : {amount}")
        posten[child_name].append((label, amount))
