import shutil

SAVE_LOCATION = "/onedrive/data/exchange_folder"
CACHE_LOCATION = ""


def copy_gnucash_xml_to_cache_location():
    """Copy the GnuCash XML file to cache location"""
    shutil.copy(
        f"{SAVE_LOCATION}/last_boekhouding.gnucash",
        f"{CACHE_LOCATION}/scratch/database.gnucash",
    )
