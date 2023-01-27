from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL
from website.models import User, Uservehicle


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError(
                'This username already existies Please choose another one!')

    def validate_email(self, email):

        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError(
                'This eamil already existies Please choose another one!')


class CorporateRegistrationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired()])
    webpage = StringField('Web Site', validators=[
                          DataRequired(), URL(require_tld=False, message='Invalid URL.')])
    img_ntn = FileField('Image NTN', validators=[
                        FileAllowed(['jpg', 'png'])])
    img_logo = FileField('Image Logo', validators=[
        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    fname = StringField('First Name')
    mname = StringField('Medium Name')
    lname = StringField('Last Name', validators=[DataRequired()])
    profession = SelectField('Profession', choices=[])
    cnic_num = StringField('CNIC', validators=[
                           DataRequired(), Length(min=13, max=13)])
    phone_num = StringField('Phone', validators=[
                            DataRequired(), Length(min=11, max=11)])
    country = SelectField('Country', choices=[])
    province = SelectField('Province', choices=[])
    city = SelectField('City', choices=[])
    districts = SelectField('Districts', choices=[])
    town = SelectField('Town', choices=[])
    area = SelectField('Area', choices=[])
    house = StringField('House No', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValidationError(
                    'This username already existies Please choose another one!')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()

            if email:
                raise ValidationError(
                    'This eamil already existies Please choose another one!')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


def UserVehicleQuery():
    return Uservehicle.query.all()


class VehicleForm(FlaskForm):
    regplate = StringField('Reg Plate', validators=[DataRequired()])
    regdate = DateField('Reg Date', format='%Y-%m-%d')
    ownername = StringField('Vehicle Owner Name', validators=[DataRequired()])
    vbodycolor = SelectField('Body Color', choices=[])
    vengineno = StringField('Engine No', validators=[DataRequired()])
    vtaxexpire = DateField('Vehicle Tax Date', format='%Y-%m-%d')
    vinsurance = SelectField('Insurance', choices=[])
    vmake = SelectField('Vehicle Make', choices=[])
    vmakemodel = SelectField('Vehicle Make Model', choices=[])
    vmodelyear = SelectField('Vehicle Model Year', choices=[])
    vbodytype = SelectField('Vehicle Body Type', choices=[])
    submit = SubmitField('Add Vehicle')

    def validate_regplate(self, regplate):

        regplate = Uservehicle.query.filter_by(
            reg_plate=regplate.data).first()

        if regplate:
            raise ValidationError(
                'This vehicle or registration plate number already existies!')

    def validate_vengineno(self, vengineno):

        vengineno = Uservehicle.query.filter_by(
            v_engine_no=vengineno.data).first()

        if vengineno:
            raise ValidationError(
                'This vehicle or engine number already existies!')


class New_OrderForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    svehicle = SelectField('Reg Car', choices=[(UserVehicleQuery)])
    submit = SubmitField('New Order')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class AddProd(FlaskForm):
    item_name = StringField('Name', validators=[DataRequired()])
    item_cond = SelectField('Condition', choices=[])
    list_title = StringField('List Title', validators=[DataRequired()])
    item_brand = SelectField('Brand', choices=[])
    color = SelectField('Color', choices=[])
    pov = SelectField('Placement Of Vehicle', choices=[])
    mpn = StringField('Manufacturer Part Number', validators=[DataRequired()])
    oem_number = StringField('Reference OE/OEM Number',
                             validators=[DataRequired()])
    material = SelectField('Material', choices=[])
    universal_fitment = SelectField(
        'Universal Fitment', choices=["No", "Yes"])
    c_r_o_manufacture = SelectField(
        'Country/Region of Manufacturer', validators=[DataRequired()])
    performance_part = SelectField('Performance Part', choices=["No", "Yes"])
    m_warranty = SelectField('Manufacture Warranty', choices=[
                             "1 Day", "3 Days", "1 Week", "2 Weeks", "1 Month", "3 Months", "6 Months", "1 Year", "2 Years", "3 Years", "5 Years", "Lifetime"])
    item_height = StringField('Item Height', validators=[DataRequired()])
    item_length = StringField('Item Length', validators=[DataRequired()])
    item_width = StringField('Item Width', validators=[DataRequired()])
    item_weight = StringField('Item Weight', validators=[DataRequired()])
    unit_type = SelectField('Unit Type', choices=[
                            "kg", "grm", "ltr", "ml", "m3", "m", "m2", "unit"])
    unit_quantity = StringField('Unit Quantity', validators=[DataRequired()])
    grade = SelectField('Grade', choices=[
                        "New", "New Old Stock", "Refurbished", "Used", "For part or not working"])
    picture_1 = FileField('Picture', validators=[
        FileAllowed(['jpg', 'png'])])
    picture_2 = FileField('Picture', validators=[
        FileAllowed(['jpg', 'png'])])
    picture_3 = FileField('Picture', validators=[
        FileAllowed(['jpg', 'png'])])
    picture_4 = FileField('Picture', validators=[
        FileAllowed(['jpg', 'png'])])
    picture_5 = FileField('Picture', validators=[
        FileAllowed(['jpg', 'png'])])
    picture_6 = FileField('Picture', validators=[
        FileAllowed(['jpg', 'png'])])
    description = TextAreaField('Description', validators=[DataRequired()])
    pricing_type = SelectField('Pricing Type', choices=[
                               "Buy it now", "Acution"])
    acution_type = SelectField('Acution Type', choices=[
                               "1 Day", "2 Days", "3 Days", "5 Days", "7 Days", "10 Days"])
    amount = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add Product')
