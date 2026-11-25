from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

from traka_automation.enrollments.payment_connection.generate_paynl_payment_link import (
    _get_reference,
    _paynl_payload,
    generate_paynl_payment_link,
)
from traka_automation.settings import PayNlSettings

END_DATE = datetime(2026, 7, 15, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def settings() -> PayNlSettings:
    return PayNlSettings(service_id="SL-1234-5678", secret="secret")


def test_payload_normalizes_name_in_description_and_reference(
    settings: PayNlSettings,
) -> None:
    payload = _paynl_payload(
        "Zoë Müller-Çelik", "Zomerkamp", 50.0, END_DATE, 1, settings
    )

    assert payload["description"] == "Deelname van Zoe Muller-Celik aan Zomerkamp."
    assert payload["reference"] == "ZomerkampZoeMullerCelik20260715"
    assert str(payload["reference"]).isascii()


def test_payload_keeps_ascii_name_unchanged(settings: PayNlSettings) -> None:
    payload = _paynl_payload("Jan Jansen", "Zomerkamp", 50.0, END_DATE, 1, settings)

    assert payload["description"] == "Deelname van Jan Jansen aan Zomerkamp."


def test_reference_is_alphanumeric_and_truncated() -> None:
    reference = _get_reference("A" * 40, "B" * 40, END_DATE)

    assert reference.isalnum()
    assert len(reference) == 32


def test_generate_payment_link_sends_normalized_name(settings: PayNlSettings) -> None:
    response = MagicMock()
    response.json.return_value = {
        "id": "order-1",
        "links": {"redirect": "https://pay.example/redirect"},
    }
    target = "traka_automation.enrollments.payment_connection.generate_paynl_payment_link.requests.post"
    with patch(target, return_value=response) as post:
        link = generate_paynl_payment_link(
            "José Ñandú", "Zomerkamp", 50.0, END_DATE, settings=settings
        )

    assert post.call_args.kwargs["json"]["description"] == (
        "Deelname van Jose Nandu aan Zomerkamp."
    )
    assert link.payment_link == "https://pay.example/redirect"
    assert link.order_id == "order-1"
