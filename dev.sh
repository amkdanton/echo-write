#!/bin/bash

# EchoWrite Development Script
# Optimized for MacBook with 8GB RAM (no Docker)

echo "🩶 EchoWrite Development Setup"
echo "================================"

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Please run this script from the echowrite root directory"
    exit 1
fi

echo "📋 Starting EchoWrite development environment..."
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is required but not installed"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is required but not installed"
    exit 1
fi

echo "✅ All prerequisites found"
echo ""

# Setup backend
echo "🐍 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "📦 Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "⚙️  Setting up environment variables..."
    cp env.example .env
    echo "📝 Please edit backend/.env with your API keys"
fi

echo "✅ Backend setup complete"
echo ""

# Setup frontend
echo "⚛️  Setting up frontend..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

if [ ! -f ".env.local" ]; then
    echo "⚙️  Setting up frontend environment..."
    echo "VITE_API_URL=http://localhost:8000/api/v1" > .env.local
fi

echo "✅ Frontend setup complete"
echo ""

# Back to root
cd ..

echo "🎉 Setup complete!"
echo ""
echo "🚀 To start development:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "📱 Access your app:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/api/docs"
echo ""
echo "💡 Don't forget to configure your .env files with API keys!"
