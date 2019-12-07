from pymongo import TEXT
from app.connect_database import Connect

Connect.get_connection().tags.create_index([('name', TEXT), ('category', TEXT)], default_language='english')
Connect.get_connection().Gallery.create_index([('title', TEXT), ('japan_title', TEXT)], default_language='english')