import csv
import shutil
import sqlite3
from datetime import datetime


def generate_overview(camp_name: str, year=None):
    if year is None:
        year = datetime.now().year
    result = ""
    posten = {}
    shutil.copy("/onedrive/data/exchange_folder/last_boekhouding.gnucash", "/scratch/database.sqlite")
    db = sqlite3.connect("/scratch/database.sqlite")
    for type in ["EXPENSE", "INCOME"]:
        print(f"--{type}--")
        camp_uuid = db.execute(f'SELECT guid FROM accounts WHERE name="{camp_name}" AND account_type="{type}" LIMIT 1').fetchone()[0]
        child_posts = db.execute(f'SELECT guid, name FROM accounts WHERE parent_guid="{camp_uuid}"').fetchall()
        for child in child_posts:
            if child[1] not in posten.keys():
                posten[child[1]] = []

            print(f"<{child[1]}>: ")
            entries = db.execute(
                f'SELECT splits.guid, splits.value_num, splits.value_denom, splits.memo, transactions.description, '
                f'strftime("%Y", transactions.post_date) FROM splits '
                f'LEFT JOIN transactions ON splits.tx_guid=transactions.guid '
                f'WHERE account_guid="{child[0]}" AND strftime("%Y", transactions.post_date) == "{year}"').fetchall()
            for entry in entries:
                print(f"{entry[3]} ({entry[4]}) : {-entry[1] / entry[2]}")
                posten[child[1]].append((f"{entry[3]} ({entry[4]})", -entry[1] / entry[2]))
    with open(f"{camp_name}_{year}.csv", "w") as f:
        writer = csv.writer(f, delimiter=";")
        for post, values in posten.items():
            writer.writerow([post, "", ""])
            for value in values:
                writer.writerow(["",value[0], value[1]])

    return posten

if __name__ == '__main__':
    kampen = ["Scoutdoor", "Eiffel Experience", "Extreem", "Jungle Adventure", "Scoutakel", "Scoutakel - 2", "Mission Possible", "Geoscouten", "BBQ"]
    for kamp in kampen:
        overview = generate_overview(kamp, 2025)
        with open(f"/onedrive/data/exchange_folder/kampoverzichten/overzicht_{kamp}.txt", "w") as f:
            for post, items in overview.items():
                f.write(f"{post}:\n")
                for description, amount in items:
                    f.write(f"    {description}: {'' if amount >= 0 else '-'}€{abs(amount):0.2f}\n")
