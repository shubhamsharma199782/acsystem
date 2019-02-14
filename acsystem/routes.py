from flask import render_template, url_for, flash, redirect, abort
from acsystem import app, bcrypt, db
from acsystem.forms import LoginForm, RegisterForm, CompanyForm
from acsystem.models import User, Company, Countries, States
from flask_login import login_user, current_user, login_required, logout_user

activecomp="click dashboard"

@app.route("/")
def home():
    return render_template("home.html", title = "home")

@app.route("/about")
def about():
    return render_template("about.html", title = "about")

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        print(form.email.data)
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You loged in Successfully!","success")
            return redirect(url_for('dashboard'))
        else:
            flash("Login Unsuccessful!", "warning")
    return render_template("login.html", title = "login", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(form.firstname.data, form.lastname.data, form.email.data, 9876543210, hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your Account for {form.firstname.data} has Been Created Successfully!","success")
        return redirect(url_for('login'))
    return render_template('register.html', title = "register", form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    global activecomp
    activecomp = Company.query.get(current_user.activecompany)
    return render_template("dashboard.html", title="Dashboard", activecomp=activecomp)

@app.route("/companies")
@login_required
def companies():
    companies = Company.query.filter_by(owner = current_user).order_by(Company.datecreated.desc())
    return render_template("companies.html", title="Company", companies = companies, activecomp = activecomp)

@app.route("/addcompany", methods=['GET','POST'])
@login_required
def addcompany():
    companies = Company.query.filter_by(owner = current_user).all()
    if len(companies)>=5:
        flash(f"You have reached the maximum limit for creating companies Under this account!","info")
        return redirect(url_for('companies'))
    if len(companies)>=4:
        flash(f"You can only create 5 companies Under this account!","warning")
    form = CompanyForm()
    form.country.choices+= [(str(country.name), country.name) for country in Countries.query.all()]
    if form.validate_on_submit():
        company = Company(companyname = form.name.data, mailingname = form.mailingname.data
                    , address = form.address.data, country = form.country.data, state = form.state.data
                    , pin = form.pin.data, email = form.email.data, phoneno = form.phone.data
                    , website = form.website.data, gstno = form.gstno.data, description = form.description.data, owner = current_user)
        db.session.add(company)
        db.session.commit()
        flash(f"Company Created Succefully!","success")
        return redirect(url_for('companies'))
    return render_template("addcompany.html", title="Company", form=form, activecomp=activecomp)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/activate/<int:compid>')
def activatecompany(compid):
    comp = Company.query.get(compid)
    if comp in current_user.companies:
        current_user.activecompany = compid
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
        abort(403)

@app.route('/company/<int:compid>/deletecompany', methods=["POST"])
@login_required
def deletecompany(compid):
    company = Company.query.get_or_404(compid)
    if company.owner != current_user:
        abort(403)
    db.session.delete(company)
    db.session.commit()
    flash(f"Company {company.companyname} deleted Successfully","success")
    return redirect(url_for('dashboard'))




# @app.route("/states/<ctry>")
# def state(ctry):
#     print("inside state route") 
#     relatedstates = States.query.filter_by(country = ctry).all()
#     statearray =[]
#     for state in relatedstates:
#         stateobj ={}
#         stateobj['id'] = str(state.id)
#         stateobj['name']= str(state.name)
#         statearray.append(stateobj)
#     return jsonify({'states': statearray})

