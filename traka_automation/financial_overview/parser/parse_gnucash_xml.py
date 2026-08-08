from typing import Any
from xml.etree.ElementTree import Element

from traka_automation.util.load_xml import load_xml


def strip_ns(elem: Element[Any]) -> None:
    """Remove XML namespaces in-place."""
    for el in elem.iter():
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]


def parse_accounts(root: Element[str]) -> dict[Any, Any]:
    """parse the root tree into a dictionary of accounts."""

    accounts = {}
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
    return accounts


def parse_transactions(root: Element[str]) -> list[Any]:
    """Convert the root tree into a list of transactions"""
    transactions = []
    for trn in root.findall(".//transaction"):
        description_elem = trn.find("description")
        description = description_elem.text if description_elem is not None else ""

        date_elem = trn.find("date-posted/date")
        year = date_elem.text[:4] if date_elem is not None else None  # type: ignore[index]

        if len(trn.findall("splits/split")) > 15:
            continue

        for sp in trn.findall("splits/split"):
            acc_elem = sp.find("account")
            value_elem = sp.find("value")

            if acc_elem is None or value_elem is None:
                continue

            acc_guid = acc_elem.text
            value = value_elem.text

            num, denom = map(int, value.split("/"))  # type: ignore[union-attr]

            memo_elem = sp.find("memo")
            memo = memo_elem.text if memo_elem is not None else ""

            transactions.append(
                {
                    "account": acc_guid,
                    "amount": num / denom,
                    "memo": memo,
                    "description": description,
                    "year": year,
                }
            )
    return transactions


def parse_gnucash_xml(path) -> tuple[dict[Any, Any], list[Any]]:
    """Parse the Gnucash XML into accounts and transactions"""
    root = load_xml(path)
    strip_ns(root)
    accounts = parse_accounts(root)
    transactions = parse_transactions(root)
    return accounts, transactions
