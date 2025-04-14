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

# Building Management API

This API provides endpoints for managing buildings, including their details and images. The API uses FastAPI and supports form-data for handling file uploads.

## API Endpoints

### 1. Get All Buildings
```http
GET /api/buildings
```
Returns a list of all buildings with their details.

**Response Example:**
```json
[
    {
        "id": "etf-building",
        "slug": "etf-building",
        "name": "ETF Building",
        "department": "School of Engineering",
        "description": "The Electrical and Telecommunications Engineering facility",
        "image": "/api/buildings/image/etf-building.jpg",
        "facilities": ["Electronics Lab", "Telecommunications Lab"],
        "coordinates": {"lat": 6.518834, "lng": 3.372500}
    }
]
```

### 2. Get Building by Slug
```http
GET /api/{slug}
```
Returns details of a specific building by its slug.

**Example:**
```http
GET /api/etf-building
```

### 3. Create Building
```http
POST /api/buildings/create
```
Creates a new building. All fields are required except the image.

**Form Data:**
- `name` (required): Building name
- `department` (required): Department name
- `description` (required): Building description
- `facilities` (required): JSON string of facilities array
- `coordinates` (required): JSON string of coordinates
- `file` (optional): Image file

**Example using Postman:**
1. Set method to POST
2. Set URL to `/api/buildings/create`
3. Set Content-Type to `multipart/form-data`
4. Add form fields:
   ```
   name: New Building
   department: School of Engineering
   description: A new building description
   facilities: ["Lab", "Classroom"]
   coordinates: {"lat": 6.518834, "lng": 3.372500}
   file: [Select image file]
   ```

### 4. Update Building
```http
PUT /api/buildings/{slug}
```
Updates an existing building. All fields are optional - only include the fields you want to update.

**Form Data:**
- `name` (optional): New building name
- `department` (optional): New department name
- `description` (optional): New description
- `facilities` (optional): JSON string of new facilities array
- `coordinates` (optional): JSON string of new coordinates
- `file` (optional): New image file

**Example using Postman:**
1. Set method to PUT
2. Set URL to `/api/buildings/etf-building`
3. Set Content-Type to `multipart/form-data`
4. Add form fields (only include what you want to update):
   ```
   name: Updated Building Name
   facilities: ["New Lab", "Updated Room"]
   ```

### 5. Get Building Image
```http
GET /api/buildings/image/{filename}
```
Returns the image file for a building.

**Example:**
```http
GET /api/buildings/image/etf-building.jpg
```

### 6. Delete Building Image
```http
DELETE /api/buildings/{slug}/image
```
Deletes the image associated with a building.

**Example:**
```http
DELETE /api/buildings/etf-building/image
```

## Form Data Format

### Facilities Format
Facilities should be provided as a JSON string array:
```json
["Lab", "Classroom", "Office"]
```

### Coordinates Format
Coordinates should be provided as a JSON string object:
```json
{"lat": 6.518834, "lng": 3.372500}
```

## Image Handling

1. **Supported Image Types:**
   - JPEG/JPG
   - PNG
   - GIF

2. **Image Processing:**
   - Images are stored in the database
   - Each image is associated with a building
   - Images can be updated or deleted independently

3. **Image URLs:**
   - Image URLs follow the format: `/api/buildings/image/{filename}`
   - The filename is generated from the building's slug

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid input data
- `404 Not Found`: Building or image not found
- `500 Internal Server Error`: Server-side errors

## Example Usage

### Creating a Building with Image
```bash
curl -X POST "http://localhost:8000/api/buildings/create" \
  -H "Content-Type: multipart/form-data" \
  -F "name=New Building" \
  -F "department=Engineering" \
  -F "description=Building description" \
  -F "facilities=[\"Lab\",\"Classroom\"]" \
  -F "coordinates={\"lat\":6.518834,\"lng\":3.372500}" \
  -F "file=@building.jpg"
```

### Updating Building Name
```bash
curl -X PUT "http://localhost:8000/api/etf-building" \
  -H "Content-Type: multipart/form-data" \
  -F "name=Updated Building Name"
```



## License

This project is licensed under the MIT License.