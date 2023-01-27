import os
import secrets
import PIL
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, jsonify, json
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, VehicleForm, CorporateRegistrationForm
from .models import User, Profession, Country, Province, City, Districts, Town, Areas, Uservehicle, Vehiclemake, Vehiclemakemodel, Vehiclebodytype, Vehiclemodelyear
from werkzeug.security import generate_password_hash, check_password_hash
from website import db, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user. is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(
            f'Your account has been created! Your are now able to login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', title='Register', form=form)


def save_picture(form_picture):
    rendon_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = rendon_hex + f_ext
    picture_path = os.path.join(
        auth.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    # form_picture.save(picture_path)

    return picture_fn


@auth.route('/coregister', methods=['GET', 'POST'])
@login_required
def coregister():
    form = CorporateRegistrationForm()
    if form.validate_on_submit():
        if form.img_ntn.data:
            imag_ntn = save_picture(form.img_ntn.data)
            current_user.img_ntn = imag_ntn

        if form.img_logo.data:
            imag_logo = save_picture(form.img_logo.data)
            current_user.img_logo = imag_logo
        current_user.company_name = form.company_name.data
        current_user.mobile = form.mobile.data
        current_user.webpage = form.webpage.data
        current_user.level = "Corporate"
        db.session.commit()
        flash(
            f'Your request has been submited! We well contact you with in 3 working day.', 'success')
        return redirect(url_for('auth.coregister'))
    elif request.method == 'GET':
        form.company_name.data = current_user.company_name
        form.mobile.data = current_user.mobile
        form.webpage.data = current_user.webpage
        form.img_ntn.data = current_user.img_ntn
        form.img_logo.data = current_user.img_logo

    image_ntn = url_for(
        'static', filename='profile_pics/' + current_user.img_ntn)

    image_logo = url_for(
        'static', filename='profile_pics/' + current_user.img_logo)
    return render_template('rig_corporate.html', title='Corporate Register', image_ntn=image_ntn, image_logo=image_logo, form=form, legend='Corporate Registration Form')


@ auth.route('/account', methods=['GET', 'POST'])
@ login_required
def account():
    form = UpdateAccountForm()
    form.profession.choices = [(profession.id, profession.profession)
                               for profession in Profession.query.all()]
    form.country.choices = [(country.id, country.country)
                            for country in Country.query.all()]
    form.province.choices = [(province.id, province.province)
                             for province in Province.query.all()]
    form.city.choices = [(city.id, city.city) for city in City.query.all()]
    form.districts.choices = [(districts.id, districts.district)
                              for districts in Districts.query.all()]
    form.town.choices = [(town.id, town.town) for town in Town.query.all()]
    form.area.choices = [(area.id, area.area) for area in Areas.query.all()]

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.fname = form.fname.data
        current_user.mname = form.mname.data
        current_user.lname = form.lname.data
        current_user.profession = form.profession.data
        current_user.cnic_num = form.cnic_num.data
        current_user.phone_num = form.phone_num.data
        current_user.country = form.country.data
        current_user.state = form.province.data
        current_user.city = form.city.data
        current_user.districts = form.districts.data
        current_user.town = form.town.data
        current_user.area = form.area.data
        current_user.house = form.house.data
        current_user.street = form.street.data
        db.session.commit()
        flash(
            f'Your account has been updated.', 'success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.fname.data = current_user.fname
        form.mname.data = current_user.mname
        form.lname.data = current_user.lname
        form.profession.data = current_user.profession
        form.cnic_num.data = current_user.cnic_num
        form.phone_num.data = current_user.phone_num
        form.country.data = current_user.country
        form.province.data = current_user.state
        form.city.data = current_user.city
        form.districts.data = current_user.districts
        form.town.data = current_user.town
        form.area.data = current_user.area
        form.house.data = current_user.house
        form.street.data = current_user.street

    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@ auth.route('/province/<get_country_id>')
def provincebycountry(get_country_id):
    province_data = Province.query.filter_by(country_id=get_country_id).all()
    provinceArray = []
    for province in province_data:
        provinceObj = {}
        provinceObj['id'] = province.id
        provinceObj['province'] = province.province
        provinceArray.append(provinceObj)
    return jsonify({'provincelist': provinceArray})


@ auth.route('/city/<get_province>')
def citybystate(get_province):
    city_data = City.query.filter_by(provinces=get_province).all()
    cityArray = []
    for city in city_data:
        cityObj = {}
        cityObj['id'] = city.id
        cityObj['city'] = city.city
        cityArray.append(cityObj)

    return jsonify({'citylist': cityArray})


@ auth.route('/district/<get_city_id>')
def districtbycity(get_city_id):
    district_data = Districts.query.filter_by(cities=get_city_id).all()
    districtArray = []
    for district in district_data:
        districtObj = {}
        districtObj['id'] = district.id
        districtObj['district'] = district.district
        districtArray.append(districtObj)

    return jsonify({'districtlist': districtArray})


@ auth.route('/town/<get_district_id>')
def townbydistrict(get_district_id):
    town_data = Town.query.filter_by(district=get_district_id).all()
    townArray = []
    for town in town_data:
        townObj = {}
        townObj['id'] = town.id
        townObj['town'] = town.town
        townArray.append(townObj)

    return jsonify({'townlist': townArray})


@ auth.route('/area/<get_town_id>')
def areabytown(get_town_id):
    area_data = Areas.query.filter_by(towns=get_town_id).all()
    areaArray = []
    for area in area_data:
        areaObj = {}
        areaObj['id'] = area.id
        areaObj['area'] = area.area
        areaArray.append(areaObj)

    return jsonify({'arealist': areaArray})


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@kwickfit.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('reset_token', token=token, external=True)}
    if you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)


@ auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@ auth.route('/reset_password<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is invalid or expire token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        user.password = hashed_password
        db.session.commit()
        flash(
            f'Your password has been updated! Your are now able to login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_token.html', title='Reset Password', form=form)


@ auth.route('/dashboard')
@ login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')


