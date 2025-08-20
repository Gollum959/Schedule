# Schedule — OB Van (PTS) Booking Workflow (Django + Crispy Forms)

> **Legacy notice:** This is a learning project from 2021. The **final working version lives on the `NewCrispyForm` branch**. It is preserved for portfolio/history and is not actively maintained.

Internal tool for **TV broadcast company** to request and manage **OB van (PTS)** bookings. It implements a multi‑step approval flow and keeps an inventory of available equipment.

---

## Features
- **Multi‑step approval workflow** for PTS requests (e.g., editorial → technical → management → scheduled/rejected)
- **Equipment catalog** with availability tracking and conflict checks
- **Request lifecycle & statuses** with comments/attachments
- **Dashboards** for requesters and approvers
- **Admin**: manage equipment, blackout dates, users/roles

---

## Tech Stack (final branch: `NewCrispyForm`)
- **Backend/UI:** Django + **django‑crispy‑forms** + vanilla JavaScript (server‑rendered HTML)
- **Database:** **PostgreSQL** (hosted in the cloud for easier collaboration)
- **Local dev:** can run against the cloud DB or switch to SQLite for quick start

---

## Quick Start (local, simplest)

```bash
# 1) clone and switch to the final branch
git clone https://github.com/Gollum959/Schedule.git
cd Schedule
git checkout NewCrispyForm

# 2) Python env & deps
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt

# 3) settings: choose your DB
# Option A — use cloud PostgreSQL (recommended for parity)
#   Set environment variables used in settings.py (see .env.example below)
# Option B — use SQLite locally
#   Edit DATABASES in schedule/settings.py to use sqlite3

# 4) migrate & create admin
python manage.py migrate
python manage.py createsuperuser

# 5) run
python manage.py runserver
```

---

## Environment variables (if using PostgreSQL)

Create a `.env` (or export variables another way) with values used by `settings.py`:

```dotenv
SECRET_KEY=replace_me
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL (cloud)
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

TIME_ZONE=Europe/Warsaw
```

> If your `settings.py` does not read from env yet, you can either:  
> (a) add `os.getenv(...)` usage there, or (b) edit `DATABASES` directly to point to your cloud Postgres.

---

## Repository layout (final branch)
- `schedule/` — Django project/app code (views, forms, templates)
- `static/` and `templates/` — vanilla JS + server‑rendered HTML

---

## Author
**Aliaksandr Aliakseyeu**
LinkedIn: https://www.linkedin.com/in/aliaksandr-alekseev
