from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import yaml
import os

app = FastAPI()

# --- Models ---
class Context(BaseModel):
    weather: Optional[str]
    music: Optional[str]
    location: Optional[str]
    last_activity: Optional[str]
    projects_active: Optional[List[str]] = []
    time_of_day: Optional[str]

class UserState(BaseModel):
    energy: int  # 1–5
    mood: Optional[str]
    context: Optional[Context]

class Task(BaseModel):
    name: str
    project: str
    effort: Optional[str]
    energy_cost: Optional[int] = 3
    executive_cost: Optional[int] = 3
    tags: Optional[List[str]] = []

class TaskRequest(BaseModel):
    user_state: UserState
    tasks: List[Task]


class PromptCategoryRequest(BaseModel):
    mood: Optional[str]
    energy: int  # 1-5
    categories: List[str]

# --- Load weights ---
def load_weights():
    try:
        with open("weights.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {
            "energy_weight": 1.0,
            "executive_cost_weight": 1.5,
            "context_match_weight": 0.5,
            "preferred_tags": {}
        }

weights = load_weights()

# --- Engine ---
class ActivationEngine:
    def get_tags(self, user_state: UserState) -> List[str]:
        tags = []

        if user_state.energy <= 2:
            tags.append("low-energy")
        elif user_state.energy >= 4:
            tags.append("high-energy")

        if user_state.mood:
            tags.append(user_state.mood.lower())

        ctx = user_state.context
        if ctx:
            if ctx.weather:
                tags.append(ctx.weather.lower())
            if ctx.music:
                tags.append(ctx.music.lower())
            if ctx.time_of_day:
                tags.append(ctx.time_of_day.lower())
            if ctx.location:
                tags.append(ctx.location.lower())
            if ctx.last_activity:
                tags.append("recent-activity")

        return list(set(tags))

    def rank_tasks(self, user_state: UserState, tasks: List[Task]) -> List[dict]:
        ranked = []
        for task in tasks:
            energy_diff = abs((task.energy_cost or 3) - user_state.energy)
            score = (
                weights["energy_weight"] * (5 - energy_diff) +
                weights["executive_cost_weight"] * (5 - (task.executive_cost or 3))
            )
            ranked.append({
                "task": task.name,
                "project": task.project,
                "score": round(score, 2),
                "reason": "Ranked using energy and executive fit"
            })
        return sorted(ranked, key=lambda x: -x["score"])

    def pick_prompt_category(self, mood: Optional[str], energy: int, categories: List[str]) -> Optional[str]:
        """Select a prompt category using simple mood and energy heuristics."""
        if not categories:
            return None

        mood_lc = mood.lower() if mood else None
        categories_lc = [c.lower() for c in categories]

        # First try to match the provided mood directly
        if mood_lc:
            for idx, cat in enumerate(categories_lc):
                if mood_lc in cat:
                    return categories[idx]

        # Next fall back to energy-based keywords
        if energy <= 2:
            low_keywords = ["low", "rest", "relax", "chill", "calm"]
            for idx, cat in enumerate(categories_lc):
                if any(k in cat for k in low_keywords):
                    return categories[idx]
        elif energy >= 4:
            high_keywords = ["high", "active", "intense", "workout", "party"]
            for idx, cat in enumerate(categories_lc):
                if any(k in cat for k in high_keywords):
                    return categories[idx]

        # If no match was found, return the first category
        return categories[0]

engine = ActivationEngine()

# --- Endpoints ---
@app.post("/get-tags")
def get_tags(user_state: UserState):
    try:
        tags = engine.get_tags(user_state)
        return {"tags": tags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rank-tasks")
def rank_tasks(task_request: TaskRequest):
    try:
        ranked = engine.rank_tasks(task_request.user_state, task_request.tasks)
        return {"candidates": ranked}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/prompt-category")
def prompt_category(req: PromptCategoryRequest):
    try:
        category = engine.pick_prompt_category(req.mood, req.energy, req.categories)
        return {"category": category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
