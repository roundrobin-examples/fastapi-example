# FastAPI Example Application

A comprehensive FastAPI example application demonstrating modern Python web development practices with:

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 🔐 **Authentication** - JWT-based authentication with password hashing
- 🗄️ **Database** - SQLAlchemy with async support (SQLite/PostgreSQL)
- 📝 **API Documentation** - Automatic OpenAPI/Swagger documentation
- 🧪 **Testing** - Comprehensive test suite with pytest
- 📦 **Package Management** - Modern dependency management with `uv`
- 🏗️ **Project Structure** - Clean, scalable project organization
- 🔧 **Configuration** - Environment-based configuration management

## Features

### Core Features

- User registration and authentication
- JWT token-based authorization
- Password hashing with bcrypt
- Database operations with async SQLAlchemy
- API versioning (v1)
- Request/response validation with Pydantic
- Comprehensive error handling
- CORS configuration

### API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/` - List users (admin only)
- `POST /api/v1/users/` - Create user (admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user (admin only)
- `DELETE /api/v1/users/{user_id}` - Delete user (admin only)

## Quick Start

### Prerequisites

- Python 3.9+
- `uv` package manager

### Installation

Requirements: uv, python 3.13+

1. **Install dependencies**

   ```bash
   uv sync
   ```

2. **Set up environment**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the application**

   ```bash
   uv run python -m app.main
   ```

   Or with uvicorn directly:

   ```bash
   uv run uvicorn app.main:app --reload
   ```

4. **Access the API**
   - Application: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## Development

### Project Structure

```
fastapi-example/
├── app/
│   ├── api/
│   │   ├── deps.py              # API dependencies
│   │   └── v1/
│   │       ├── api.py           # API router
│   │       └── endpoints/
│   │           ├── auth.py      # Authentication endpoints
│   │           └── users.py     # User management endpoints
│   ├── core/
│   │   ├── config.py            # Configuration settings
│   │   ├── security.py          # Security utilities
│   │   └── exceptions.py        # Exception handlers
│   ├── crud/
│   │   └── user.py              # Database operations
│   ├── db/
│   │   └── database.py          # Database setup
│   ├── models/
│   │   └── user.py              # SQLAlchemy models
│   ├── schemas/
│   │   └── user.py              # Pydantic schemas
│   ├── utils/                   # Utility functions
│   └── main.py                  # FastAPI application
├── tests/                       # Test suite
├── pyproject.toml              # Project configuration
├── .env.example                # Environment template
└── README.md                   # This file
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test file
uv run pytest tests/test_main.py
```

### Database Management

#### Using SQLite (Default)

The application uses SQLite by default, which is perfect for development and testing.

#### Using PostgreSQL (Production)

1. Install PostgreSQL
2. Create a database
3. Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database_name
   ```

#### Database Migrations (Future Enhancement)

The project is set up for Alembic migrations:

```bash
# Initialize migrations (when needed)
uv run alembic init alembic

# Create migration
uv run alembic revision --autogenerate -m "Description"

# Apply migrations
uv run alembic upgrade head
```

### Creating Your First User

Since the application starts with an empty database, you'll need to create your first user. You can do this by:

1. **Using the API directly** (after starting the app):

   ```bash
   curl -X POST "http://localhost:8000/api/v1/users/" \
        -H "Content-Type: application/json" \
        -d '{
          "email": "admin@example.com",
          "username": "admin",
          "password": "securepassword123",
          "full_name": "Admin User",
          "is_active": true
        }'
   ```

2. **Or add a script** to create an initial superuser (you can create this)

### Authentication Flow

1. **Create a user** (or use existing)
2. **Login** with username/password to get JWT token:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin&password=securepassword123"
   ```
3. **Use the token** in subsequent requests:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/users/me" \
        -H "Authorization: Bearer YOUR_TOKEN_HERE"
   ```

## Configuration

Key configuration options in `.env`:

| Variable                      | Description                | Default  |
| ----------------------------- | -------------------------- | -------- |
| `DEBUG`                       | Enable debug mode          | `False`  |
| `SECRET_KEY`                  | JWT signing key            | Required |
| `DATABASE_URL`                | Database connection string | SQLite   |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time      | `30`     |
| `ALLOWED_HOSTS`               | CORS allowed origins       | `["*"]`  |

## API Documentation

Once the application is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The documentation is automatically generated from your code and includes:

- All endpoints with descriptions
- Request/response schemas
- Authentication requirements
- Try-it-out functionality

## Production Deployment

### Security Considerations

1. **Change the SECRET_KEY** to a strong, random value
2. **Use PostgreSQL** instead of SQLite
3. **Set DEBUG=False**
4. **Configure proper ALLOWED_HOSTS**
5. **Use HTTPS** in production
6. **Set up proper logging**
7. **Configure rate limiting**

### Environment Variables for Production

```bash
DEBUG=False
ENVIRONMENT=production
SECRET_KEY=your-very-long-random-secret-key
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
```

### Docker (Future Enhancement)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install uv && uv pip install --system .
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Next Steps

This is a foundation that you can extend with:

- **Database Migrations** with Alembic
- **Background Tasks** with Celery/RQ
- **File Upload** handling
- **Email Services** integration
- **Rate Limiting** with slowapi
- **Caching** with Redis
- **Docker** containerization
- **CI/CD** pipeline setup
- **Monitoring** and logging
- **API Rate Limiting**
- **WebSocket** support
- **GraphQL** integration

Happy coding! 🎉
