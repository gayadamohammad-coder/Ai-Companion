# AI Companion

A personal AI companion built to become a real Jarvis — a long-term mentor, code teacher, and productivity partner. Not a tutorial project. Not a university assignment. A real software engineering build, learned and shipped one feature at a time.

## Vision

The end goal is an AI system that knows my goals, tracks my learning, reviews my code, explains my mistakes, and eventually sees my screen and lives inside my editor. Built local-first using Ollama, with a real product-style web interface — not a chatbot demo.

## The journey so far

This project started as a basic terminal chatbot and grew into a Flask web app with persistent memory, a live dashboard, and a working code-review assistant called Jarvis. Along the way the codebase was refactored from loose functions into a proper `DatabaseManager` class, config and secrets were separated out of code, and the chat system was rebuilt to actually understand conversation structure instead of dumping raw text at the model.

What I learned building this: SQLite and database design, Python OOP (classes, `self`, constructors), Flask routing and templates, connecting a frontend to a real backend, JavaScript fetch and async/await, DOM manipulation, CodeMirror integration for a real code editor experience, and how to structure a growing codebase so it doesn't collapse under its own weight.

## Current architecture

- **Language:** Python
- **Backend:** Flask
- **Database:** SQLite, accessed through a single `DatabaseManager` class
- **Local AI:** Ollama running Qwen models (currently `qwen2.5:1.5b` for speed on lower-end hardware)
- **Frontend:** Server-rendered Jinja templates plus vanilla JavaScript, dark terminal-inspired UI
- **Config:** `.env` + `config.py` for secrets and settings, never hardcoded paths

## Features shipped

**Foundation**
- SQLite database with a clean `DatabaseManager` class (memories, goals, chat history, learning topics)
- Centralized config via `.env` and `config.py`
- Flask website with a live dashboard pulling real data from the database

**Local AI**
- Ollama integration, fully local, no API costs
- Dynamic system prompts that inject saved memories and goals into every conversation, so Jarvis actually knows who he's talking to

**Code Teacher (in progress)**
- Persistent chat history saved to the database, survives page refresh
- A real popup code editor (CodeMirror, dark theme, Python syntax highlighting) for pasting code to review, instead of a plain text box
- File upload — attach a `.py`, `.html`, `.css`, or `.js` file directly and ask Jarvis to explain it
- Stop/cancel button to abort an in-flight response
- Dark, terminal-inspired UI redesign across dashboard and chat

## Roadmap

**Phase 1 — Foundation** ✅ done
SQLite, memory system, goal system, Flask website

**Phase 2 — Local AI** ✅ done
Ollama integration, Qwen models, fully local-first, no cloud dependency

**Phase 3 — Code Teacher** 🔄 in progress
Code review, debugging help, file-based code explanation, learning topic tracking, personalized next-steps

**Phase 4 — Developer Assistant** ⏳ next
VS Code integration, file awareness, project awareness, context-aware coding assistance directly inside the editor

**Phase 5 — Jarvis** ⏳ future
Voice interaction, screen awareness, agent-style autonomous assistance, long-term memory that compounds over time

## Software engineering goals

This project is also where I'm learning to write professional code, not just working code. The long-term direction is toward proper OOP, SOLID principles, separation of concerns, and a structure that looks like a real product codebase rather than one giant script. Patterns like Repository, Service Layer, and Dependency Injection are on the list to explore as the codebase grows.

## Why local-first

No API costs, no quotas, full ownership of the data and the model, better privacy, and long-term sustainability — the AI Companion should keep working even with zero internet connection and zero recurring cost.

## Status

Actively in development. This README is updated as new phases ship.
