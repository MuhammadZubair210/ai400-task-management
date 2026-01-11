# Demo Video Script (60-90 seconds)

## Introduction (10 seconds)
"Hi! I'm presenting my AI-400 Class 1 Project: A Task Management API with AI-powered agent skills."

## Part 1: Show the Skills (25 seconds)

### Technical Skills Demo
**Screen: Terminal running skills**

"First, let me show you the three technical skills I built:"

1. **Code Review Skill** (8 seconds)
   ```bash
   python -m app.skills.code_review
   ```
   "This automatically analyzes Python code for issues, style violations, and potential bugs."

2. **Database Optimizer** (8 seconds)
   ```bash
   python -m app.skills.db_optimizer
   ```
   "This analyzes SQL queries and provides optimization recommendations with a score."

3. **Test Generator** (9 seconds)
   ```bash
   python -m app.skills.test_generator
   ```
   "And this automatically generates pytest test cases for FastAPI endpoints."

## Part 2: Workflow Skills (15 seconds)

**Screen: Running workflow skills**

"I also created two daily workflow automation skills:"

1. **Standup Reporter** (7 seconds)
   ```bash
   python -m app.skills.standup_reporter
   ```
   "Generates daily standup reports from git commits and tasks."

2. **Task Prioritizer** (8 seconds)
   ```bash
   python -m app.skills.task_prioritizer
   ```
   "Intelligently prioritizes tasks using deadlines and urgency scoring."

## Part 3: API Demo (30 seconds)

**Screen: Browser showing API docs**

"Now let me show the Task Management API with full CRUD operations:"

1. **Show API Documentation** (5 seconds)
   - Navigate to `http://localhost:8000/docs`
   "Here's the interactive API documentation with all endpoints."

2. **Create Task** (8 seconds)
   - Use POST /tasks/ endpoint
   - Show request body with title, description, priority
   "Creating a new task with priority and due date."

3. **List Tasks** (5 seconds)
   - Use GET /tasks/ endpoint
   "Retrieving all tasks with filtering options."

4. **Update Task** (7 seconds)
   - Use PUT /tasks/{id} endpoint
   "Updating task status to in_progress."

5. **Delete Task** (5 seconds)
   - Use DELETE /tasks/{id} endpoint
   "And deleting a completed task."

## Part 4: Tests (10 seconds)

**Screen: Terminal running tests**

```bash
pytest -v
```

"All features are tested with pytest. Here are the passing tests for both the API and skills."

**Show: Green passing tests**

## Closing (5 seconds)

**Screen: Project structure or README**

"This project demonstrates FastAPI, SQLModel, pytest, and reusable agent skills. Thanks for watching!"

---

## Technical Setup for Recording

### Before Recording:
1. Set up virtual environment
2. Install dependencies
3. Start the FastAPI server in one terminal (database creates automatically!)
4. Open browser to API docs
5. Have terminals ready for skill demos
6. Optionally load sample data with `python demo_data.py`

### Terminal Commands to Run:
```bash
# Terminal 1: Start API
uvicorn app.main:app --reload

# Terminal 2: Skills demos
python -m app.skills.code_review
python -m app.skills.db_optimizer
python -m app.skills.test_generator
python -m app.skills.standup_reporter
python -m app.skills.task_prioritizer

# Terminal 3: Run tests
pytest -v --tb=short

# Browser: API Documentation
http://localhost:8000/docs
```

## Recording Tips:
- Record in 1080p or higher
- Use a clean terminal with large font
- Speak clearly and at a steady pace
- Practice the demo 2-3 times before recording
- Keep total time between 60-90 seconds
- Show confidence and enthusiasm!

## Alternative Quick Demo Structure (60 seconds)

1. **Intro** (5s): "AI-400 Task Management API with agent skills"
2. **Skills Overview** (20s): Quickly show all 5 skills running with output
3. **API Demo** (25s): Show FastAPI docs, create/read/update/delete tasks
4. **Tests** (7s): Run pytest showing green tests
5. **Close** (3s): "Full CRUD API with automation skills"
