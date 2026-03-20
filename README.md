# FleetLog – Vehicle Maintenance Backend API

FleetLog is a backend API for managing personal vehicle maintenance records. It allows users to register, authenticate, track multiple vehicles and log detailed service history with filtering and pagination support.

This project demonstrates practical backend engineering concepts including authentication, relational data modelling, API design, containerisation and automated testing.

---

## Tech Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy ORM**
* **Alembic (migrations)**
* **JWT Authentication**
* **Docker (API + Database)**
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

## Getting Started (Docker)

### 1. Clone Repository

```bash
git clone https://github.com/86monti/fleetlog-api.git
cd fleetlog-api
```

### 2. Create Environment File

```bash
cp .env.example .env
```

Update values if needed.

### 3. Start the Full Stack

```bash
docker compose up --build
```

This starts:

* PostgreSQL (port 5432)
* API (port 8000)

### 4. Run Migrations

```bash
docker compose exec api alembic upgrade head
```

### 5. Access the API

* API: http://127.0.0.1:8000
* Swagger Docs: http://127.0.0.1:8000/docs

---

## Running Tests

Run tests locally:

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

Dockerfile
docker-compose.yml
```

---

## Development Notes

* API and database are fully containerised
* Uses Alembic for schema migrations
* PostgreSQL data is persisted via Docker volume
* Protected endpoints require JWT bearer tokens
* Users can only access their own vehicles and service records

---

## Future Improvements

* vehicle summary endpoint (service stats)
* maintenance reminders
* CI pipeline (GitHub Actions)
* cloud deployment

---

## Author

Daniel Hedayati

This project is for educational and portfolio purposes.
