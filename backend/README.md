# 🚀 EchoWrite Backend

FastAPI-powered backend for AI-powered content curation and newsletter generation.

## 🏗️ Architecture

```
backend/
├── app/
│   ├── api/v1/           # API Routes
│   │   ├── health.py     # Health checks
│   │   ├── ingestion.py  # Content ingestion
│   │   ├── trends.py     # Trend analysis
│   │   ├── style.py      # Voice training
│   │   ├── generation.py # Newsletter generation
│   │   ├── delivery.py   # Email delivery
│   │   └── feedback.py   # User feedback
│   ├── core/             # Business Logic
│   │   ├── database.py   # Database connection
│   │   ├── ingestion/    # RSS/YouTube processing
│   │   ├── trends/       # Content scoring
│   │   ├── style/        # Voice analysis
│   │   ├── generation/   # AI newsletter creation
│   │   ├── delivery/     # Email sending
│   │   └── feedback/     # Feedback processing
│   ├── models/           # Pydantic schemas
│   │   └── schemas.py    # Data models
│   └── services/         # External integrations
├── database/             # Database migrations
│   ├── schema.sql        # Complete schema
│   └── migrations/       # SQL migrations
├── main.py               # FastAPI application
├── requirements.txt      # Python dependencies
└── test_apis.py         # API testing suite
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Supabase account
- OpenAI API key
- Resend API key (optional)

### Installation

1. **Create virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   ```bash
   cp env.example .env
   # Edit .env with your actual API keys
   ```

4. **Run the development server:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## 🔧 Environment Variables

```bash
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# AI Services
OPENAI_API_KEY=your_openai_api_key

# Email Service (Optional)
RESEND_API_KEY=your_resend_api_key

# Test Credentials (for testing)
TEST_EMAIL=test@example.com
TEST_PASSWORD=testpassword123
```

## 📊 API Endpoints

### Health Check

- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed service status

### Content Ingestion

- `POST /api/v1/ingestion/process` - Process content feeds
- `GET /api/v1/ingestion/sources` - Get user sources
- `POST /api/v1/ingestion/sources` - Add new source
- `DELETE /api/v1/ingestion/sources/{id}` - Delete source
- `POST /api/v1/ingestion/sources/{id}/test` - Test source

### Trend Analysis

- `POST /api/v1/trends/analysis` - Analyze trending content
- `GET /api/v1/trends/score/{id}` - Get item trend score

### Voice Training

- `POST /api/v1/style/train` - Train AI voice model
- `GET /api/v1/style/profile` - Get voice profile
- `POST /api/v1/style/samples` - Add style sample
- `DELETE /api/v1/style/samples/{id}` - Delete style sample

### Newsletter Generation

- `POST /api/v1/generation/newsletter` - Generate newsletter
- `GET /api/v1/generation/drafts` - Get user drafts
- `DELETE /api/v1/generation/drafts/{id}` - Delete draft

### Email Delivery

- `POST /api/v1/delivery/send` - Send newsletter
- `GET /api/v1/delivery/status/{id}` - Get delivery status

### User Feedback

- `POST /api/v1/feedback` - Submit feedback
- `GET /api/v1/feedback/analytics/{user_id}` - Get feedback analytics

## 🔐 Authentication

The backend uses JWT authentication with Supabase:

1. **JWT Token**: Extracted from `Authorization: Bearer <token>` header
2. **User Context**: Each request is scoped to the authenticated user
3. **Database Access**: Row-Level Security (RLS) policies enforce data isolation

### Example API Call

```python
import requests

headers = {
    'Authorization': 'Bearer <your_jwt_token>',
    'Content-Type': 'application/json'
}

# Get user's sources
response = requests.get(
    'http://localhost:8000/api/v1/ingestion/sources',
    headers=headers
)
```

## 🧪 Testing

### Run API Tests

```bash
python test_apis.py
```

This will:

- Test all API endpoints
- Create, test, and delete sample data
- Verify authentication
- Check error handling

### Test Individual Services

```bash
# Test content ingestion
python test_ingestion.py

# Test trend engine
python test_trend_engine.py

# Test newsletter generation
python test_newsletter_generation.py
```

## 📈 Performance

- **Health Check**: < 100ms response time
- **Authentication**: < 200ms login/signup
- **Content Ingestion**: < 5s for 10 sources
- **Trend Analysis**: < 2s for 100 items
- **Newsletter Generation**: < 30s with OpenAI

## 🔧 Development

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

### Database Migrations

```bash
# Apply new migrations
psql -h your_host -d your_db -f database/migrations/new_migration.sql
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection**: Ensure Supabase credentials are correct
2. **JWT Token**: Verify token format and expiration
3. **OpenAI API**: Check API key and rate limits
4. **Port Conflicts**: Kill processes on port 8000

### Debug Mode

```bash
# Run with debug logging
DEBUG=true python main.py
```

### Logs

- **API Logs**: Check console output
- **Database Logs**: Monitor Supabase dashboard
- **Error Tracking**: Check error responses for details

## 📚 Documentation

- **API Docs**: Visit `http://localhost:8000/api/docs` when running
- **Schema**: See `app/models/schemas.py` for data models
- **Database**: Check `database/schema.sql` for table structure

## 🔄 Deployment

### Production Checklist

- [ ] Set `ENVIRONMENT=production`
- [ ] Configure production database
- [ ] Set up proper logging
- [ ] Configure rate limiting
- [ ] Set up monitoring
- [ ] Configure SSL/TLS
- [ ] Set up backup strategy

---

**EchoWrite Backend** — _Powering AI-driven newsletters with FastAPI_
