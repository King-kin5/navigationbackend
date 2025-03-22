# Campus Navigation Backend

A FastAPI-based backend service for managing building information and navigation within a campus environment.

## Features

- CRUD operations for campus buildings
- Building search and retrieval by slug
- PostgreSQL database with SQLAlchemy ORM
- Full text search capabilities
- Database connection pooling
- Automatic database seeding with sample data
- CORS support for frontend integration

## Prerequisites

- Python 3.8+
- PostgreSQL database
- pip package manager

## Installation

1. Clone the repository:
```sh
git clone <repository-url>
cd navigationbackend
```

2. Create and activate a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```

4. Set up environment variables by creating a `.env` file:
```
DATABASE_URL=postgresql://user:password@host:port/dbname
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development
DEBUG=true
```

## Database Setup

The application automatically handles database initialization, including:
- Creating the database if it doesn't exist
- Setting up required PostgreSQL extensions
- Creating database tables
- Seeding initial building data

## Project Structure

```
navigationbackend/
├── backend/
│   ├── core/
│   │   └── config.py         # Application configuration
│   ├── database/
│   │   ├── base.py          # Database connection setup
│   │   ├── config.py        # Database configuration
│   │   ├── init_db.py       # Database initialization
│   │   └── models/          # Database models
│   ├── routes/
│   │   └── building.py      # API endpoints
│   └── seed_data.py         # Sample data for seeding
├── main.py                  # Application entry point
├── requirements.txt         # Project dependencies
└── .env                     # Environment variables
```

## API Endpoints

### Buildings

- `GET /buildings/` - Get all buildings
- `GET /buildings/{slug}` - Get building by slug
- `PUT /buildings/{slug}` - Update building (full update)
- `PATCH /buildings/{slug}` - Partially update building

## Running the Application

1. Start the development server:
```sh
python main.py
```

Or using uvicorn directly:
```sh
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Access the API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Data Models

### Building Model

```python
{
    "id": "string",
    "slug": "string",
    "name": "string",
    "department": "string",
    "description": "string",
    "facilities": ["string"],
    "coordinates": {"lat": float, "lng": float}
}
```

## Development

The application uses:
- FastAPI for the web framework
- SQLAlchemy for ORM
- Pydantic for data validation
- PostgreSQL for the database
- SQLAlchemy Utils for database utilities

## Error Handling

The application includes comprehensive error handling for:
- Database connection issues
- Invalid data validation
- Resource not found errors
- General HTTP exceptions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.