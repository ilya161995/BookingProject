import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com/"


@pytest.fixture(scope="function")
def create_booking():
    """Фикстура для создания бронирования"""
    payload = {
        "firstname": "ilya",
        "lastname": "Brown",
        "totalprice": 1000,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-01-23",
            "checkout": "2026-02-15"
        },
        "additionalneeds": "Breakfast"
    }
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    assert response.status_code == 200
    return response.json()