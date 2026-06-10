from datetime import date, timedelta

expected_month = date.today().replace(day=1).isoformat()

def test_revenue_report(client, create_reservation):
    response = client.post("/reports/revenue", json={
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=7)).isoformat()
    })

    assert response.status_code == 200
    assert response.json()["revenue"] is not None

def test_revenue_invalid_end_date(client, create_reservation):
    response = client.post("/reports/revenue", json={
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=-7)).isoformat()
    })

    assert response.status_code == 409
    assert response.json()["detail"] == "End date must be after start date."

def test_revenue_empty_payload(client, create_reservation):
    response = client.post("/reports/revenue", json={
        "end_date": (date.today() + timedelta(days=-7)).isoformat()
    })

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_revenue_report_monthly(client, create_reservation):
    response = client.get("/reports/revenue/monthly")

    assert response.status_code == 200
    assert response.json()[0]["month"] == expected_month
    assert response.json()[0]["revenue"] is not None

def test_occupancy_report_today(client, create_reservation):
    response = client.get("/reports/occupancy/today")
    assert response.status_code == 200
    assert response.json()["total_rooms"] == 1
    assert response.json()["occupied_rooms"] == 1
    assert response.json()["occupancy_percentage"] == 100.0

def test_occupancy_report_monthly(client, create_reservation):
    response = client.post("/reports/occupancy/monthly", json={
        "month_start": date.today().isoformat(),
        "month_end": (date.today() + timedelta(days=30)).isoformat()
    })

    assert response.status_code == 200
    assert response.json()["available_room_nights"] == 30
    assert response.json()["occupied_room_nights"] == 7
    assert response.json()["occupancy_percentage"] == 23.33

def test_occupancy_invalid_end_date(client, create_reservation):
    response = client.post("/reports/occupancy/monthly", json={
        "month_start": date.today().isoformat(),
        "month_end": (date.today() + timedelta(days=-7)).isoformat()
    })

    assert response.status_code == 409
    assert response.json()["detail"] == "End date must be after start date."

def test_occupancy_empty_payload(client, create_reservation):
    response = client.post("/reports/occupancy/monthly", json={
        "month_end": (date.today() + timedelta(days=-7)).isoformat()
    })

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"