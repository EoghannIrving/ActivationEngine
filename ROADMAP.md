---
title: "Modular Roadmap – Activation Engine and Ecosystem"
status: "active"
area: "design"
effort: "medium"
energy_cost: 3
last_reviewed: 2025-08-01
tags: ["#roadmap", "#activation_engine", "#mindloom", "#echo_journal"]
---

# 🧭 Modular Roadmap: Activation Engine Ecosystem

## 🧱 Activation Engine (Core Logic)
The centralized logic layer responsible for low-friction, context-aware decision making across apps.

### ✅ Responsibilities
- Contextual tag generation from mood, energy, time, media
- Task filtering based on user energy/executive cost
- Task scoring and basic ranking
- Configurable scoring rules via `weights.yaml`
- Input model: `UserState`, `TaskList`, `Context`
- Output: Ranked tasks or contextual tags
- FastAPI endpoints: `/get-tags`, `/rank-tasks`
- Dockerized for reuse

---

## 🗂️ MindLoom Responsibilities
Neurodivergent-friendly project and task management tool.

### ✅ Owns
- Task and project storage (YAML, Obsidian parsing, etc.)
- Task completion, streaks, rejection tracking
- Task review, snoozing, priority rules
- GPT-based final task phrasing and rationale
- User interaction history and learning loop

### 🔁 Uses Engine For
- Energy/contextual task pre-filtering
- Executive function–aware candidate generation
- Final ranking decisions via GPT based on engine output

---

## 📓 Echo Journal Responsibilities
Journaling app for anchoring emotion, memory, and reflection in daily life.

### ✅ Owns
- Prompt bank and display logic
- Mood/context tagging for entries
- Memory anchoring (photos, media, music)
- Journal streaks, reviews, exports (e.g. PDF memory cards)
- GPT-enhanced prompt refinement (optional)

### 🔁 Uses Engine For
- Tag generation for selecting relevant prompts
- Mood/context parsing and mood trend inference (future)

---

## 🔄 Shared Interfaces & Utilities
Used by both apps, or any future extensions:

- `POST /get-tags` → for prompt filtering (Echo Journal)
- `POST /rank-tasks` → for ranked task suggestions (MindLoom)
- `weights.yaml` → external scoring configuration
- Optional: export feedback to refine weights or tune models

---

## 📡 Future-Compatible Interfaces
> "One brain, many tools"

Planned consumer surfaces of the Activation Engine:

- Voice assistant (e.g. suggest task via voice input)
- CLI or cron-triggered nudge script
- Mobile PWA for journaling/task selection
- Daily email or push notification w/ top suggestion

---

## 🧠 Guiding Principle
Keep the Activation Engine a **stateless, reusable cognitive logic module**, while letting Echo Journal and MindLoom retain:
- User-specific state
- Final phrasing and interaction logic
- Logging and memory
- App-specific user experience

---

## ✅ Next Priorities
- [x] Refactor FastAPI endpoints to `/get-tags` and `/rank-tasks`
- [x] Add external `weights.yaml` for scoring configuration
- [ ] Add support for returning N top candidates with detailed scores
- [ ] Enable debug mode for scoring explanations
- [ ] Expand context-aware tag matching logic
- [ ] Optional: CLI test harness or API client scaffold

---

