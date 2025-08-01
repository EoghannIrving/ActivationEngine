# Activation Engine

Activation Engine is a small FastAPI service that scores and tags user tasks based on contextual information like energy level, mood, and surroundings. It is designed as a stateless module that other apps can call to suggest relevant tasks or tags.

## Features
- Generate context tags from a `UserState` payload.
- Rank tasks using simple scoring rules defined in `weights.yaml`.
- Exposed REST endpoints via FastAPI (`/get-tags` and `/rank-tasks`).
- Dockerfile for containerized deployment.

## Requirements
- Python 3.11+
- Packages listed in `requirements.txt` (`fastapi`, `uvicorn`, `pydantic`).

Install dependencies with:
```bash
pip install -r requirements.txt
```

## Running Locally

Start the API using Uvicorn:
```bash
uvicorn main:app --reload
```
The server will be available at `http://localhost:8000` by default. Use any REST client to interact with the endpoints.

## API Endpoints

### `POST /get-tags`
Input: a `UserState` object. Returns a list of context tags derived from the user state.

### `POST /rank-tasks`
Input: a `TaskRequest` object containing `UserState` and a list of `Task` objects. Returns the tasks ranked from highest to lowest score.

See `main.py` for model definitions.

## Configuration

Scoring weights live in `weights.yaml`. Modify these values to tune how energy and executive cost influence the ranking algorithm. The file also contains placeholder weights for future tag matching.

## Docker
Build and run the Docker image:
```bash
docker build -t activation-engine .
docker run -p 80:80 activation-engine
```

## Roadmap & Known Issues
Planned enhancements and known bugs are documented in [`ROADMAP.md`](ROADMAP.md) and [`BUGS.md`](BUGS.md).

