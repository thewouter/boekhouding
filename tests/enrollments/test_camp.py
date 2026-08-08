from traka_automation.enrollments.enrollment.camp import Camp


def test_camp_properties(example_camp: Camp):
    assert example_camp.start_date_string == "12 juli 2027"
    assert example_camp.end_date_string == "19 juli 2027"
    assert example_camp.cancellation_term_one.text_date == "13 mei 2027"
    assert example_camp.cancellation_term_one.text_retainer == "€43.88"
    assert example_camp.cancellation_term_two.text_date == "12 juni 2027"
    assert example_camp.cancellation_term_two.text_retainer == "€87.75"
    assert example_camp.year == 2027
