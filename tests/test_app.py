# tests/test_stock_api.py

import requests

BASE_URL = "http://localhost:5000"  # Replace with your API's URL


def test_get_stock():
    # Replace endpoint as needed
    response = requests.get(f"{BASE_URL}/stockkkk/AAPL")
    assert response.status_code == 200  # Check if the response is OK
    data = response.json()
    print(data)
    assert "symbol" in data
    assert data["symbol"] == "AAPL"
