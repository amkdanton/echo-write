#!/bin/bash

# EchoWrite Status Check Script

echo "🔍 EchoWrite Status Check"
echo "=========================="
echo ""

# Check if backend is running
echo "📡 Backend Status:"
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Backend is running on port 8000"
    echo "   URL: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/api/docs"
else
    echo "❌ Backend is NOT running"
    echo "   To start: cd backend && source venv/bin/activate && python main.py"
fi
echo ""

# Check if frontend is running  
echo "⚛️  Frontend Status:"
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Frontend is running on port 3000"
    echo "   URL: http://localhost:3000"
else
    echo "❌ Frontend is NOT running"
    echo "   To start: cd frontend && npm run dev"
fi
echo ""

# Check Python virtual environment
echo "🐍 Python Environment:"
if [ -d "backend/venv" ]; then
    echo "✅ Virtual environment exists"
    if [ -f "backend/venv/bin/python" ]; then
        PYTHON_VERSION=$(backend/venv/bin/python --version 2>&1)
        echo "   $PYTHON_VERSION"
    fi
else
    echo "❌ Virtual environment not found"
    echo "   Run: cd backend && python -m venv venv"
fi
echo ""

# Check Node modules
echo "📦 Frontend Dependencies:"
if [ -d "frontend/node_modules" ]; then
    echo "✅ Node modules installed"
else
    echo "❌ Node modules not found"
    echo "   Run: cd frontend && npm install"
fi
echo ""

# Check environment files
echo "⚙️  Configuration:"
if [ -f "backend/.env" ]; then
    echo "✅ Backend .env exists"
else
    echo "⚠️  Backend .env not found"
    echo "   Copy: cp backend/env.example backend/.env"
fi

if [ -f "frontend/.env.local" ]; then
    echo "✅ Frontend .env.local exists"
else
    echo "⚠️  Frontend .env.local not found"
    echo "   Create with: VITE_API_URL=http://localhost:8000/api/v1"
fi
echo ""

echo "=========================="
echo "💡 Quick Commands:"
echo "   Kill backend:  lsof -ti:8000 | xargs kill -9"
echo "   Kill frontend: lsof -ti:3000 | xargs kill -9"
echo "   Full setup:    ./dev.sh"
echo ""
