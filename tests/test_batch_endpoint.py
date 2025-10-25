# tests/test_batch_endpoint.py
def test_batch_min_max_bounds(client, seed_minimal):
    ok1 = [{"id": 10, "name": "A", "datetime": "2021-01-01T10:00:00", "department_id": 1, "job_id": 1}]
    r = client.post("/employees/batch", json=ok1)
    assert r.status_code == 200
    assert r.json()["inserted"] == 1

    ok1000 = [
        {"id": i, "name": f"N{i}", "datetime": "2021-02-01T10:00:00", "department_id": 1, "job_id": 1}
        for i in range(1000, 2000)
    ]
    r = client.post("/employees/batch", json=ok1000)
    assert r.status_code == 200
    assert r.json()["inserted"] == 1000

def test_batch_zero_fails(client):
    r = client.post("/employees/batch", json=[])
    assert r.status_code == 400

def test_batch_over_limit_fails(client, seed_minimal):
    too_many = [
        {"id": i, "name": f"N{i}", "datetime": "2021-03-01T10:00:00", "department_id": 1, "job_id": 1}
        for i in range(1, 1002)
    ]
    r = client.post("/employees/batch", json=too_many)
    assert r.status_code == 400

def test_batch_rollback_on_duplicate(client, seed_minimal):
    payload = [
        {"id": 5001, "name": "A", "datetime": "2021-04-01T10:00:00", "department_id": 1, "job_id": 1},
        {"id": 5001, "name": "B", "datetime": "2021-05-01T10:00:00", "department_id": 1, "job_id": 1},
    ]
    r = client.post("/employees/batch", json=payload)
    assert r.status_code in (400, 409)
