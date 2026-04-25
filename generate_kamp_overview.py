import csv
import shutil
import sys
import gzip
from datetime import datetime
import xml.etree.ElementTree as ET

SAVE_LOCATION = '/onedrive/data/exchange_folder'


def strip_ns(elem):
    """Remove XML namespaces in-place."""
    for el in elem.iter():
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]

def parse_gnucash_xml(path):
    # --- handle gzip transparently ---
    with open(path, "rb") as f:
        magic = f.read(2)

    if magic == b"\x1f\x8b":
        f = gzip.open(path, "rb")
    else:
        f = open(path, "rb")

    tree = ET.parse(f)
    root = tree.getroot()
    f.close()

    # --- strip namespaces ---
    strip_ns(root)

    accounts = {}
    transactions = []

    # --- parse accounts ---
    for acc in root.findall(".//account"):
        id_elem = acc.find("id")
        name_elem = acc.find("name")
        type_elem = acc.find("type")

        # skip incomplete/invalid accounts
        if id_elem is None or name_elem is None or type_elem is None:
            continue

        guid = id_elem.text
        name = name_elem.text
        acc_type = type_elem.text

        parent_elem = acc.find("parent")
        parent = parent_elem.text if parent_elem is not None else None

        accounts[guid] = {
            "name": name,
            "type": acc_type,
            "parent": parent,
        }

    # --- parse transactions + splits ---
    for trn in root.findall(".//transaction"):
        description_elem = trn.find("description")
        description = description_elem.text if description_elem is not None else ""

        date_elem = trn.find("date-posted/date")
        year = date_elem.text[:4] if date_elem is not None else None

        if len(trn.findall("splits/split")) > 15:
            continue

        for sp in trn.findall("splits/split"):
            acc_elem = sp.find("account")
            value_elem = sp.find("value")

            if acc_elem is None or value_elem is None:
                continue

            acc_guid = acc_elem.text
            value = value_elem.text

            num, denom = map(int, value.split("/"))

            memo_elem = sp.find("memo")
            memo = memo_elem.text if memo_elem is not None else ""


            transactions.append({
                "account": acc_guid,
                "amount": num / denom,
                "memo": memo,
                "description": description,
                "year": year,
            })

    return accounts, transactions


def generate_overview(camp_name: str, year=None):
    if year is None:
        year = datetime.now().year

    posten = {}

    # copy file (same as before)
    shutil.copy(
        f"{SAVE_LOCATION}/last_boekhouding.gnucash",
        f"{SAVE_LOCATION}/scratch/database.gnucash"
    )

    accounts, transactions = parse_gnucash_xml(
        f"{SAVE_LOCATION}/scratch/database.gnucash"
    )

    # --- optional speedup: index by account ---
    from collections import defaultdict
    transactions_by_account = defaultdict(list)
    for t in transactions:
        transactions_by_account[t["account"]].append(t)

    for type in ["EXPENSE", "INCOME"]:
        print(f"--{type}--")

        # find camp account
        camp_uuid = next(
            guid for guid, acc in accounts.items()
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
                if entry["year"] == str(year):
                    amount = -entry["amount"]  # keep your sign convention
                    label = f"{entry['memo']} ({entry['description']})"

                    print(f"{label} : {amount}")
                    posten[child_name].append((label, amount))

    # --- write CSV ---
    with open(f"{camp_name}_{year}.csv", "w") as f:
        writer = csv.writer(f, delimiter=";")
        for post, values in posten.items():
            writer.writerow([post, "", ""])
            for value in values:
                writer.writerow(["", value[0], value[1]])

    return posten


if __name__ == '__main__':
    print(sys.argv)

    if len(sys.argv) == 2:
        SAVE_LOCATION = sys.argv[1]

    kampen = [
        "Scoutdoor", "Eiffel Experience", "Extreem", "Jungle Adventure",
        "Scoutakel", "Scoutakel - 2", "Mission Possible", "Geoscouten", "BBQ"
    ]

    for kamp in kampen:
        overview = generate_overview(kamp, datetime.now().year)

        with open(f"{SAVE_LOCATION}/kampoverzichten/overzicht_{kamp}.txt", "w") as f:
            for post, items in overview.items():
                f.write(f"{post}:\n")
                for description, amount in items:
                    f.write(f"    {description}: {'' if amount >= 0 else '-'}€{abs(amount):0.2f}\n")