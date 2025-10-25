# tests/conftest.py
import os, tempfile, pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app import models
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="function")
def db_session(tmp_path):
    
    db_file = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_file}",
        connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def seed_minimal(db_session):
    
    db_session.query(models.HiredEmployee).delete()
    db_session.query(models.Job).delete()
    db_session.query(models.Department).delete()
    db_session.commit()

    db_session.add_all([
        models.Department(id=1, department="Engineering"),
        models.Department(id=2, department="Finance"),
        models.Job(id=1, job="Data Engineer"),
        models.Job(id=2, job="Analyst"),
    ])
    db_session.commit()
