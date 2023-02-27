# import requests
from flask import render_template, redirect, url_for, flash, request
from app import App, db
from app.forms import LoginForm, RegistrationForm, StreakForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, LibMed, Categories, StreakEntry, MedFavorite
import random
from datetime import datetime, timedelta
from werkzeug.urls import url_parse


@App.route("/", methods=["GET", "POST"])
@App.route("/index", methods=["GET", "POST"])
def index():
    # Daily Suggestions Functionality
    d0 = datetime(2023, 1, 3)  # arbitrary date in the past
    d1 = datetime.now()
    delta = d1 - d0
    random.seed(delta.days)  # taken from: https://stackoverflow.com/a/69396228 accessed 24th Jan 2023

    short_meds = LibMed.query.filter(LibMed.time <= 7.0).all()
    random_short_med = random.choice(short_meds)
    mid_meds = LibMed.query.filter(LibMed.time > 7.0, LibMed.time <= 12.0).all()
    random_mid_med = random.choice(mid_meds)
    long_meds = LibMed.query.filter(LibMed.time > 12.0).all()
    random_long_med = random.choice(long_meds)

    # Tracker Entry Functionality
    latest_entry = (
        StreakEntry.query
        .filter(StreakEntry.user_id == current_user.get_id())
        .order_by(StreakEntry.timestamp.desc())
        .first())

    if latest_entry is None:
        # to ensure the function works even when the user is tracking their meditation days for the first time
        form = StreakForm()
        user = User.query.filter_by(id=current_user.get_id()).first()
        if form.validate_on_submit():
            entry = StreakEntry(user_id=current_user.get_id(), streak_tick=form.streak_tick.data)
            user.current_streak = 1
            if user.best_streak < user.current_streak:
                user.best_streak = user.current_streak
            db.session.add(entry)
            db.session.commit()
            flash("Well done!")
            return redirect(url_for("index"))
    else:
        latest_entry_ts = latest_entry.timestamp
        latest_entry_date = latest_entry_ts.date()

        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        time_difference = today - latest_entry_date

        form = StreakForm()
        user = User.query.filter_by(id=current_user.get_id()).first()
        if time_difference.days > 1:
            user.current_streak = 0

        if form.validate_on_submit():
            entry = StreakEntry(user_id=current_user.get_id(), streak_tick=form.streak_tick.data)
            if latest_entry_date == today:
                flash("You already tracked your meditation today.")
                return redirect(url_for("index"))
            elif latest_entry_date == yesterday:
                # entry = StreakEntry(user_id=current_user.get_id(), streak_tick=form.streak_tick.data)
                user.current_streak += 1
                if user.best_streak < user.current_streak:
                    user.best_streak = user.current_streak
                db.session.add(entry)
                db.session.commit()
                flash("Well done!")
                return redirect(url_for("index"))
            else:
                # entry = StreakEntry(user_id=current_user.get_id(), streak_tick=form.streak_tick.data)
                user.current_streak = 1
                if user.best_streak < user.current_streak:
                    user.best_streak = user.current_streak
                db.session.add(entry)
                db.session.commit()
                flash("Well done!")
                return redirect(url_for("index"))
    return render_template("index.html", form=form, user=user, random_short=random_short_med, random_mid=random_mid_med,
                           random_long=random_long_med)

    # return render_template("index.html", title="Home")


@App.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for("index"))
    form = LoginForm()  # in helenas slides called myform
    if form.validate_on_submit():
        user_query = User.query.filter_by(username=form.username.data).first()
        # user = myform.username.data
        if user_query is None or not user_query.check_password(form.password.data):
            flash("Invalid username or password.")
            return redirect(url_for("login"))
        login_user(user_query, remember=form.remember_me.data)
        # return redirect(url_for("index"))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    # return render_template("index.html", title="Home", user=user)
    return render_template("login.html", title="Sign In", form=form)


@App.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@App.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered and logged in.")
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You are now registered.")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)


@App.route("/user/")
def check_user():
    if current_user.is_anonymous:
        flash("Please login or register to access this page.")
        return redirect(url_for("login"))
    return render_template("user.html")


@App.route('/user/<username>')
@login_required
def user(username):
    if username is None:
        return redirect(url_for("login"))
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, query=LibMed.query.all())


@App.route("/categories", methods=["GET", "POST"])
@login_required
def show_categories():
    user = User.query.filter_by(id=current_user.get_id())
    if request.method == "GET":
        return render_template("categories.html", category_overview=Categories.query.all(), user=user)
    return redirect(url_for("show_categories"))


@App.route("/library/<category>", methods=["GET", "POST"])
def library(category):
    selected_category = Categories.query.filter_by(cat_name=category).first()
    meditations = LibMed.query.filter_by(category=selected_category.id).all()
    return render_template("library.html", med_selection=meditations)


@App.route("/favorites")
@login_required
def favorites():
    favorites = LibMed.query.join(MedFavorite).join(User).filter(
        User.id == current_user.get_id())  # https://stackoverflow.com/a/10727852/21118398 accessed 31st January 2023
    for i in favorites:  ##why does this work??
        return render_template("favorite.html", favorites=favorites)
    else:
        flash("You currently haven't favorited any meditations. "
              "Tap the 'favorite' button when listening to a meditation and it will show up here.")
    return render_template("favorite.html", favorites=favorites)


@App.route("/audioplayer/<int:med_id>")
def audioplayer(med_id):
    selected_title = LibMed.query.filter_by(id=med_id).first()
    med = LibMed.query.filter_by(id=med_id).first()
    return render_template("audioplayer.html", selection=selected_title, med=med)


@App.route("/audioplayer/<int:med_id>/<action>")
def favorite_action(med_id, action):
    med = LibMed.query.filter_by(id=med_id).first_or_404()
    if action == "favorite":
        current_user.favorite_med(med)
        db.session.commit()
    if action == "unfavorite":
        current_user.unfavorite_med(med)
        db.session.commit()
    return redirect(request.referrer)


@App.route("/sos", methods=["GET", "POST"])
@login_required
def sos():
    query = User.query.filter_by(id=current_user.get_id()).first()
    sos_med1 = LibMed.query.filter_by(id=query.sos_med1).first()

    sos_med2 = LibMed.query.filter_by(id=query.sos_med2).first()
    sos_med3 = LibMed.query.filter_by(id=query.sos_med3).first()

    if request.method == "POST":
        if "form1_submit" in request.form:  # https://stackoverflow.com/a/58123300 accessed 28th January 2023
            sos_form_entry = int(request.form["sos_meditation1"])
            print(sos_form_entry)
            User.query.filter_by(id=current_user.get_id()).update({"sos_med1": sos_form_entry})
            db.session.commit()
            return redirect(url_for("sos"))
        elif "form2_submit" in request.form:
            sos_form_entry = int(request.form["sos_meditation2"])
            User.query.filter_by(id=current_user.get_id()).update({"sos_med2": sos_form_entry})
            db.session.commit()
            return redirect(url_for("sos"))
        if "form3_submit" in request.form:
            sos_form_entry = int(request.form["sos_meditation3"])
            print(sos_form_entry)
            User.query.filter_by(id=current_user.get_id()).update({"sos_med3": sos_form_entry})
            db.session.commit()
            return redirect(url_for("sos"))
    return render_template("sos.html", all_meditations=LibMed.query.all(), all_categories=Categories.query.all(),
                           user=user, sos_med1=sos_med1, sos_med2=sos_med2, sos_med3=sos_med3)


@App.route("/about", methods=["GET", "POST"])
@login_required
def about():
    return render_template("about.html")
