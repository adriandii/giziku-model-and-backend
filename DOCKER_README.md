# Giziku - Food Nutrition API Docker Setup

## Prerequisites
- Docker installed on your system
- Docker Compose installed

## Running with Docker Compose

### 1. Build and Start Services
```bash
cd app
docker-compose up --build
```

### 2. Access the API
- **API Base URL:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

### 3. Database Access (if needed)
- **Host:** localhost
- **Port:** 3306
- **User:** root
- **Password:** password
- **Database:** giziku

## Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f mysql
```

### Stop Services
```bash
docker-compose down
```

### Rebuild Images
```bash
docker-compose up --build
```

### Remove Volumes (Reset Database)
```bash
docker-compose down -v
```

## File Structure
```
giziku/
├── app/
│   ├── Dockerfile           # Container image definition
│   ├── docker-compose.yml   # Services orchestration
│   ├── requirements.txt     # Python dependencies
│   ├── main.py             # FastAPI application
│   ├── database.py         # Database configuration
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── auth.py             # Authentication logic
│   ├── model.py            # ML model inference
│   ├── nutrition.py        # Nutrition calculations
│   └── macro.py            # Macro calculations
├── model/
│   └── mobilenet_food_model.h5  # Pre-trained model
├── .dockerignore            # Files to exclude from Docker build
└── .env                     # Environment variables
```

## Troubleshooting

### "Connection refused" error
- Wait a few seconds for MySQL to start up completely
- Check if MySQL container is running: `docker-compose ps`
- View MySQL logs: `docker-compose logs mysql`

### Port already in use
If port 8000 or 3306 is already in use:
1. Edit `docker-compose.yml` to use different ports
2. Change line 7 to: `- "8001:8000"` (for example)
3. Change line 23 to: `- "3307:3306"` (for example)

### Model Loading Issues
Ensure the model file exists at `../model/mobilenet_food_model.h5` relative to the Dockerfile

## Environment Variables
Update `.env` file or pass them to `docker-compose`:
```bash
DATABASE_URL=mysql+pymysql://root:password@mysql:3306/giziku \
docker-compose up
```

## Notes
- The database persists in a Docker volume named `giziku_mysql_data`
- Containers automatically restart on failure
- The model file is copied during build, not mounted, so rebuild if you update the model
