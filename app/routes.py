from flask import Blueprint, request, redirect, jsonify
from datetime import datetime, timedelta
import string, random
from .models import URLMapping
from .extensions import db

main = Blueprint('main', __name__)

def generate_short_url(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choice(characters) for _ in range(length))
        if not URLMapping.query.filter_by(short_url=short_url).first():
            break
    return short_url

@main.route('/shorten', methods=['POST'])
def shorten_url():
    if request.is_json:
        data = request.get_json()
        original_url = data.get('url')
        length = int(data.get('length', 6))
        days_valid = data.get('days_valid', None)
    else:
        original_url = request.form['url']
        length = int(request.form.get('length', 6))
        days_valid = request.form.get('days_valid', None)
    
    expiration_date = None
    if days_valid:
        expiration_date = datetime.utcnow() + timedelta(days=int(days_valid))

    short_url = generate_short_url(length)
    new_url = URLMapping(original_url=original_url, short_url=short_url, expiration_date=expiration_date)
    db.session.add(new_url)
    db.session.commit()
    return jsonify(shortened_url=f"http://{request.host}/{short_url}")

@main.route('/<short_url>')
def redirect_to_original(short_url):
    url_map = URLMapping.query.filter_by(short_url=short_url).first()
    if url_map:
        if url_map.expiration_date and url_map.expiration_date < datetime.utcnow():
            url_map.is_active = False
            db.session.commit()
            return "URL has expired", 404
        url_map.clicks += 1
        db.session.commit()
        return redirect(url_map.original_url)
    else:
        return "URL not found", 404
