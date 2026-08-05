# CrillX Backend

CrillX Backend is a Django-based REST API project configured with PostgreSQL and JWT Authentication.

---

## 🚀 Features

- **Framework:** Django 6.0 + Django REST Framework
- **Database:** PostgreSQL (configured via environment variables)
- **Authentication:** SimpleJWT (JSON Web Tokens)
- **File Storage:** AWS S3 (via Boto3 for direct frontend presigned uploads)
- **Environment Management:** `python-dotenv` for secure environment variable loading

---

## 🛠️ Prerequisites

- Python 3.10+
- PostgreSQL server installed and running
- Virtual environment (`env` or `venv`)

---

## 📋 Setup & Installation

### 1. Environment Setup

Ensure your virtual environment is activated, then install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables (`.env`)

Create a `.env` file in the root directory (same folder as `manage.py`):

```env
DB_NAME=CrillX
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# AWS S3 Settings (Required for Presigned URLs)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_S3_REGION_NAME=your_region (e.g., us-east-1)
```

### 3. Database Migrations

Apply the database migrations to set up schema tables in your PostgreSQL database:

```bash
python manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

## 🏃 Running the Server

Start the Django development server:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## 📁 Project Structure

```
CrillX/
├── CrillX/             # Core project configuration (settings, urls, wsgi)
├── users/              # App handling user models and authentication
├── .env                # Environment variables (DB credentials, secrets)
├── .gitignore          # Git ignore file
├── manage.py           # Django CLI management script
├── README.md           # Project documentation
└── requirements.txt    # Project Python dependencies
```
