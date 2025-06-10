# OptiChoice - Movie Recommendation System

A Django-based movie recommendation system with multiple AI models and a modern React frontend.

## Environment Setup

### 1. Clone the repository and navigate to the project directory
```bash
cd OPC2/OPC
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables Setup
Copy the example environment file and fill in your values:
```bash
cp .env.example .env
```

Edit the `.env` file with your actual values:
- **SECRET_KEY**: Generate a new Django secret key
- **EMAIL_HOST_USER**: Your Gmail address
- **EMAIL_HOST_PASSWORD**: Your Gmail app password (not your regular password)
- **DEBUG**: Set to `False` in production
- **ALLOWED_HOSTS**: Add your domain for production

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Load Movie Data (if available)
```bash
python manage.py loaddata movies_data.json  # if you have a fixture
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Security Notes

### Environment Variables
All sensitive information is stored in environment variables:
- Database credentials
- Email configuration
- Secret keys
- API keys
- JWT settings

### Gmail Setup for Email
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password
   - Use this password in `EMAIL_HOST_PASSWORD`

### Production Deployment
For production, make sure to:
1. Set `DEBUG=False`
2. Use a strong `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS`
4. Use environment variables for all sensitive data
5. Enable SSL/HTTPS
6. Use a production database (PostgreSQL recommended)

## API Endpoints

### Authentication
- `POST /auth/jwt/create/` - Login and get JWT tokens
- `POST /auth/jwt/refresh/` - Refresh access token
- `POST /register/` - User registration

### Movies
- `GET /movies/search/` - Search movies
- `POST /movies/recommend/` - Get movie recommendations
- `POST /movies/recommend-genre/` - Get genre-based recommendations

## Available AI Models

1. **TF-IDF** - Text-based similarity
2. **KNN** - K-Nearest Neighbors
3. **Genre-Based** - Genre similarity matching
4. **KNN-Genre** - KNN with genre features
5. **Embeddings** - Neural embeddings
6. **Neural Network** - Deep learning model

## Frontend

The React frontend is converted from Django templates and provides:
- User authentication with JWT
- Movie search with autocomplete
- AI-powered recommendations
- Dark/Light theme support
- Responsive design

## Development

### Adding New AI Models
1. Create a new file in `movies/ai_models/`
2. Implement the recommendation function
3. Add the model to `movies/views.py`
4. Update the frontend model selection

### Testing
```bash
python manage.py test
```

## Support

For issues and questions, please check the documentation or create an issue in the repository.
