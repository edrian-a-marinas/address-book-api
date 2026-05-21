# Address Book API

A minimal REST API built with FastAPI for managing addresses with coordinate support and distance-based search.

---

## Highlights

Beyond the core requirements, a few things worth calling out:

- **Logging at every meaningful event** — each route logs on entry, and services log on success, failure, and not-found cases with appropriate severity (`INFO`, `WARNING`, `ERROR`). Failures also trigger a `db.rollback()` before re-raising.
- **Coordinate validation in Pydantic schemas** — latitude/longitude bounds and empty-string checks are enforced in `AddressCreate` and `AddressUpdate` via `@field_validator`, so invalid data is rejected before it touches the database.
- **Geopy for geodesic distance** — uses a well-tested library instead of a hand-rolled formula.
- **Partial updates handled correctly** — `AddressUpdate` uses `exclude_unset=True`, so only fields explicitly provided in the request body are applied.
- **Containerized + tested** — Docker support and 16 passing tests covering CRUD and nearby search.
- **Type hints throughout**, ORM-based DB access, externalized config, and a clean project structure.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/edrian-a-marinas/address-book-api.git
cd address-book-api
```

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

**Windows:**
```bash
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

```env
DATABASE_URL=sqlite:///./address_book.db
DEBUG=True  # enables Swagger UI at /docs
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

---

## Docker

> Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) or Docker Engine (Linux).

### 1. Clone the repository

```bash
git clone https://github.com/edrian-a-marinas/address-book-api.git
cd address-book-api
```

### 2. Copy the environment file

**Windows:**
```bash
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

### 3. Build the image

```bash
docker build -t address-book-api .
```

### 4. Run the container

```bash
docker run -p 8000:8000 -e DEBUG=True address-book-api
```

Open `http://127.0.0.1:8000/docs`.

> If port 8000 is already in use, map to a different host port:
> ```bash
> docker run -p 8001:8000 -e DEBUG=True address-book-api
> ```
> Then open `http://127.0.0.1:8001/docs`.

---

## Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

16 tests covering CRUD and nearby search.

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/addresses/` | Create a new address |
| `GET` | `/api/v1/addresses/nearby` | Get addresses within a given distance |
| `GET` | `/api/v1/addresses/{address_id}` | Get address by ID |
| `PUT` | `/api/v1/addresses/{address_id}` | Update an address |
| `DELETE` | `/api/v1/addresses/{address_id}` | Delete an address |

---

## Example Payloads

### `POST /api/v1/addresses/`

```json
{
  "street": "123 Main St",
  "city": "Quezon City",
  "country": "Philippines",
  "latitude": 14.5995,
  "longitude": 120.9842
}
```

---

### `GET /api/v1/addresses/nearby`

| Parameter | Value |
|-----------|-------|
| `latitude` | `14.5995` |
| `longitude` | `120.9842` |
| `distance_km` | `10` |

---

### `GET /api/v1/addresses/{address_id}`

Provide the `address_id` of the address you want to retrieve (e.g. `1`).

---

### `PUT /api/v1/addresses/{address_id}`

Provide the `address_id` and any fields you want to update:

```json
{
  "street": "456 Rizal Ave",
  "city": "Makati",
  "country": "Philippines",
  "latitude": 14.5547,
  "longitude": 121.0244
}
```

---

### `DELETE /api/v1/addresses/{address_id}`

Provide the `address_id` of the address to delete. Returns `204 No Content` on success.

---

## Project Structure

```
address-book-api/
├── app/
│   ├── main.py        # Entry point
│   ├── routes.py      # Route handlers
│   ├── services.py    # Business logic
│   ├── models.py      # ORM models
│   ├── schemas.py     # Pydantic schemas
│   └── database.py    # DB connection and session
├── tests/
│   ├── conftest.py    # Fixtures
│   └── test_addresses.py
├── .env.example
├── Dockerfile
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — Web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM
- **[Pydantic](https://docs.pydantic.dev/)** — Validation
- **[Geopy](https://geopy.readthedocs.io/)** — Geodesic distance
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — Config
- **[Docker](https://www.docker.com/)** — Containerization
- **[pytest](https://docs.pytest.org/)** — Testing
