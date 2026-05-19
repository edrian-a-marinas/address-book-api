# Address Book API

A minimal REST API built with FastAPI for managing addresses with coordinate support and distance-based search.

## Getting Started

### 1. Clone the repository

```bash
git clone git@github.com:edrian-a-marinas/address-book-api.git
cd address-book-api
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

A `.env` file is included for assessment purposes only — in production, this should never be committed.

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

```bash
docker build -t address-book-api .
docker run -p 8000:8000 -e DEBUG=True address-book-api
```

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
| `GET` | `/api/v1/addresses/{id}` | Get address by ID |
| `PUT` | `/api/v1/addresses/{id}` | Update an address |
| `DELETE` | `/api/v1/addresses/{id}` | Delete an address |
| `GET` | `/api/v1/addresses/nearby` | Get addresses within a given distance |

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

### `PUT /api/v1/addresses/{id}`

```json
{
  "street": "456 Rizal Ave",
  "city": "Makati",
  "country": "Philippines",
  "latitude": 14.5547,
  "longitude": 121.0244
}
```

### `DELETE /api/v1/addresses/{id}`

Returns `204 No Content` on success.

### `GET /api/v1/addresses/nearby`

| Parameter | Value |
|-----------|-------|
| `latitude` | `14.5995` |
| `longitude` | `120.9842` |
| `distance_km` | `10` |

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
├── .env
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