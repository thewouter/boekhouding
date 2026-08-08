from traka_automation.enrollments.enrollment.enrollment_web_form import (
    EnrollmentWebForm,
)


def test_enrollment_from_json(example_enrollment_json):
    enrollment = EnrollmentWebForm.from_json(example_enrollment_json, uuid="test-uuid")
    assert isinstance(enrollment, EnrollmentWebForm)

    assert len(enrollment.participants) == 2


def test_enrollment_web_form_properties(example_enrollment_web_form: EnrollmentWebForm):
    assert example_enrollment_web_form.total_price == 175.5 + 175.5
    assert example_enrollment_web_form.combined_names == "Jan Jansen en Piet Jansen"
    assert example_enrollment_web_form.payment_link.payment_link == "https://google.com"
    assert (
        example_enrollment_web_form.json_representation
        == '{"camp":{"name":"Jungle Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"participants":[{"camp":{"name":"Jungle Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"name":"Jan Jansen","zip_code":"1234 AB","address":"Voorbeeldstraat 1","city":"Voorbeeldstad","birth_date":"2016-03-15","email_address":"wouter@woutervanharten.nl","phone":"06-12345678","dietary_restrictions":"Ik mag geen rijst op woensdagen","photo":"fotodieiknetgenomenheb.jpg","backup_name":"Papa of Mama","backup_email_address":"backup1@test.nl","backup_phone":"06-12345688","member_number":"SN-98765","scouting_group":"Scouting Orion","scouting_city":"Delft","age_group":"Welpen"},{"camp":{"name":"Jungle Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"name":"Piet Jansen","zip_code":"1234 AC","address":"Voorbeeldstraat 3","city":"Voorbeeldstad","birth_date":"1940-03-15","email_address":"wouter.van.harten@trapperskamp.com","phone":"06-12345678","dietary_restrictions":"Ik mag geen rijst op dinsdagen","photo":"fotodieiknetgenomenheb.jpg","backup_name":"Mijn echtgenoot of echtgenote","backup_email_address":"backup1@test.nl","backup_phone":"06-12345688","member_number":"SN-98765","scouting_group":"Scouting Orion","scouting_city":"Delft","age_group":"Welpen"}],"uuid":"test-uuid","payment_link_cache":{}}'
    )
    assert example_enrollment_web_form.email_addresses == [
        "wouter@woutervanharten.nl",
        "wouter.van.harten@trapperskamp.com",
    ]


def test_enrollment_web_form_dynamic_link_generation(
    example_enrollment_web_form: EnrollmentWebForm,
):
    assert example_enrollment_web_form.payment_link_cache is None
    assert example_enrollment_web_form.payment_link.payment_link == "https://google.com"
    assert example_enrollment_web_form.payment_link_cache is not None


def test_enrollment_web_form_to_json(example_enrollment_web_form: EnrollmentWebForm):
    json_representation = example_enrollment_web_form.json_representation
    assert isinstance(json_representation, str)
    assert (
        json_representation
        == '{"camp":{"name":"Jungle Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"participants":[{"camp":{"name":"Jungle Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"name":"Jan Jansen","zip_code":"1234 AB","address":"Voorbeeldstraat 1","city":"Voorbeeldstad","birth_date":"2016-03-15","email_address":"wouter@woutervanharten.nl","phone":"06-12345678","dietary_restrictions":"Ik mag geen rijst op woensdagen","photo":"fotodieiknetgenomenheb.jpg","backup_name":"Papa of Mama","backup_email_address":"backup1@test.nl","backup_phone":"06-12345688","member_number":"SN-98765","scouting_group":"Scouting Orion","scouting_city":"Delft","age_group":"Welpen"},{"camp":{"name":"Jungle Adventure","price":175.5,"start_date":"2027-07-12T00:00:00","end_date":"2027-07-19T00:00:00"},"name":"Piet Jansen","zip_code":"1234 AC","address":"Voorbeeldstraat 3","city":"Voorbeeldstad","birth_date":"1940-03-15","email_address":"wouter.van.harten@trapperskamp.com","phone":"06-12345678","dietary_restrictions":"Ik mag geen rijst op dinsdagen","photo":"fotodieiknetgenomenheb.jpg","backup_name":"Mijn echtgenoot of echtgenote","backup_email_address":"backup1@test.nl","backup_phone":"06-12345688","member_number":"SN-98765","scouting_group":"Scouting Orion","scouting_city":"Delft","age_group":"Welpen"}],"uuid":"test-uuid","payment_link_cache":null}'
    )
