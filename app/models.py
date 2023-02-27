from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from collections import OrderedDict


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)  # string type field with maximum 64 characters
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    current_streak = db.Column(db.Integer, default=0)
    best_streak = db.Column(db.Integer, default=0)
    tracking = db.relationship("StreakEntry", backref="user", lazy="dynamic")
    sos_med1 = db.Column(db.Integer, db.ForeignKey("lib_med.id"))
    sos_med2 = db.Column(db.Integer, db.ForeignKey("lib_med.id"))
    sos_med3 = db.Column(db.Integer, db.ForeignKey("lib_med.id"))
    favorites = db.relationship("MedFavorite", foreign_keys="MedFavorite.user_id", backref="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

        # https://stackoverflow.com/a/52679456 accessed 29th January 2023

    def favorite_med(self, med):
        if not self.has_favorited_med(med):
            favorite = MedFavorite(user_id=self.id, med_id=med.id)
            db.session.add(favorite)

    def unfavorite_med(self, med):
        if self.has_favorited_med(med):
            MedFavorite.query.filter(MedFavorite.user_id == self.id, MedFavorite.med_id == med.id).delete()

    def has_favorited_med(self, med):
        return MedFavorite.query.filter(
            MedFavorite.user_id == self.id,
            MedFavorite.med_id == med.id).count() > 0

    def __repr__(self):
        # """Returns instance of string to represent User object."""
        return "<User {}>".format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class MedFavorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    med_id = db.Column(db.Integer, db.ForeignKey("lib_med.id"))

    def __init__(self, user_id, med_id):
        self.user_id = user_id
        self.med_id = med_id

    def __repr__(self):
        return "<{}>".format(self.id)


class StreakEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    streak_tick = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(50))
    cat_description = db.Column(db.Text)
    cat_img_url = db.Column(db.String(50))
    cat_img_alt_text = db.Column(db.Text)
    meditations = db.relationship("LibMed", backref="categories", lazy="dynamic")

    def __init__(self, id, cat_name, meditations, cat_img_url):
        self.id = id
        self.cat_name = cat_name
        self.cat_img_url = cat_img_url
        self.meditations = meditations

    def __repr__(self):
        return f'{self.id}'


class LibMed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    category = db.Column(db.Integer, db.ForeignKey("categories.id"))
    time = db.Column(db.Float)
    cover_url = db.Column(db.Text)
    cover_alt_text = db.Column(db.Text)
    mp3_url = db.Column(db.Text)
    description = db.Column(db.Text)
    sos_med1_entry = db.relationship("User", foreign_keys="User.sos_med1",
                                     lazy="dynamic")  # https://stackoverflow.com/a/18854791 accessed 28th January 2023
    sos_med2_entry = db.relationship("User", foreign_keys="User.sos_med2", lazy="dynamic")
    sos_med3_entry = db.relationship("User", foreign_keys="User.sos_med3", lazy="dynamic")
    favorites = db.relationship("MedFavorite", foreign_keys="MedFavorite.med_id", lazy="dynamic")

    def __init__(self, title, category, cover_url, time):
        self.title = title
        self.category = category
        self.cover_url = cover_url
        self.time = time

    def __repr__(self):
        return str(self.cover_url)
