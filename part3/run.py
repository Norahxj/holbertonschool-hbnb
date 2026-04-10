from flask import send_from_directory
from app import create_app, db
import os

app = create_app()

with app.app_context():
    db.create_all()

FRONTEND_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'part4')
)

@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory(FRONTEND_FOLDER, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
