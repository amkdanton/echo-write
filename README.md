# 🩶 EchoWrite

### _Crafting clarity from the chatter._

AI-powered content curation and newsletter automation for creators, agencies, and marketers. EchoWrite listens to the digital noise, finds what matters, and drafts your next newsletter — in your voice, every morning.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Supabase account
- OpenAI API key
- Resend API key

> **Note**: No Docker required! This setup is optimized for local development on MacBook with limited RAM.

### Backend Setup (FastAPI)

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   ```bash
   cp env.example .env
   # Edit .env with your actual API keys
   ```

5. **Run the development server:**

   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/api/docs`

### Frontend Setup (React)

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Set up environment variables:**

   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API URL
   ```

4. **Run the development server:**

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

### Alternative: Run Both Services

You can run both backend and frontend simultaneously:

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## 🏗️ Architecture

```
echowrite/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/         # API Routes
│   │   ├── core/           # Business Logic
│   │   │   ├── ingestion/  # RSS/YouTube/Twitter
│   │   │   ├── trends/     # Content scoring
│   │   │   ├── style/      # Voice training
│   │   │   ├── generation/ # AI newsletter creation
│   │   │   └── delivery/   # Email sending
│   │   ├── models/         # Pydantic schemas
│   │   └── services/       # External integrations
│   ├── main.py             # FastAPI app
│   └── requirements.txt
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # UI Components
│   │   ├── pages/          # Route Components
│   │   ├── services/       # API Client
│   │   └── utils/          # Utilities
│   ├── package.json
│   └── vite.config.ts
└── docs/                   # Documentation
```

## 🛠️ Core Features

### 🎯 Complete MVP Features

- ✅ **User Authentication**: Supabase Auth with JWT tokens
- ✅ **Content Sources**: RSS feeds and YouTube channel integration
- ✅ **Content Ingestion**: Real-time RSS and YouTube feed processing
- ✅ **Trend Analysis**: Sophisticated 5-component scoring algorithm
- ✅ **AI Newsletter Generation**: OpenAI-powered content creation
- ✅ **Drafts Management**: Full CRUD operations with preview
- ✅ **Newsletter Delivery**: Send functionality with status tracking
- ✅ **User Feedback**: Reaction tracking and analytics
- ✅ **Dashboard**: Real-time statistics and quick actions
- ✅ **Settings**: User preferences and voice training
- ✅ **Database Schema**: Complete PostgreSQL setup with RLS
- ✅ **API Integration**: Comprehensive REST API with authentication
- ✅ **Frontend Interface**: Modern React dashboard with TypeScript
- ✅ **Testing Suite**: Automated API testing with real data

## 🔧 Environment Variables

### Backend (.env)

```bash
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# AI Services
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Email Service
RESEND_API_KEY=your_resend_api_key

# Redis (for background tasks)
REDIS_URL=redis://localhost:6379/0

# Environment
ENVIRONMENT=development
DEBUG=true
```

### Frontend (.env.local)

```bash
VITE_API_URL=http://localhost:8000/api/v1
```

## 📊 Database Schema

The application uses Supabase (PostgreSQL) with the following main tables:

- `users` - User profiles and preferences
- `sources` - RSS feeds, YouTube channels, Twitter accounts
- `items` - Content items with trend scores
- `style_samples` - Writing samples for voice training
- `drafts` - Generated newsletter drafts
- `feedback` - User feedback on newsletters

## 🚀 API Endpoints

### Health

- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed service status

### Ingestion

- `POST /api/v1/ingestion/process` - Process content feeds
- `GET /api/v1/ingestion/sources` - Get user sources
- `POST /api/v1/ingestion/sources` - Add new source
- `DELETE /api/v1/ingestion/sources/{id}` - Delete source

### Trends

- `POST /api/v1/trends/analysis` - Analyze trending content
- `GET /api/v1/trends/score/{id}` - Get item trend score

### Style

- `POST /api/v1/style/train` - Train AI voice model
- `GET /api/v1/style/profile` - Get voice profile

### Generation

- `POST /api/v1/generation/newsletter` - Generate newsletter
- `GET /api/v1/generation/drafts` - Get user drafts

### Delivery

- `POST /api/v1/delivery/send` - Send newsletter
- `GET /api/v1/delivery/status/{id}` - Get delivery status

### Feedback

- `POST /api/v1/feedback` - Submit feedback
- `GET /api/v1/feedback/analytics/{user_id}` - Get feedback analytics

## 🧪 Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
black .
flake8 .

# Frontend linting
cd frontend
npm run lint
```

## 🆘 Troubleshooting

Having issues? We've got you covered:

- **QUICK_FIXES.md** - Instant solutions for common problems
- **TROUBLESHOOTING.md** - Comprehensive troubleshooting guide
- **check-status.sh** - Run `./check-status.sh` to diagnose issues

**Most Common Fixes:**

```bash
# Kill port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill port 3000 (frontend)
lsof -ti:3000 | xargs kill -9

# Reinstall frontend dependencies
cd frontend && npm install
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is open-sourced under the **MIT License**.

---

**EchoWrite** — _Crafting clarity from the chatter._
