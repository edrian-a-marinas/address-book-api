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

A `.env` file is included in this repository for assessment purposes only, so reviewers can run the project immediately without any additional setup.

> **Note:** In a real production setup, `.env` should never be committed to version control. It would be listed in `.gitignore` and provisioned separately per environment.

The included `.env`:

```env
DATABASE_URL=sqlite:///./address_book.db
DEBUG=True
```

> `DEBUG=True` enables the Swagger UI at `http://127.0.0.1:8000/docs`. Set to `False` in production to disable it.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

---

## Running with Docker

```bash
docker build -t address-book-api .
docker run -p 8000:8000 -e DEBUG=True address-book-api
```

Then open `http://localhost:8000/docs`.

---

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

All 16 tests should pass covering CRUD operations and nearby address search.

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

## Example Usage

Use the built-in Swagger UI at `http://127.0.0.1:8000/docs` to interact with the API directly — no external tools needed.

1. Click on any endpoint to expand it
2. Click **"Try it out"**
3. Fill in the request body or parameters
4. Click **"Execute"**

### Create an address — `POST /api/v1/addresses/`

```json
{
  "street": "123 Main St",
  "city": "Quezon City",
  "country": "Philippines",
  "latitude": 14.5995,
  "longitude": 120.9842
}
```

### Get address by ID — `GET /api/v1/addresses/{id}`

Set `id` to `1` to retrieve the address created above.

### Update an address — `PUT /api/v1/addresses/{id}`

```json
{
  "street": "456 Rizal Ave",
  "city": "Makati",
  "country": "Philippines",
  "latitude": 14.5547,
  "longitude": 121.0244
}
```

### Delete an address — `DELETE /api/v1/addresses/{id}`

Set `id` to the address you want to remove. Returns `204 No Content` on success.

### Get nearby addresses — `GET /api/v1/addresses/nearby`

| Parameter | Value |
|-----------|-------|
| `latitude` | `14.5995` |
| `longitude` | `120.9842` |
| `distance_km` | `10` |

Returns all addresses within 10km of the given coordinates.

---

## Project Structure

```
address-book-api/
├── app/
│   ├── main.py        # FastAPI app entry point
│   ├── routes.py      # Route handlers
│   ├── services.py    # Business logic
│   ├── models.py      # SQLAlchemy ORM models
│   ├── schemas.py     # Pydantic request/response schemas
│   └── database.py    # Database connection and session
├── tests/
│   ├── conftest.py    # Shared fixtures (client, db setup, sample data)
│   └── test_addresses.py  # Tests for all endpoints
├── .env               # Included for assessment purposes only
├── .gitignore
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
- **[SQLite](https://www.sqlite.org/)** — Database
- **[Pydantic](https://docs.pydantic.dev/)** — Data validation
- **[Geopy](https://geopy.readthedocs.io/)** — Geodesic distance calculation
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** — Environment variable management
- **[Docker](https://www.docker.com/)** — Containerization
- **[pytest](https://docs.pytest.org/)** — Testing