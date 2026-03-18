# Cithara – AI Music Generator Platform

Cithara is a web-based platform that enables users to generate AI-powered music, manage personal song libraries, and share content.

## Exercise 3: Implementing the Domain Layer Using Django

This repository contains the implementation of the domain layer for Cithara, focusing on correct domain modeling and persistence using Django ORM.

### Project Setup

1. **Clone the repository:**
   ```bash
   git clone [repository_url](https://github.com/Yon64/cithara.git)
   cd cithara
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access Django Admin:**
   - Create a superuser: `python manage.py createsuperuser`
   - Go to `http://127.0.0.1:8000/admin/`

### Domain Entities

- **User**: Standard Django user (can be extended).
- **Playlist**: Groups songs for a user.
- **Song**: Stores AI generation parameters, status, and audio references.
