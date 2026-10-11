import pytest

from traka_automation.enrollments.models import Camp


def test_camp_properties(example_camp: Camp):
    assert example_camp.start_date_string == "12 juli 2027"
    assert example_camp.end_date_string == "19 juli 2027"
    assert example_camp.cancellation_term_one.text_date == "13 mei 2027"
    assert example_camp.cancellation_term_one.text_retainer == "€43.88"
    assert example_camp.cancellation_term_two.text_date == "12 juni 2027"
    assert example_camp.cancellation_term_two.text_retainer == "€87.75"
    assert example_camp.year == 2027


@pytest.mark.parametrize(
    "name",
    ["Mission Impossible", "mission impossible", "Trex Adventure", "trex adventure"],
)
def test_allows_for_two_payment_terms_true(example_camp: Camp, name: str):
    camp = example_camp.model_copy(update={"name": name})
    assert camp.allows_for_two_payment_terms is True


def test_allows_for_two_payment_terms_false(example_camp: Camp):
    camp = example_camp.model_copy(update={"name": "Jungle Adventure"})
    assert camp.allows_for_two_payment_terms is False


def test_payment_term_one_rounds_up_to_nearest_50(example_camp: Camp):
    camp = example_camp.model_copy(update={"price": 175.5})
    assert camp.payment_term_one == 100
    assert camp.payment_term_two == 75.5


def test_payment_term_one_capped_at_price(example_camp: Camp):
    camp = example_camp.model_copy(update={"price": 40})
    assert camp.payment_term_one == 40
    assert camp.payment_term_two == 0


def test_payment_term_one_no_price_raises(example_camp: Camp):
    camp = example_camp.model_copy(update={"price": None})
    with pytest.raises(ValueError):
        _ = camp.payment_term_one


def test_payment_term_two_no_price_raises(example_camp: Camp):
    camp = example_camp.model_copy(update={"price": None})
    with pytest.raises(ValueError):
        _ = camp.payment_term_two
