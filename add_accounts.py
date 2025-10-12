import sqlite3
import uuid

kampen = ["Scoutdoor", "Eiffel Experience", "Extreem", "Jungle Adventure", "Scoutakel", "Scoutakel - 2", "Mission Possible", "Geoscouten"]
subposten = ["Voorbereidingen", "Vervoerskosten", "Gebouwen en terreinen", "Programmakosten", "Voeding", "Organisatiekosten"]

db = sqlite3.connect("Traka_boekhouding_2025_TESTER.sqlite")
commodity_guid = db.execute('SELECT guid FROM commodities WHERE mnemonic="EUR" LIMIT 1').fetchone()[0]
root_account_guid = db.execute(f'SELECT guid FROM accounts WHERE parent_guid IS NULL LIMIT 1').fetchone()[0]
expense_root_guid = db.execute(f'SELECT guid FROM accounts WHERE parent_guid = "{root_account_guid}" AND account_type="EXPENSE" LIMIT 1').fetchone()[0]
kampen_root_guid = db.execute(f'SELECT guid FROM accounts WHERE parent_guid = "{expense_root_guid}" AND name="Kampen" LIMIT 1').fetchone()[0]
print(commodity_guid)
print(root_account_guid)
print(expense_root_guid)
print(kampen_root_guid)

for kamp in kampen:
    kamp_uuid = uuid.uuid4().hex
    db.execute(f'INSERT INTO accounts (guid, name, account_type, commodity_guid, parent_guid, commodity_scu, non_std_scu) VALUES ("{kamp_uuid}", "{kamp}", "EXPENSE", "{commodity_guid}", "{kampen_root_guid}", 100, 0)')
    db.commit()
    for subpost in subposten:
        subpost_uuid = uuid.uuid4().hex
        db.execute(f'INSERT INTO accounts (guid, name, account_type, commodity_guid, parent_guid, '
                   f'commodity_scu, non_std_scu) VALUES ("{subpost_uuid}", "{subpost}", '
                   f'"EXPENSE", "{commodity_guid}", "{kamp_uuid}", 100, 0)')
        db.commit()

db.close()