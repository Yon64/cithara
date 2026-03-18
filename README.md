# Cithara – AI Music Generator Platform

Cithara is a web-based platform that enables users to generate AI-powered music, manage personal song libraries, and share content.

## Exercise 3: Implementing the Domain Layer Using Django

This repository contains the implementation of the domain layer for Cithara, focusing on correct domain modeling and persistence using Django ORM.

### Project Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Yon64/cithara.git
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

- **User**: Standard Django user.
- **Playlist**: Groups songs for a user.
- **Song**: Stores AI generation parameters, status, and audio references.
    - **New Fields**: `reference_url`, `audio_format` (MP3/M4A), and `share_token` (UUID).

### CRUD Evidence

As required by Exercise 3, here is a summary of the domain entities supported by CRUD operations via Django Admin:

1. **Create**: New songs can be created with AI parameters (mood, occasion, etc.).
2. **Read**: Songs can be listed and filtered by status, mood, and format.
3. **Update**: Any field can be edited; `share_token` is generated automatically and remains read-only.
4. **Delete**: Songs and playlists can be removed from the database.

*Note: Screenshots or a demo video should be added here for final submission.*
