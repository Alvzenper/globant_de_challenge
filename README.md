# 📘 Globant DE Challenge — Data Engineering API

This project implements a modular **ETL API built with FastAPI**, allowing the ingestion, validation, and reporting of data from CSV and JSON files.
The data is processed, cleaned, and stored in an SQL database (SQLite locally, extendable to PostgreSQL or Azure SQL).
The project concludes with its **deployment on Azure** using **Docker**, **Azure Container Registry (ACR)**, and **Azure Container Instance (ACI)**.

Its design reflects a focus on **data quality, modularity, and automated deployment**, aligned with modern data engineering best practices.

---

## 🧰 Tech Stack
| Area             | Tools                                                   |
| ---------------- | ------------------------------------------------------- |
| Language         | Python 🐍                                               |
| API Framework    | FastAPI ⚡                                               |
| Database         | SQLite (demo) → extendable to PostgreSQL / Azure SQL    |
| Core Libraries   | `pandas`, `sqlalchemy`, `pydantic`, `pytest`, `uvicorn` |
| Containers       | Docker 🐳                                               |
| Cloud Deployment | Azure ACR + Azure Container Instance                    |
| Testing          | Pytest with ephemeral database and dependency injection |

---

## 🧱 Repository Structure

| Folder / File          | Purpose                                                                         |
| ---------------------- | ------------------------------------------------------------------------------- |
| **`app/`**             | Core API logic and routers                                                      |
| **`app/routers/`**     | Endpoints organized by functionality (`upload`, `reports`, `employee`, `batch`) |
| **`app/models.py`**    | SQLAlchemy ORM models (Departments, Jobs, HiredEmployees)                       |
| **`app/schemas.py`**   | Data validation and parsing with Pydantic                                       |
| **`app/database.py`**  | Database connection, session, and configuration                                 |
| **`tests/`**           | Automated endpoint and data consistency tests                                   |
| **`Dockerfile`**       | Reproducible image for deployment                                               |
| **`requirements.txt`** | Project dependencies                                                            |
| **`README.md`**        | Documentation and execution guide                                               |

---

## 🧩 Main Endpoints

| Endpoint                               | Method | Description                                                        |
| -------------------------------------- | ------ | ------------------------------------------------------------------ |
| `/upload/departments`                  | POST   | Bulk upload of departments from CSV                                |
| `/upload/jobs`                         | POST   | Bulk upload of job positions from CSV                              |
| `/upload/hired_employees`              | POST   | Bulk upload of employees with foreign key validation               |
| `/employees/batch`                     | POST   | Batch insertion of up to 1000 JSON records in a single transaction |
| `/reports/hired-by-quarter-2021`       | GET    | Report of employees hired by quarter and department                |
| `/reports/departments-above-mean-2021` | GET    | Report of departments with hiring above the annual average         |

---

## 🧠 Design Highlights

- Robust data validation using Pydantic and schema matching.

- Transaction-safe inserts with rollback on error.

- Batch processing endpoint supporting large JSON payloads.

- Automated testing with ephemeral SQLite databases.

- Dockerized deployment for portability and scalability.

- Cloud integration with Azure Container Registry and Instance.

- Modular architecture separating logic, data, and configuration layers.

---

## ⚙️ Process Flow


          ┌───────────────────────────────┐
          │   CSV / JSON Input (Upload)   │
          └────────────┬──────────────────┘
                       │
                       ▼
             ┌─────────────────────┐
             │ Pydantic Validation │
             └────────────┬────────┘
                          │
                          ▼
             ┌─────────────────────┐
             │ ORM SQLAlchemy DB   │
             └────────────┬────────┘
                          │
                          ▼
             ┌─────────────────────┐
             │   API Reports       │
             └────────────┬────────┘
                          │
                          ▼
             ┌───────────────────────────────┐
             │ Docker + Azure ACR + ACI      │
             └───────────────────────────────┘

---
 ## ☁️ Cloud Deployment (Azure)

```bash
# 1. Build the container
docker build -t globant-de-api .

# 2. Login to Azure
az login
az acr login --name <acr>

# 3. Push to ACR
docker tag globant-de-api <acr>.azurecr.io/globant-de-api:v1
docker push <acr>.azurecr.io/globant-de-api:v1

# 4. Create Azure Container Instance
az container create \
  --resource-group <resource-group> \
  --name globant-de-api \
  --image <acr>.azurecr.io/globant-de-api:v1 \
  --registry-login-server <acr>.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --ports 80

# 5. Access the API
# Endpoint: http://4.248.19.55:8000/docs#
# FastAPI Swagger UI automatically available for testing.


---

## 🧪 Testing

- Run tests:

pytest -v

- Test coverage includes:
    - Upload endpoints (valid and invalid CSVs)
    - FK constraint validation
    - Batch insert logic
    - SQL-based reporting endpoints

---

## 🧾 Project Information


| Field      | Detail                                                                |
| ---------- | --------------------------------------------------------------------- |
| Author     | **Álvaro Adrianzen Vizcarra**                                         |
| Project    | Globant Data Engineering Challenge                                    |
| Created    | October 2025                                                          |
| Framework  | FastAPI + SQLAlchemy                                                  |
| Deployment | Docker + Azure ACI                                                    |
| License    | MIT License                                                           |

---

## 🚀 Next Steps

| Phase         | Improvement                                                       |
| ------------- | ----------------------------------------------------------------- |
| CI/CD         | Integrate **GitHub Actions** for automated build & deployment     |
| Database      | Migrate from SQLite to PostgreSQL (Azure Database for PostgreSQL) |
| Observability | Add logging & monitoring with Azure Monitor                       |
| Data QA       | Implement schema validation and quality assurance checks          |
| Security      | Add JWT authentication and environment management with `.env`     |

---

## 🖼️ Cloud Architecture

End-to-end deployment pipeline: GitHub → Docker → ACR → ACI → FastAPI API.

---
