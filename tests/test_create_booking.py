import allure
import pytest
import requests
from pydantic import ValidationError
from core.models.booking import BookingResponse
from requests.exceptions import HTTPError



@allure.feature('Test create booking')
@allure.story('Test creating new booking')
def test_create_booking(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    response_data = api_client.create_booking(booking_data)
    with allure.step('Verifying created booking data'):
        created_booking = response_data["booking"]
        assert created_booking["firstname"] == booking_data["firstname"]
        assert created_booking["lastname"] == booking_data["lastname"]
        assert created_booking["totalprice"] == booking_data["totalprice"]
        assert created_booking["depositpaid"] == booking_data["depositpaid"]
        assert created_booking["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
        assert created_booking["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with random dates')
def test_create_booking_with_random_dates(api_client, booking_dates):
    booking_data = {
        "firstname": "Ilya",
        "lastname": "Ivanovich",
        "totalprice": 1500,
        "depositpaid": True,
        "bookingdates": booking_dates,
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with empty strings')
def test_create_booking_empty_strings(api_client):
    booking_data = {
        "lastname": "",
        "totalprice": 1500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }
    with pytest.raises(HTTPError):
        api_client.create_booking(booking_data)


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with invalid firstname type')
def test_create_booking_invalid_firstname_type(api_client):
    booking_data = {
        "firstname": 123,
        "lastname": "Ivanovich",
        "totalprice": 1500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }
    with pytest.raises(HTTPError):
        api_client.create_booking(booking_data)


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with invalid date format')
def test_create_booking_invalid_date_format(api_client):
    booking_data = {
        "lastname": "Ivanovich",
        "totalprice": 1500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "1-2025-25",
            "checkout": "2025.02.10"
        },
        "additionalneeds": "Dinner"
    }
    with pytest.raises(HTTPError):
        api_client.create_booking(booking_data)