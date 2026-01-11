#!/bin/bash

# AI-400 Task Management API Setup Script

set -e

echo "=========================================="
echo "AI-400 Task Management API Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your database credentials"
else
    echo ""
    echo "✓ .env file already exists"
fi

# Database setup
echo ""
echo "Using SQLite database (taskmanagement.db)"
echo "✓ No additional database setup required!"

# Run tests
echo ""
echo "Running tests..."
pytest -v

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
else
    echo ""
    echo "⚠️  Some tests failed. Please check the output above."
fi

# Final instructions
echo ""
echo "=========================================="
echo "Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start the API server:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Open your browser to:"
echo "   http://localhost:8000/docs"
echo ""
echo "3. Load demo data (optional):"
echo "   python demo_data.py"
echo ""
echo "4. Run skills demonstrations:"
echo "   python -m app.skills.code_review"
echo "   python -m app.skills.db_optimizer"
echo "   python -m app.skills.test_generator"
echo "   python -m app.skills.standup_reporter"
echo "   python -m app.skills.task_prioritizer"
echo ""
echo "=========================================="
