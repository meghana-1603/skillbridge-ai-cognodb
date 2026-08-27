# 🕸️ SkillBridge AI

A graph-powered career networking platform built using **CognoDB (Neo4j-compatible Graph Database)** and **Streamlit**.

## Overview

SkillBridge AI helps users discover mentors, explore companies, and understand the relationships between people, skills, companies, and courses using graph traversal.

## Why a Graph Database?

Traditional relational databases require multiple joins to answer relationship-heavy questions.

A graph database models these connections naturally.

Example multi-hop traversal:

User → Skill ← User

This enables mentor recommendations based on shared skills with a simple graph query.

## Graph Data Model

* **User**
* **Skill**
* **Company**
* **Course**

Relationships:

* `HAS_SKILL`
* `WORKS_AT`
* `REQUIRES_SKILL`
* `TEACHES`

## Features

* User Explorer
* Mentor Recommendations
* Company Explorer
* Required Skills
* Live Database Statistics

## Tech Stack

* Python
* Streamlit
* CognoDB Cloud
* Neo4j Python Driver
* Cypher

## Project Structure

```text
skillbridge-ai/
│
├── app.py
├── seed.py
├── requirements.txt
├── README.md
│
└── db/
    ├── connection.py
    ├── queries.py
    └── __init__.py
```

## Setup

1. Create a CognoDB instance.
2. Create a `.env` file.

```env
DB_URI=your_uri
DB_USER=cognodb
DB_PASSWORD=your_password
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Seed the database.

```bash
python seed.py
```

5. Run the application.

```bash
streamlit run app.py
```

## Main Cypher Queries

### Mentor Recommendation

Finds users connected through shared skills.

### Company Explorer

Lists employees working at a selected company.

### Required Skills

Shows skills required by each company.

## Author

**Meghana Dasari**

B.Tech – Data Science & Artificial Intelligence
