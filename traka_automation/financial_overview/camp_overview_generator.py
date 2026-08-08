import sys
from datetime import UTC, datetime

from traka_automation.financial_overview.overview.generate_overview import (
    generate_overview, prepare_gnucash_xml,
)
from traka_automation.financial_overview.overview.save_camp_overview import (
    save_camp_overview,
)
from traka_automation.financial_overview.parser.copy_xml_file_to_location import (
    copy_gnucash_xml_to_cache_location,
)

CAMPS = [
    "Scoutdoor",
    "Eiffel Experience",
    "Extreem",
    "Jungle Adventure",
    "Scoutakel",
    "Scoutakel - 2",
    "Mission Possible",
    "Geoscouten",
    "BBQ",
]


def main():
    copy_gnucash_xml_to_cache_location()
    accounts, transactions = prepare_gnucash_xml()
    for camp in CAMPS:
        process_camp(camp, accounts, transactions)


def process_camp(camp: str, accounts, transactions, year=None):
    """Process a single camp and save the overview to a file."""
    overview = generate_overview(camp, accounts, transactions, year=year)
    save_camp_overview(
        overview, f"{SAVE_LOCATION}/kampoverzichten/overzicht_{camp}.txt"
    )


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 2:
        SAVE_LOCATION = sys.argv[1]
        CACHE_LOCATION = sys.argv[1]

    main()
