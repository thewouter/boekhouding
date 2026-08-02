from typing import Any


def get_camp_overview(
    accounts: dict[str, dict[str, Any]],
    camp_name: str,
    transactions: dict[str, list[dict[str, Any]]],
    year: int,
) -> dict[str, list[Any]]:
    overview: dict = {}

    for account_type in ["EXPENSE", "INCOME"]:
        print(f"--{account_type}--")

        # find camp account
        camp_uuid = find_camp_account(camp_name, account_type, accounts)

        # find children
        child_posts = find_children_of_camp_account(camp_uuid, accounts)

        # loop over children and add children to overview
        for child_guid, child_name in child_posts:
            entries_in_children = transactions[child_guid]
            add_child_to_overview(overview, child_name, entries_in_children, year)
    return overview


def find_camp_account(camp_name, account_type, accounts):
    """Find the uuid of the camp account with the given name"""
    return next(
        guid
        for guid, acc in accounts.items()
        if acc["name"] == camp_name and acc["type"] == account_type
    )


def find_children_of_camp_account(camp_uuid, accounts):
    """find all children of the camp account with the given uuid"""
    return [
        (guid, acc["name"])
        for guid, acc in accounts.items()
        if acc["parent"] == camp_uuid
    ]


def add_child_to_overview(overview, child_name, entries_in_child, year):
    if child_name not in overview:
        overview[child_name] = []

        print(f"<{child_name}>:")

        for entry in entries_in_child:
            add_entry_to_overview(overview, entry, child_name, year)


def add_entry_to_overview(overview, entry, child_name, year):
    if entry["year"] == str(year):
        amount = -entry["amount"]  # keep your sign convention
        label = f"{entry['memo']} ({entry['description']})"

        print(f"{label} : {amount}")
        overview[child_name].append((label, amount))
