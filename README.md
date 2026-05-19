# GameStatisticBot 🎮📊

> ⚠️ **Project Note:** This repository is a **Demo/MVP version** of a larger modular analytical platform. It has been refactored and extracted from a private workspace to demonstrate async application design, web scraping/automation, and data transformation patterns, while completely stripping out proprietary credentials.

An asynchronous Python-based Discord bot and data aggregation tool designed to fetch, parse, and monitor player profiles and market statistics from various gaming ecosystems (including Albion Online, Dota 2, and WoW).

## 🚀 Key Features & Demo Scope
* **Data Ingestion & Extraction:** Implements data fetching from public endpoints, game APIs, and custom parsing logic to extract valuable insights.
* **Browser Automation & Scraping:** Features background automation elements (originally tested with Selenium) to handle dynamic web content delivery where standard HTTP requests fall short.
* **Asynchronous Architecture:** Built on top of `discord.py` (v2.0+) using native `asyncio` loops to handle asynchronous command trees (`app_commands`), parallel requests, and rapid I/O operations without blocking the core application.
* **Data Normalization & Filtering:** Includes custom text/string processors that decompose complex item modifications (e.g., parsing strings like `T7_BAG@2`) and execute threshold-based analytics (e.g., filtering cross-market items with $\ge 30\%$ profit margins).
* **Storage-Ready Mapping:** Uses locally managed analytical states (with a layout easily scalable to containerized PostgreSQL/Supabase instances via Docker).

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** discord.py (Modern application commands & slash tree setup)
* **Web Automation & Ingestion:** Requests, JSON Parsing, Selenium (Browser Automation)
* **Database / State:** SQLite / In-memory data structures (Production-ready for PostgreSQL migrations)
* **Visual Formatting:** Colorama (For structured pipeline terminal monitoring)

## 📈 Pipeline Alignment
The core logic of this bot reflects a structured **Download ➡️ Parse ➡️ Filter ➡️ Present** pipeline. For example, the `/prices` command handles a bulk network payload, transforms nested JSON values, filters out incomplete/corrupted records, and dynamically streams the normalized analytical report back to the user via structured Discord File buffers.

---
*Developed as a functional demonstration focusing on robust async data parsing, string normalization, and service automation.*
