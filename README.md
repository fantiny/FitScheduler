# FitScheduler

Backend API service for sports coach and venue booking management.

## Project Overview

FitScheduler is a full-featured appointment management system designed for sports coaches and venue reservations. The system supports:

- User, coach, and venue management
- Appointment creation and management
- Payment method management
- Rating and favorite functionality
- Authentication and authorization
- Permission control for different user roles

## Installation Guide

### Requirements

- Python 3.8+
- MySQL 5.7+
- Node.js 16+ (for frontend)

### Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/yourusername/bsweetOrder-yoyaku.git
cd bsweetOrder-yoyaku
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:

```bash
# Production dependencies
pip install -r requirements.txt --prefer-binary

# Development dependencies (including testing and code quality tools)
pip install -r requirements-dev.txt --prefer-binary
```

> **Note**: The `--prefer-binary` option prioritizes pre-compiled binary packages to avoid Rust compilation issues. If you still encounter Rust-related errors, ensure you have installed the [Rust toolchain](https://www.rust-lang.org/tools/install).

4. Configure environment variables (or create a .env file):

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=yoyaku
SECRET_KEY=your_secret_key
```

5. Initialize the database:

```bash
python app/db/init_db.py
```

6. Start the application:

#### Using Startup Script (Recommended)

On Windows systems, you can double-click the following batch file to start the service:

- `start-app.bat` - Start the backend API service

The startup script will automatically check the environment, create a virtual environment, install dependencies, and start the service.

#### Manual Startup

```bash
uvicorn main:app --reload --port 8000
```

The service will start at http://localhost:8000, and the API documentation will be available at http://localhost:8000/docs.

## Project Structure

```
yoyaku/
├── app/                      # Core application code
│   ├── api/                  # API layer
│   │   ├── dependencies/     # Shared dependencies (auth, permissions)
│   │   └── v1/               # API version 1
│   │       ├── endpoints/    # Resource endpoints
│   │       └── router.py     # Main router configuration
│   │
│   ├── core/                 # Core configuration
│   │   ├── config.py         # Configuration file
│   │   ├── security.py       # Security related
│   │   └── environment.py    # Environment configuration
│   │
│   ├── db/                   # Database related
│   │   ├── base.py           # Base model class
│   │   ├── session.py        # Database session
│   │   └── init_db.py        # Database initialization
│   │
│   ├── models/               # Database models (ORM)
│   │
│   ├── schemas/              # Pydantic models (request/response)
│   │
│   ├── services/             # Business logic layer
│   │
│   └── utils/                # Common utility functions
│
├── alembic/                  # Database migrations
│   └── versions/             # Migration versions
│
├── sql/                      # SQL scripts
│   └── ddl.sql               # Database definition
│
├── tests/                    # Test code
│   ├── unit_test.py          # Unit tests
│   ├── integration_test.py   # Integration tests
│   ├── test_setup.py         # Test data setup
│   └── testing_guide.md      # Testing guide
│
├── docs/                     # Documentation
│   ├── README_zh.md          # Chinese README
│   └── README_ja.md          # Japanese README
│
├── .env                      # Environment variables
│
├── .env.example              # Environment variables example
│
├── .gitignore                # Git ignore file
│
├── .dockerignore             # Docker ignore file
│
├── alembic.ini               # Alembic configuration
│
├── main.py                   # Application entry point
│
├── requirements.txt          # Production dependencies
│
├── requirements-dev.txt      # Development dependencies
│
└── start-app.bat             # Backend service startup script
```

## Frontend Project

This project has a separate frontend repository `fitscheduler-frontend` built with Vue 3 and Vite. The frontend project communicates with this backend project via API.

Frontend project repository: [FitScheduler Frontend](../fitscheduler-frontend)

### Starting the Frontend Project

The frontend project can be started using:

1. Startup script (in the frontend project directory):
   - `start-frontend.bat` - Start the frontend development server

2. Manual startup:
```bash
cd ../yoyaku-frontend
npm install
npm run dev
```

The frontend service will start at http://localhost:5173.

## API Usage Guide

### Authentication

The API uses JWT tokens for authentication. Steps to obtain a token:

1. Register a new user:

```
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "username": "example_user",
  "password": "secure_password",
  "phone": "12345678901"
}
```

2. Login and get a token:

```
POST /api/v1/auth/login
{
  "username": "user@example.com",
  "password": "secure_password"
}
```

3. Use the token for subsequent requests:

```
Authorization: Bearer <your_token>
```

### Main API Endpoints

- `/api/v1/auth/*` - Authentication related
- `/api/v1/users/*` - User management
- `/api/v1/coaches/*` - Coach management
- `/api/v1/venues/*` - Venue management
- `/api/v1/bookings/*` - Booking management
- `/api/v1/reviews/*` - Review management
- `/api/v1/lesson-types/*` - Lesson type management

Complete API documentation is available at the `/docs` endpoint after running the application.

## Development Guide

### Code Style

The project follows the PEP8 coding standard and uses the FastAPI official recommended project structure. The following tools are recommended for code quality control:

- `black` - Automatic code formatting
- `flake8` - Code style checking

These tools are included in `requirements-dev.txt`.

### Adding New Features

1. **Create a new database model**: Create in the `app/models/` directory

2. **Define Pydantic schema**: Create request and response schemas in the `app/schemas/` directory

3. **Implement service logic**: Add business logic in the `app/services/` directory

4. **Create API endpoint**: Add a new route in the `app/api/v1/endpoints/` directory

### Running Tests

First, ensure you have installed the development dependencies:

```bash
pip install -r requirements-dev.txt
```

Then use the following commands to run the tests:

```bash
python tests/test_setup.py  # Create test data
pytest tests/unit_test.py   # Run unit tests
pytest tests/integration_test.py  # Run integration tests
```

### Database Migrations

Use Alembic for database migrations:

```bash
# Create migration script
alembic revision --autogenerate -m "describe changes"

# Apply migration
alembic upgrade head
```

## Contribution Guidelines

Pull Requests and Issue reports are welcome. Please ensure the code passes all tests and follows the project coding standards.

## License

This project is licensed under the MIT License.

## Languages

This documentation is available in multiple languages:
- [English](README.md) (current)
- [中文](docs/README_zh.md)
- [日本語](docs/README_ja.md) 