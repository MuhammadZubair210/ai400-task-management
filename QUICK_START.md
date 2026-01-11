# Quick Start Guide

Get the AI-400 Task Management API running in 3 minutes!

## Prerequisites

- Python 3.10+
- Git (for standup reporter skill)

**That's it!** No database installation needed - SQLite is built into Python.

## 1. Setup (1 minute)

```bash
# Clone/navigate to project
cd ai400-task-management

# Run automated setup
chmod +x setup.sh
./setup.sh
```

**Note**: The database (taskmanagement.db) will be created automatically when you first start the API!

## 2. Start the API (30 seconds)

```bash
# Activate virtual environment
source venv/bin/activate

# Start server
uvicorn app.main:app --reload
```

Server runs at: http://localhost:8000

API Docs at: http://localhost:8000/docs

## 3. Load Demo Data (30 seconds)

```bash
# In a new terminal
python demo_data.py
```

## 4. Try the Skills (2 minutes)

```bash
# Technical Skills
python -m app.skills.code_review
python -m app.skills.db_optimizer
python -m app.skills.test_generator

# Workflow Skills
python -m app.skills.standup_reporter
python -m app.skills.task_prioritizer
```

## 5. Run Tests (30 seconds)

```bash
pytest -v
```

## Quick API Examples

### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Task",
    "description": "Testing the API",
    "priority": "high",
    "status": "todo"
  }'
```

### Get All Tasks
```bash
curl "http://localhost:8000/tasks/"
```

### Update a Task
```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Delete a Task
```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## Interactive API Testing

Open http://localhost:8000/docs in your browser for interactive API documentation where you can:
- Test all endpoints
- See request/response schemas
- Try different parameters
- View example responses

## Common Issues

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

### Database Issues
SQLite is file-based, so no connection issues! If you need to reset:
```bash
# Delete the database file
rm taskmanagement.db

# Restart the API (database will be recreated)
uvicorn app.main:app --reload
```

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

1. Read [README.md](README.md) for detailed documentation
2. Explore [SKILLS_DOCUMENTATION.md](SKILLS_DOCUMENTATION.md) for skill details
3. Follow [DEMO_SCRIPT.md](DEMO_SCRIPT.md) to record your demo video
4. Modify and extend the skills for your own workflows!

## Need Help?

- Check the logs for error messages
- Ensure Python 3.10+ is installed
- Check that port 8000 is available
- Make sure virtual environment is activated
- Database file (taskmanagement.db) should be in the project root
