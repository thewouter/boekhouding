import sys
from datetime import UTC, datetime

from traka_automation.financial_overview.generate_overview import generate_overview
from traka_automation.financial_overview.save_camp_overview import save_camp_overview

from generate_overview import CACHE_LOCATION, SAVE_LOCATION

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


def process_camp(camp: str):
    overview = generate_overview(camp, datetime.now(UTC).year)
    save_camp_overview(
        overview, f"{SAVE_LOCATION}/kampoverzichten/overzicht_{camp}.txt"
    )


def main():
    for camp in CAMPS:
        process_camp(camp)


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 2:
        SAVE_LOCATION = sys.argv[1]
        CACHE_LOCATION = sys.argv[1]

    main()
