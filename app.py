from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import string
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db = SQLAlchemy(app)

class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512), nullable=False)
    short_url = db.Column(db.String(6), unique=True, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=True)

def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choice(characters) for _ in range(length))
        if not URLMap.query.filter_by(short_url=short_url).first():
            break
    return short_url

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    length = int(request.form.get('length', 6))  # Default to 6 if not specified
    days_valid = request.form.get('days_valid', None)
    expiration_date = None
    if days_valid:
        expiration_date = datetime.utcnow() + timedelta(days=int(days_valid))

    short_url = generate_short_url(length)
    new_url = URLMap(original_url=original_url, short_url=short_url, expiration_date=expiration_date)
    db.session.add(new_url)
    db.session.commit()
    return jsonify(shortened_url=f"http://{request.host}/{short_url}")

@app.route('/<short_url>')
def redirect_to_original(short_url):
    url_map = URLMap.query.filter_by(short_url=short_url).first()
    if url_map:
        if url_map.expiration_date and url_map.expiration_date < datetime.utcnow():
            db.session.delete(url_map)
            db.session.commit()
            return "URL has expired", 404
        return redirect(url_map.original_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
