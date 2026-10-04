from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def base_payload():
    return {
        "lights": 0.0,
        "T1": 19.7, "RH_1": 45.59,
        "T2": 18.89, "RH_2": 44.23,
        "T3": 19.89, "RH_3": 44.9,
        "T4": 19.17, "RH_4": 45.03,
        "T5": 18.0, "RH_5": 49.66,
        "T6": 4.73, "RH_6": 96.47,
        "T7": 17.7, "RH_7": 41.59,
        "T8": 18.53, "RH_8": 49.4,
        "T9": 17.0, "RH_9": 45.73,
        "T_out": 5.48,
        "Press_mm_hg": 742.88,
        "RH_out": 90.17,
        "Windspeed": 5.0,
        "Visibility": 30.83,
        "Tdewpoint": 3.95,
        "rv1": 49.63, "rv2": 49.63,
        "hour": 10, "day_of_week": 1, "month": 1, "is_weekend": 0,
        "Appliances_lag_1": 260.0,
        "Appliances_lag_2": 30.0,
        "Appliances_lag_3": 40.0,
        "Appliances_rolling_mean_3": 110.0,
    }


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_prediction_success():
    response = client.post("/predict", json=base_payload())
    assert response.status_code == 200
    body = response.json()
    assert "predicted_energy_wh" in body
    assert isinstance(body["predicted_energy_wh"], float)


def test_prediction_response_schema():
    response = client.post("/predict", json=base_payload())
    body = response.json()
    assert set(body.keys()) == {
        "predicted_energy_wh",
        "consumption_category",
        "recommendations",
    }
    assert body["consumption_category"] in {"Low", "Moderate", "High"}
    assert isinstance(body["recommendations"], list)


def test_invalid_payload():
    payload = base_payload()
    del payload["T1"]
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
