from Application import db
from Application.models import Posts, Users

db.drop_all()
db.create_all()
