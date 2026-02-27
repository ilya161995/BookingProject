import allure
import pytest
import requests

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
