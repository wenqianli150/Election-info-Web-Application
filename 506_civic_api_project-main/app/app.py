#!/usr/local/bin/python3

from email_validator import validate_email, EmailNotValidError
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_wtf import FlaskForm, form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, length
from civic import find_elections, find_reps, validateAddress, find_directions
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from models import db, login, UserModel



class loginForm(FlaskForm):

    email = StringField('Email', [InputRequired(), Length(min=6, max=50)])
    username = StringField('Username', [InputRequired(), Length(min=6, max=50)])
    password = PasswordField(label='Password',validators=[DataRequired(), Length(min=6, max=16)])
    submit = SubmitField(label='Login')

class RegisterForm(FlaskForm):

    email = StringField('Email', [InputRequired(), length(max=50)])
    username = StringField('Username', [InputRequired(), length(max=50)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=16)])
    address = StringField('Address', [InputRequired()])
    submit = SubmitField(label='Register')

class ChangeAddressForm(FlaskForm):
    address = StringField('Address', [InputRequired()])
    submit = SubmitField(label='Update')


app=Flask(__name__)
app.secret_key='a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
login.login_view = 'login'


@app.before_first_request
def create_table():
    db.create_all()
    
@app.route('/')
def baseSite():
    return redirect("/login")
    
@app.route('/civic')
@login_required
def civic():
    address = current_user.address
    repdata=find_reps(address)
    officials = repdata["officials"]
    offices = repdata["offices"]
    election_response = find_elections(address)
    return render_template('civic.html', address=address, election_data=find_directions(election_response, address), officials=officials, offices=offices)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    try:
        if form.validate_on_submit():
            if request.method == "POST":
                username=request.form["username"]
                pw=request.form["password"]
                email=request.form["email"]
                address=request.form["address"]
                valid_address=validateAddress(address)
                user = UserModel.query.filter_by(username = username).first()
                email_address = UserModel.query.filter_by(email = email).first()
                try:
                    valid = validate_email(email)
                except:
                    flash('Invalid email address.')
                    return render_template('register.html', form=form)
                if user:
                    flash('Username already in use.')
                    return render_template('register.html', form=form)
                elif email_address:
                    flash('Email already in use.')
                    return render_template('register.html', form=form)
                elif len(valid_address['results'])==0:
                    flash('Invalid address.')
                    return render_template('register.html', form=form)
                else:
                    new_user = UserModel(username=username)
                    new_user.set_password(pw)
                    new_user.email=email
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect('/login')
            else:
                return render_template('register.html', form=form)
        else:
            return render_template('register.html', form=form)
    except:
        return render_template('error.html', form=form)

@app.route('/login', methods=["POST", "GET"])
def login():
    form = loginForm()
    try:
        if current_user.is_authenticated:
            return redirect('/civic')
        if request.method == "POST":
            username = request.form["username"]
            pw = request.form["password"]
            user = UserModel.query.filter_by(username=username).first()
            if user and user.check_password(pw):
                login_user(user)
                return redirect('/civic')
            else:
                flash("Invalid Login Details")
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)
    except:
        return render_template('error.html', form=form)

@app.route('/change_address', methods=['GET', 'POST'])
def change_address():
    if current_user.is_authenticated == False:
        return redirect('/login')
    form=ChangeAddressForm()
    if request.method == "POST":
        address = request.form["address"]
        response = validateAddress(address)
        validaddress = False
        for item in response['results']:
            if(item['geometry']['location_type']!= 'APPROXIMATE'):
                current_user.address = address
                db.session.commit()
                validaddress = True
                return redirect('/civic')
        if(not validaddress):
               return render_template('change_address.html', form=form)
    else:
        return render_template('change_address.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)




