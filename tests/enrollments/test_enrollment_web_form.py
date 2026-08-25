from mollie.api.objects.payment_link import PaymentLink

from traka_automation.enrollments.models.enrollment_web_form import (
    EnrollmentWebForm,
)


def test_enrollment_from_json(example_enrollment_json):
    enrollment = EnrollmentWebForm.from_json(example_enrollment_json, uuid="test-uuid")
    assert isinstance(enrollment, EnrollmentWebForm)

    assert len(enrollment.participants) == 2


def test_enrollment_web_form_properties(example_enrollment_web_form: EnrollmentWebForm):
    assert example_enrollment_web_form.total_price == 175.5 + 175.5
    assert example_enrollment_web_form.combined_names == "Jan Jansen en Piet Jansen"
    assert isinstance(example_enrollment_web_form.payment_link, PaymentLink)
    assert example_enrollment_web_form.payment_link.payment_link == "https://google.com"  # type: ignore
    assert (
        example_enrollment_web_form.json_representation.startswith('{"camp":{"name":"Jungle '
        'Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"participants":[{"camp":{"name":"Jungle '
        'Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"name":"Jan '
        'Jansen","zip_code":"1234 AB","address":"Voorbeeldstraat '
        '1","city":"Voorbeeldstad","birth_date":"2016-03-15","email_address":"wouter@woutervanharten.nl","phone":"06-12345678","dietary_restrictions":"Ik '
        "mag geen rijst op "))
    assert example_enrollment_web_form.email_addresses == [
        "wouter@woutervanharten.nl",
        "wouter.van.harten@trapperskamp.com",
    ]


def test_enrollment_web_form_dynamic_link_generation(
    example_enrollment_web_form: EnrollmentWebForm,
):
    assert example_enrollment_web_form.payment_link_cache is None
    assert example_enrollment_web_form.payment_link.payment_link == "https://google.com"  # type: ignore
    assert example_enrollment_web_form.payment_link_cache is not None


def test_enrollment_web_form_to_json(example_enrollment_web_form: EnrollmentWebForm):
    json_representation = example_enrollment_web_form.json_representation
    assert isinstance(json_representation, str)
    assert (
        json_representation.startswith('{"camp":{"name":"Jungle '
 'Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"participants":[{"camp":{"name":"Jungle '
 'Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"name":"Jan '
 'Jansen","zip_code":"1234 AB","address":"Voorbeeldstraat '
 '1","city":"Voorbeeldstad","birth_date":"2016-03-15","email_address":"wouter@woutervanharten.nl","phone":"06-12345678","dietary_restrictions":"Ik '
 'mag geen rijst op '
 'woensdagen","photo":"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAACXBIWXMAAAsSAAALEgHS3X78AAAARElEQVQIHWM8zRn3/wb7U4aoDzYMTAyMDIwHuMP/7+K5zPCb6Q/DP4b/DCx6P+QY7rO9Ykh4bw8WYPzP0PAfJANSDgIAgkYYUh06X6cAAAAASUVORK5CYII==","backup_name":"Papa '
                                       ))
