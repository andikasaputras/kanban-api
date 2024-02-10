from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_session import Session


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
sess = Session()


def init_db(app):
    db.init_app(app)
    sess.init_app(app)
    with app.app_context():
        db.create_all()
    return db
