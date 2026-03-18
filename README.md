# FleetLog – Vehicle Maintenance Backend API

FleetLog is a backend API for managing personal vehicle maintenance records. It allows users to register, authenticate, track multiple vehicles and log detailed service history with filtering and pagination support.

This project is designed to demonstrate real-world backend development practices including authentication, relational data modelling, API design and testing.

---

## Tech Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy ORM**
* **Alembic (migrations)**
* **JWT Authentication**
* **Docker (PostgreSQL)**
* **Pytest (testing)**

---

## Features

### Authentication

* User registration
* Secure login with JWT tokens
* Protected routes using bearer authentication

### Vehicle Management

* Create, read, update, delete vehicles
* Each user can manage multiple vehicles
* Ownership-based access control

### Service History Tracking

* Add maintenance records per vehicle
* Track:

  * service type
  * description
  * service date
  * odometer reading
  * cost
  * provider

### Advanced Querying

* Pagination (`limit`, `offset`)
* Filtering:

  * provider
  * date range
  * odometer range
* Sorting (ascending / descending)

### Testing

* Automated test suite using pytest
* Covers:

  * authentication
  * vehicle endpoints
  * service records
  * filtering logic

---

## API Structure

### Auth

* `POST /api/v1/auth/login`

### Users

* `POST /api/v1/users/`
* `GET /api/v1/users/me`

### Vehicles

* `POST /api/v1/vehicles/`
* `GET /api/v1/vehicles/`
* `GET /api/v1/vehicles/{vehicle_id}`
* `PUT /api/v1/vehicles/{vehicle_id}`
* `DELETE /api/v1/vehicles/{vehicle_id}`

### Service Records

* `POST /api/v1/vehicles/{vehicle_id}/service-records/`
* `GET /api/v1/vehicles/{vehicle_id}/service-records/`
* `GET /api/v1/vehicles/{vehicle_id}/service-records/{record_id}`
* `PUT /api/v1/vehicles/{vehicle_id}/service-records/{record_id}`
* `DELETE /api/v1/vehicles/{vehicle_id}/service-records/{record_id}`

---

## Example Requests

### Create User

```json
POST /api/v1/users/

{
  "email": "danny@example.com",
  "password": "testpassword123",
  "full_name": "Danny Hedayati"
}
```

### Login

```json
POST /api/v1/auth/login

{
  "email": "danny@example.com",
  "password": "testpassword123"
}
```

### Create Vehicle

```json
POST /api/v1/vehicles/

{
  "make": "Mazda",
  "model": "MX-5",
  "year": 2010,
  "registration_plate": "ABC123",
  "vin": "JM0TEST1234567890",
  "current_odometer": 67000
}
```

### Create Service Record

```json
POST /api/v1/vehicles/1/service-records/

{
  "title": "engine oil and filter",
  "description": "5w40 oil and fresh filter",
  "service_date": "2026-03-14",
  "odometer": 210500,
  "cost": 89.95,
  "provider": "home garage"
}
```

---

## Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/fleetlog.git
cd fleetlog
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file:

```
PROJECT_NAME=FleetLog API
VERSION=0.1.0
DEBUG=True
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fleetlog
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Run Database (Docker)

```bash
docker compose up -d
```

### 6. Run Migrations

```bash
alembic upgrade head
```

### 7. Start API

```bash
uvicorn app.main:app --reload
```

API available at:

* http://127.0.0.1:8000
* Swagger docs: http://127.0.0.1:8000/docs

---

## Running Tests

```bash
pytest -v
```

---

## Project Structure

```
app/
  api/
  core/
  models/
  schemas/
  main.py

tests/
  test_auth.py
  test_vehicles.py
  test_service_records.py
```

---

## Future Improvements

* vehicle summary endpoint (service stats)
* maintenance reminders
* CI pipeline (GitHub Actions)
* full containerised deployment

---

## Author

Daniel Hedayati
- This project is for educational and portfolio purposes.
