# Backend README

1. Create and activate virtual environment:
   python3 -m venv venv
   source venv/bin/activate

2. Install requirements:
   pip install -r requirements.txt

3. Copy .env.example to .env and set DB credentials.

4. Run app:
   python app.py

Notes:
- Ensure MySQL DB is created using database/create_tables.sql
- NLTK data will download at first run
