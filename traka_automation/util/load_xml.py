import gzip
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element


def load_xml(path) -> Element[str]:
    """Load and XML file."""
    with open(path, "rb") as f:
        magic = f.read(2)

    if magic == b"\x1f\x8b":
        with gzip.open(path, "rb") as f:
            tree = ET.parse(f)
            root = tree.getroot()
    else:
        with open(path, "rb") as f:
            tree = ET.parse(f)
            root = tree.getroot()
    return root
