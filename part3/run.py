from flask import send_from_directory
from app import create_app, db
import os

app = create_app()

# Create DB tables
with app.app_context():
    db.create_all()

# Serve frontend files from part4/frontend
FRONTEND_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'part4', 'frontend')

@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory(FRONTEND_FOLDER, path)

@app.route('/')
def index():
    return send_from_directory(FRONTEND_FOLDER, 'login.html')

if __name__ == '__main__':
    app.run(debug=True)
