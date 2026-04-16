# Cithara – AI Music Generator Platform

Cithara is a web-based platform that enables users to generate AI-powered music, manage personal song libraries, and share content.

## Project Setup

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
   pip install django python-dotenv requests
   ```

4. **Environment Configuration:**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   SUNO_API_TOKEN=your-suno-api-token
   GENERATOR_STRATEGY=mock # or 'suno' for real generation
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access Features:**
   - **Main Page**: `http://127.0.0.1:8000/` (Song Creation)
   - **Library**: `http://127.0.0.1:8000/library/` (Manage your tracks)
   - **Django Admin**: `http://127.0.0.1:8000/admin/`

## Core Features

### 1. AI Music Generation
- Create custom tracks based on title, prompt, genre, mood, and occasion.
- Support for different singer genders (Male, Female, Non-binary).
- Real-time status tracking from 'Generating' to 'Ready'.

### 2. Personal Library Management
- **Advanced Filtering**: Filter your collection by mood, genre, occasion, status, or voice gender.
- **Dynamic Sorting**: Organise by newest/oldest or alphabetically.
- **Search**: Fast text-based search for track titles.
- **Playlist Management**: Create custom playlists and organize your songs using a drag-and-drop-like interface or simple selectors.

### 3. Public Sharing
- **Secure Sharing**: Each song has a unique UUID `share_token`.
- **Standalone Share Page**: Share songs via a dedicated minimalist link that features only the music and its metadata, perfect for a clean listening experience.
- **Direct Link**: Quickly copy share links from the library or creation result.

## Domain Entities

- **User**: Standard Django user.
- **Playlist**: Groups songs for a user.
- **Song**: Stores AI generation parameters, status, and audio references.
    - `audio_format`: (MP3/M4A).
    - `reference_url`: Optional reference song URL for inspiration.
    - `singer_gender`: Inclusivity choices.
    - `share_token`: (UUID) for secure public URLs.

*Link of vidéo : https://drive.google.com/file/d/1YsP_fViyEK5ehwbaKoeYi_uxygHL6xJq/view?usp=sharing*
