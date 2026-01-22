# Recipes API

## Overview


The system ingests a large JSON dataset of recipes, stores normalized data in a PostgreSQL database, exposes RESTful APIs for querying and searching recipes, and provides a lightweight frontend built with plain HTML, CSS, and JavaScript for visualization.

The focus of this implementation is correctness, clean backend design, real-world data handling, and clear API contracts.

---

## Tech Stack

### Backend

* Python 3.13
* FastAPI
* SQLAlchemy ORM
* PostgreSQL (JSONB support)

### Frontend

* Plain HTML
* Modern CSS (custom styling)
* Vanilla JavaScript (Fetch API)

---

## Project Structure

```
recipes-api/
│
├── app/
│   ├── main.py            # FastAPI app & CORS configuration
│   ├── database.py        # Database connection & session
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic response schemas
│   ├── services/
│   │   └── recipe_service.py
│   └── routes/
│       └── recipes.py     # API endpoints
│
├── scripts/
│   └── load_data.py       # JSON ingestion script
│
├── data/
│   └── recipes.json       # Provided recipe dataset
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── requirements.txt
├── .env
└── README.md
```

---

## Database Design

The `recipes` table stores normalized recipe information with support for nested data using PostgreSQL `JSONB`.

### Fields Stored

* `cuisine`
* `title`
* `rating`
* `prep_time`
* `cook_time`
* `total_time`
* `description`
* `nutrients` (JSONB)
* `instructions` (JSONB array)
* `serves`

Numeric fields containing invalid or `NaN` values in the input dataset are safely converted to `NULL` during ingestion.

---

## Data Ingestion

A dedicated ingestion script (`scripts/load_data.py`) is used to:

* Parse the large JSON file (13+ MB)
* Handle non-standard JSON structure (numeric-string keys)
* Convert invalid numeric values to `NULL`
* Store nested fields such as `nutrients` and `instructions` as JSONB

Run ingestion:

```bash
python3 -m scripts.load_data
```

---

## API Endpoints

### 1. Get All Recipes

**Endpoint**

```
GET /api/recipes
```

**Query Parameters**

* `page` (default: 1)
* `limit` (default: 10)

**Features**

* Pagination
* Sorted by rating (descending)

**Response Format**

```json
{
  "page": 1,
  "limit": 10,
  "total": 8451,
  "data": [ ... ]
}
```

---

### 2. Search Recipes

**Endpoint**

```
GET /api/recipes/search
```

**Supported Filters**

* `title` (partial match)
* `cuisine` (exact match)
* `rating` (>=, <=, =)
* `total_time` (>=, <=, =)
* `calories` (>=, <=, = from JSONB field)

**Example**

```
/api/recipes/search?title=pie&rating=>=4.5&calories=<=400
```

**Response Format**

```json
{
  "data": [ ... ]
}
```

---

## Frontend

The frontend is implemented using plain HTML, CSS, and JavaScript to keep the setup lightweight and framework-independent.

### Features

* Tabular view of recipes
* Pagination with configurable page size (15–50)
* Field-level search using `/search` API
* Right-side drawer for detailed recipe view
* Step-by-step instructions rendered as ordered lists
* Nutrition information rendered as readable key–value lists

The frontend communicates with the backend using Fetch API and relies on CORS middleware for cross-origin requests.

---

## CORS Configuration

CORS middleware is enabled in the FastAPI application to allow the frontend (served from a different origin or file system) to access the backend APIs during development.

---

## How to Run the Project

### Backend

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend will be available at:

```
https://recipes-awbz.onrender.com/docs
```

Swagger UI:

```
https://recipes-awbz.onrender.com/docs
```

### Frontend

Open `frontend/index.html` in a browser or serve it using a local static server.

---

## Notes

* Database schema creation is handled programmatically for simplicity (assessment scope).
* No authentication or authorization is implemented as it was not required.
* The project prioritizes backend correctness, data handling, and API clarity over frontend complexity.

---

