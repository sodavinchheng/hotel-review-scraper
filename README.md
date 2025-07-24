> **[日本語版はこちら / Japanese version here](README.ja.md)**

# Full Stack Application

A modern full-stack application with React frontend and Python FastAPI backend, containerized with Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0 or higher)
- [Make](https://www.gnu.org/software/make/) (optional, for convenience commands)

## Project Structure

```
react-fastapi-template/
├── docker-compose.yml          # Main Docker Compose configuration
├── docker-compose.prod.yml     # Production overrides
├── Makefile                    # Convenience commands
├── README.md                   # This file
├── README.ja.md                # Japanese version of this file
├── frontend/                   # React application
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── assets              # Images, icons, etc
│       ├── components          # UI Components
│       │   ├── atoms           # Basic resuable components
│       │   ├── molecules       # Secondary reusable components
│       │   ├── organisms       # Reusable component blocks
│       │   ├── pages           # Page view component
│       │   └── ui              # Components installed using ShadCN ui
│       ├── constants           # Configuration values
│       ├── contexts            # Dependency
│       ├── core
│       │   ├── api             # OpenAPI class definition (See OpenAPI section for more details)
│       │   └── http            # OpenAPI connection client
│       ├── hooks               # Reusable hooks
│       ├── lib                 # Tailwindcss function installed by ShadCN ui
│       ├── services            # External service gateway functions
│       ├── types               # Application domain type definition
│       ├── utils               # Common utility functions
│       └── App.tsx
└── backend/                    # Python FastAPI application
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py
    ├── alembic
    │   └── versions            # Database migrations
    └── src/
        ├── config              # Constant values for configurations
        ├── controllers         # Usecase handlers
        ├── dependencies        # Dependency injection
        ├── database            # Database connection settings
        ├── models              # Database schema model definition
        ├── repositories        # Database operations and queries
        ├── routes              # API route handler
        ├── services            # External services
        ├── types               # API request and response classes
        └── utils               # Common functions
```

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/sodavinchheng/react-fastapi-template.git
cd react-fastapi-template
```

### 2. Add API keys

Create `.env` file in base directly

```bash
cp .env.sample .env
```

In the new `.env` file, add your own API key

### 3. Start Development Environment

[Optional] Create a python virtual environment (recommended for IDE intellisense)

```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r ./backend/requirements.txt
```

Using Make (recommended):

```bash
make dev
```

Or using Docker Compose directly:

```bash
docker-compose up --build -d
docker-compose exec backend alembic upgrade head
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **API Documentation**: (See OpenAPI section for more details)
  - _Swagger_: http://localhost:8000/docs
  - _Redoc_: http://localhost:8000/redoc
- **Database**: localhost:5432 (user: `user`, password: `password`, db: `appdb`)

## OpenAPI

FastAPI automatically generates an `openapi.json` file that can be displayed using Swagger UI.

Frontend application utilizes `openapi-generator-cli` in order to generate TypeScript classes of the API definitions. Run the command in order to sync the API definition classes with the API implementation.

```bash
make openapi
```

OR if you prefer not to use Make

```bash
docker-compose exec frontend npm run openapi:docker
```

OR if you prefer to run the command locally

```bash
npm run openapi
```

## Available Commands

If you have Make installed, you can use these convenient commands:

```bash
make dev          # Start development environment
make prod         # Start production environment
make build        # Build all services
make up           # Start services in background
make down         # Stop all services
make restart      # Restart all services
make logs         # View logs from all services
make clean        # Clean up containers, images, and volumes

# Database commands
make db-makemigration   # Create new database migration
make db-migrate         # Run database migrations
make db-reset           # Reset database to initial state
```

## Manual Docker Commands

If you prefer not to use Make:

```bash
# Start development
docker-compose up --build

# Start in background
docker-compose up -d --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose build frontend
docker-compose build backend

# Execute commands in containers
docker-compose exec backend python manage.py migrate
docker-compose exec frontend npm test
```

## Development Workflow

### Hot Reloading

Both frontend and backend support hot reloading during development:

- **Frontend**: React development server automatically reloads on file changes
- **Backend**: FastAPI with `--reload` flag restarts on Python file changes

### Making Changes

1. Edit files in `frontend/` or `backend/` directories
2. Changes are automatically reflected in the running containers
3. Database changes persist in the `postgres_data` volume

### Adding Dependencies

**Frontend (React):**

```bash
cd frontend
npm install <package-name>
```

**Backend (Python):**

```bash
cd backend
pip install <package-name>
echo "<package-name>==<version>" >> requirements.txt
```

Then rebuild the containers:

```bash
make build
```

## Environment Configuration

### Development Environment Variables

The application uses these default environment variables for development:

**Frontend:**

- `VITE_API_URL=http://localhost:8000`

**Backend:**

- `DATABASE_URL=postgresql://user:password@db:5432/appdb`
- `CORS_ORIGINS=http://localhost:5173`

**Database:**

- `POSTGRES_DB=appdb`
- `POSTGRES_USER=user`
- `POSTGRES_PASSWORD=password`

### Production Environment Variables

For production, update `docker-compose.prod.yml` with:

```yaml
environment:
  - REACT_APP_API_URL=https://api.yourdomain.com
  - DATABASE_URL=postgresql://user:secure_password@db:5432/appdb
  - CORS_ORIGINS=https://yourdomain.com
  - POSTGRES_PASSWORD=your_secure_password_here
```

## Production Deployment

### 1. Configure Environment

Edit `docker-compose.prod.yml` to update:

- Domain names
- Database credentials
- API URLs
- Any other environment-specific settings

### 2. Deploy

```bash
make prod
```

Or manually:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

### 3. Production Features

- **Frontend**: Served by Nginx with gzip compression and security headers
- **Backend**: Uses Gunicorn with multiple workers for better performance
- **Database**: Persistent storage with secure credentials
- **Security**: Non-root users, health checks, and proper CORS configuration

## Database Management

### Initial Setup

The database is automatically created when you start the services. To run initial migrations:

```bash
make db-migrate
```

### Reset Database

To reset the database to its initial state:

```bash
make db-reset
```

### Manual Database Access

```bash
docker-compose exec db psql -U user -d appdb
```

## Troubleshooting

### Common Issues

**Port Already in Use:**

```bash
# Stop services using the ports
make down
# Or change ports in docker-compose.yml
```

**Database Connection Issues:**

```bash
# Check if database is running
docker-compose ps
# View database logs
docker-compose logs db
```

**Permission Issues:**

```bash
# Clean up and rebuild
make clean
make build
```

### Viewing Logs

```bash
# All services
make logs

# Specific service
docker-compose logs -f frontend
docker-compose logs -f backend
docker-compose logs -f db
```

### Cleaning Up

To completely clean up Docker resources:

```bash
make clean
```

This removes:

- All containers
- Unused images
- Unused volumes
- Unused networks

## Development Tips

1. **Code Changes**: Both frontend and backend support hot reloading
2. **Database Data**: Persists between container restarts in `postgres_data` volume
3. **Logs**: Use `make logs` to monitor all services
4. **Testing**: Run tests inside containers with `docker-compose exec`
5. **Dependencies**: Add new packages and rebuild containers

## Support

For issues or questions:

1. Check the logs: `make logs`
2. Ensure Docker is running and up to date
3. Try cleaning up and rebuilding: `make clean && make build`
4. Check Docker Compose configuration files

## License

MIT
