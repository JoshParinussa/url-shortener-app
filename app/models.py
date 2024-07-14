from .extensions import db

class URLMapping(db.Model):
    __tablename__ = 'url_mapping'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512), nullable=False)
    short_url = db.Column(db.String(6), unique=True, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=True)
    clicks = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
