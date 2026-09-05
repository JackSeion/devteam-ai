# DevTeam AI Architecture

## Purpose

DevTeam AI is an AI-powered software engineering system that takes a
software development task, analyzes a repository, generates code changes,
executes the changes in an isolated Docker environment, runs tests, and
iterates when failures occur.

## Core Workflow

User
→ FastAPI
→ Create Task
→ PostgreSQL
→ Redis Queue
→ Worker
→ LangGraph
→ Planner
→ Developer
→ Docker Sandbox
→ Tester
→ PostgreSQL

If testing fails, the result is returned to the Developer Agent for
another iteration.

## Components

### Frontend

React-based user interface.

Responsibilities:
- Submit development tasks
- Select repositories
- Display task status
- Display agent progress
- Display test results

### Backend

FastAPI application responsible for the HTTP API.

Responsibilities:
- Receive requests
- Validate input
- Manage persistent application state
- Create tasks
- Queue background work
- Expose task/run status

### Worker

Background processing service.

Responsibilities:
- Consume queued tasks
- Execute agent workflows
- Coordinate Planner, Developer, and Tester agents
- Persist execution state

### Execution

Sandboxed code execution environment.

Responsibilities:
- Prepare repository
- Apply generated changes
- Install dependencies
- Run tests
- Run lint/build commands
- Return execution results

### PostgreSQL

Primary persistent data store.

Stores:
- Users
- Repositories
- Tasks
- Runs
- Agent steps
- Test results

### Redis

Background job queue and temporary coordination layer.

### GitHub

Source-code repository provider.

### LangGraph

Agent workflow orchestration.

### Ollama

Local LLM runtime.

### pgvector

Vector storage and similarity search for repository RAG.
