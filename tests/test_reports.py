from app import models


def seed_hires(db_session):
    rows = [
        models.HiredEmployee(
            id=1, name="A", datetime="2021-01-15T10:00:00", department_id=1, job_id=1
        ),
        models.HiredEmployee(
            id=2, name="B", datetime="2021-03-20T10:00:00", department_id=1, job_id=1
        ),
        models.HiredEmployee(
            id=3, name="C", datetime="2021-10-01T10:00:00", department_id=1, job_id=1
        ),
        models.HiredEmployee(
            id=4, name="D", datetime="2021-12-31T10:00:00", department_id=1, job_id=1
        ),
        models.HiredEmployee(
            id=5, name="E", datetime="2021-05-10T10:00:00", department_id=2, job_id=2
        ),
    ]
    db_session.bulk_save_objects(rows)
    db_session.commit()


def test_hired_by_quarter(client, db_session, seed_minimal):
    seed_hires(db_session)
    r = client.get("/reports/hired-by-quarter-2021")
    assert r.status_code == 200
    data = r.json()
    row = next(
        x
        for x in data
        if x["department"] == "Engineering" and x["job"] == "Data Engineer"
    )
    assert row["Q1"] == 2
    assert row["Q2"] == 0
    assert row["Q3"] == 0
    assert row["Q4"] == 2


def test_departments_above_mean(client, db_session, seed_minimal):
    seed_hires(db_session)
    r = client.get("/reports/departments-above-mean-2021")
    assert r.status_code == 200
    names = {x["department"] for x in r.json()}
    assert "Engineering" in names
    assert "Finance" not in names
