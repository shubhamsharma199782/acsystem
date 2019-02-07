from flask import render_template, url_for, flash, redirect, json
from acsystem import app, bcrypt, db
from acsystem.forms import LoginForm, RegisterForm, CompanyForm
from acsystem.models import User
from flask_login import login_user

@app.route("/")
def home():
    return render_template("home.html", title = "home")

@app.route("/about")
def about():
    return render_template("about.html", title = "about")

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"You logined Successfully!","Success")
            return redirect(url_for('home'))
        else:
            flash(f"Login Unsuccessful!", "warning")
    return render_template("login.html", title = "login", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(form.firstname.data, form.lastname.data, form.email.data, 9876543210, hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your Account for {form.firstname.data} has Been Created Successfully!","success")
        return redirect(url_for('dashboard'))
    return render_template('register.html', title = "register", form=form)

@app.route("/dashboard")
def dashboard():
	return render_template("dashboard.html", title="Dashboard")

@app.route("/companies")
def companies():
    return render_template("companies.html", title="Company")

@app.route("/addcompany", methods=['GET','POST'])
def addcompany():
    form = CompanyForm()
    if form.validate_on_submit():
        flash(f"Company Created Succefully!","success")
        return redirect(url_for('companies'))
    return render_template("addcompany.html", title="Company", form=form)


