# tests/test_upload_endpoints.py
from io import BytesIO


def test_upload_departments_valid_csv(client):
    csv = b"id,department\n1,Engineering\n2,Finance\n"
    files = {"file": ("departments.csv", BytesIO(csv), "text/csv")}
    r = client.post("/upload/departments", files=files)
    assert r.status_code == 200
    body = r.json()
    assert body["inserted"] >= 0  # depende de tu lógica
    assert "skipped" in body


def test_upload_jobs_invalid_csv(client):
    # Falta encabezado 'job'
    bad = b"id,title\n1,Data Engineer\n"
    files = {"file": ("jobs.csv", BytesIO(bad), "text/csv")}
    r = client.post("/upload/jobs", files=files)
    assert r.status_code in (400, 422)


def test_upload_idempotent(client):
    csv = b"id,department\n1,Engineering\n"
    files = {"file": ("departments.csv", BytesIO(csv), "text/csv")}
    client.post("/upload/departments", files=files)
    r = client.post("/upload/departments", files=files)
    assert r.status_code == 200
    # segundo intento debería marcar skipped=1 si tienes esa lógica
    assert r.json()["skipped"] >= 1
