from datetime import datetime
from flask import abort
from website import db, login_manager, admin
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(50), nullable=False,
                           default='default.png')
    password = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    last_update = db.Column(db.DateTime,
                            default=datetime.utcnow, onupdate=datetime.utcnow)
    fname = db.Column(db.String(20))
    mname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    profession = db.Column(db.Integer, nullable=False)
    cnic_num = db.Column(db.String(13), unique=True)
    phone_num = db.Column(db.String(11), unique=True)
    # Province
    country = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Integer, nullable=False)
    city = db.Column(db.Integer, nullable=False)
    districts = db.Column(db.Integer, nullable=False)
    town = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Integer, nullable=False)
    house = db.Column(db.String(50))
    street = db.Column(db.String(50))
    verification_remarks = db.Column(
        db.String(250), default="User not verified for work on this plateform")
    detail_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    level = db.Column(db.String(50), default="User")
    # Corporate informaton
    company_name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(11), nullable=False)
    img_ntn = db.Column(db.String(50), nullable=False,
                        default='image-not-found.jpg')
    img_logo = db.Column(db.String(50), nullable=False,
                         default='image-not-found.jpg')
    webpage = db.Column(db.String(100), nullable=False)
    leaving_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.utcnow)
    leaving_comint = db.Column(
        db.String(1000), default="Empty", nullable=False)
    # Relationship
    orders = db.relationship('Neworder', backref='author', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    user_vehicles = db.relationship(
        'Uservehicle', backref='user', lazy='dynamic')
    products = db.relationship('Product', backref='user', lazy='dynamic')
    brands = db.relationship('Brand', backref='user', lazy='dynamic')
    itemconds = db.relationship('Itemcond', backref='user', lazy='dynamic')
    colors = db.relationship('Color', backref='user', lazy='dynamic')
    placementofvehicles = db.relationship(
        'Placementofvehicle', backref='user', lazy='dynamic')
    materials = db.relationship(
        'Material', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.image_file}')"


class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        return current_user.is_authenticated

    def not_auth(self):
        return "You're not authorized to use this admin dashboard"


class Neworder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.String(100), nullable=False)
    order_posted_date = db.Column(db.DateTime, nullable=False,
                                  default=datetime.utcnow)
    order_content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_vehicles = db.Column(db.Integer, db.ForeignKey(
        'uservehicle.id'), nullable=False)

    def __repr__(self):
        return f"Neworder('{self.order}', '{self.order_posted_date}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_condition = db.Column(db.String(30), nullable=False)
    list_title = db.Column(db.String(250), nullable=False)
    item_brand = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    placementofvehicle = db.Column(db.String(50), nullable=False)
    mpn = db.Column(db.String(50), nullable=False)
    oem_number = db.Column(db.String(50), nullable=False)
    material = db.Column(db.String(50), nullable=False)
    universal_fitment = db.Column(db.String(50), nullable=False)
    c_r_o_manufacture = db.Column(db.String(20), nullable=False)
    performance_part = db.Column(db.String(50), nullable=False)
    m_warranty = db.Column(db.String(50), nullable=False)
    item_height = db.Column(db.String(3), nullable=False)
    item_length = db.Column(db.String(3), nullable=False)
    item_width = db.Column(db.String(3), nullable=False)
    picture_1 = db.Column(db.String(100), nullable=False)
    picture_2 = db.Column(db.String(100), nullable=False)
    picture_3 = db.Column(db.String(100), nullable=False)
    picture_4 = db.Column(db.String(100), nullable=False)
    picture_5 = db.Column(db.String(100), nullable=False)
    picture_6 = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    pricing_type = db.Column(db.String(50), nullable=False)
    acution_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    last_update = db.Column(db.DateTime,
                            default=datetime.utcnow, onupdate=datetime.utcnow)
    detail_verified = db.Column(db.Boolean, default=False)
    # RelationShips
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey(
        'brand.id'), nullable=False)
    placementofvehicle_id = db.Column(
        db.Integer, db.ForeignKey('placementofvehicle.id'), nullable=False)
    material_id = db.Column(
        db.Integer, db.ForeignKey('material.id'), nullable=False)

    def __repr__(self):
        return f"Product('{self.id}', '{self.item_name}')"


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    last_update = db.Column(db.DateTime,
                            default=datetime.utcnow, onupdate=datetime.utcnow)
    detail_verified = db.Column(db.Boolean, default=False)
    # RelationShips
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey(
        'country.id'), nullable=False)
    products = db.relationship('Product', backref='brand', lazy='dynamic')

    def __repr__(self):
        return f"Brand('{self.id}', '{self.brand_name}', '{self.region}')"


class Itemcond(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cond_name = db.Column(db.String(50), nullable=False)
    cond_remark = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    last_update = db.Column(db.DateTime,
                            default=datetime.utcnow, onupdate=datetime.utcnow)
    detail_verified = db.Column(db.Boolean, default=False)
    # RelationShips
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)


class Placementofvehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pov_name = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    last_update = db.Column(db.DateTime,
                            default=datetime.utcnow, onupdate=datetime.utcnow)
    detail_verified = db.Column(db.Boolean, default=False)
    # RelationShips
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    products = db.relationship(
        'Product', backref='placemnetofvehicle', lazy='dynamic')

    def __repr__(self):
        return f"Brand('{self.id}', '{self.pov_name}')"


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_name = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    last_update = db.Column(db.DateTime,
                            default=datetime.utcnow, onupdate=datetime.utcnow)
    detail_verified = db.Column(db.Boolean, default=False)
    # RelationShips
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)

    def __repr__(self):
        return f"Brand('{self.id}', '{self.material_name}')"


class Color(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color_name = db.Column(db.String(50), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    last_update = db.Column(db.DateTime,
                            default=datetime.utcnow, onupdate=datetime.utcnow)
    detail_verified = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)

    def __repr__(self):
        return f"Color('{self.id}', '{self.color_name}')"


class Uservehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_plate = db.Column(db.String(100), unique=True, nullable=False)
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)
    owner_name = db.Column(db.String(50))
    v_body_color = db.Column(db.String(20), nullable=False)
    v_engine_no = db.Column(db.String(30), nullable=False)
    v_tax_expire = db.Column(db.DateTime, default=datetime.utcnow)
    v_insurance = db.Column(db.String(30), nullable=False)
    verification_remarks = db.Column(
        db.String(250), default="Vehicle not verified yet")
    v_makes = db.Column(db.String(100), default="default value empty")
    v_make_models = db.Column(db.String(100))
    v_years = db.Column(db.String(20))
    v_body_types = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    last_update = db.Column(db.DateTime,
                            default=datetime.utcnow, onupdate=datetime.utcnow)
    detail_verified = db.Column(db.Boolean, default=False)
    # RelationShips
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    v_make = db.Column(db.Integer, db.ForeignKey(
        'vehiclemake.id'), nullable=False)
    v_make_model = db.Column(db.Integer, db.ForeignKey(
        'vehiclemakemodel.id'), nullable=False)
    v_model_year = db.Column(db.Integer, db.ForeignKey(
        'vehiclemodelyear.id'))
    v_body_type = db.Column(db.Integer, db.ForeignKey(
        'vehiclebodytype.id'), nullable=False)
    new_orders = db.relationship(
        'Neworder', backref='user_vehicle', lazy='dynamic')

    def __repr__(self):
        return f"Uservehicle('{self.reg_plate}', '{self.owner_name}')"


class Vehiclemake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    vehicle_make = db.Column(db.String(50), unique=True)
    uservehicles = db.relationship(
        'Uservehicle', backref='vehiclemake', lazy='dynamic')
    mainvehicles = db.relationship(
        'Mainvehicle', backref='vehicle_make', lazy='dynamic')
    v_make = db.relationship(
        'Vehiclemakemodel', backref='vehicle_make', lazy='dynamic')

    def __repr__(self):
        return f"Vmake('{self.vehicle_make}', '{self.id}')"


class Vehiclemakemodel(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    vehicle_make_model = db.Column(db.String(50), unique=True)
    # Relationships
    uservehicles = db.relationship(
        'Uservehicle', backref='vehicle_make_model', lazy='dynamic')
    mainvehicles = db.relationship(
        'Mainvehicle', backref='vehicle_make_model', lazy='dynamic')
    v_make = db.Column(db.Integer, db.ForeignKey(
        'vehiclemake.id'), nullable=False)

    def __repr__(self):
        return f"Vmakemodel('{self.vehicle_make_model}', '{self.id}')"


class Vehiclemodelyear(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    vehicle_year = db.Column(db.String(4), unique=True)
    # Relationships
    uservehicles = db.relationship(
        'Uservehicle', backref='vehicle_model_year', lazy='dynamic')
    mainvehicles = db.relationship(
        'Mainvehicle', backref='vehicle_model_year', lazy='dynamic')

    def __repr__(self):
        return f"Vmodelyear('{self.vehicle_year}', '{self.id}')"


class Vehiclebodytype(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    vehicle_body_type = db.Column(db.String(50), unique=True)
    # Relationships
    uservehicles = db.relationship(
        'Uservehicle', backref='vehicle_body_type', lazy='dynamic')
    mainvehicles = db.relationship(
        'Mainvehicle', backref='vehicle_body_type', lazy='dynamic')

    def __repr__(self):
        return f"Vbodytype('{self.vehicle_body_type}', '{self.id}')"


class Mainvehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    vehicle_makes = db.Column(db.Integer, db.ForeignKey(
        'vehiclemake.id'), nullable=False)
    vehicle_make_models = db.Column(db.Integer, db.ForeignKey(
        'vehiclemakemodel.id'), nullable=False)
    vehicle_model_years = db.Column(db.Integer, db.ForeignKey(
        'vehiclemodelyear.id'), nullable=False)
    vehicle_body_types = db.Column(db.Integer, db.ForeignKey(
        'vehiclebodytype.id'), nullable=False)

    def __repr__(self):
        return f"Mainvehicle('{self.vehicle_name}', '{self.timestamp}')"


class Country(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(20), unique=True, nullable=False)
    flag_image = db.Column(db.String(60))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Relationships
    provinces = db.relationship(
        'Province', backref='country', lazy='dynamic')
    brands = db.relationship(
        'Brand', backref='country', lazy='dynamic')

    def __repr__(self):
        return f"Country('{self.id}','{self.country}')"


class Province(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(20), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Relationships
    country_id = db.Column(db.Integer, db.ForeignKey(
        'country.id'), nullable=False)
    citys = db.relationship(
        'City', backref='province', lazy='dynamic')

    def __repr__(self):
        return f"Province('{self.province}','{self.id}')"


class City(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Relationships
    provinces = db.Column(db.Integer, db.ForeignKey(
        'province.id'), nullable=False)
    district = db.relationship(
        'Districts', backref='districts', lazy='dynamic')

    def __repr__(self):
        return f"City('{self.city}', '{self.id}')"


class Districts(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    district = db.Column(db.String(20), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Relationships
    cities = db.Column(db.Integer, db.ForeignKey(
        'city.id'), nullable=False)
    town = db.relationship(
        'Town', backref='districts', lazy='dynamic')

    def __repr__(self):
        return f"Districts('{self.district}', '{self.id}')"


class Town(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    town = db.Column(db.String(20), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Relationships
    district = db.Column(db.Integer, db.ForeignKey(
        'districts.id'), nullable=False)
    area = db.relationship(
        'Areas', backref='areas', lazy='dynamic')

    def __repr__(self):
        return f"Town('{self.town}', '{self.id}')"


class Areas(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(20), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Relationships
    towns = db.Column(db.Integer, db.ForeignKey(
        'town.id'), nullable=False)

    def __repr__(self):
        return f"Areas('{self.area}', '{self.id}')"


class Profession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.String(30), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Profession('{self.profession}', '{self.timestamp}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    update_posted = db.Column(db.DateTime,
                              default=datetime.utcnow, onupdate=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


admin.add_view(Controller(User, db.session))
admin.add_view(Controller(Neworder, db.session))
admin.add_view(Controller(Product, db.session))
admin.add_view(Controller(Brand, db.session))
admin.add_view(Controller(Itemcond, db.session))
admin.add_view(Controller(Placementofvehicle, db.session))
admin.add_view(Controller(Material, db.session))
admin.add_view(Controller(Color, db.session))
admin.add_view(Controller(Uservehicle, db.session))
admin.add_view(Controller(Vehiclemake, db.session))
admin.add_view(Controller(Vehiclemakemodel, db.session))
admin.add_view(Controller(Vehiclemodelyear, db.session))
admin.add_view(Controller(Vehiclebodytype, db.session))
admin.add_view(Controller(Mainvehicle, db.session))
admin.add_view(Controller(Country, db.session))
admin.add_view(Controller(Province, db.session))
admin.add_view(Controller(City, db.session))
admin.add_view(Controller(Districts, db.session))
admin.add_view(Controller(Town, db.session))
admin.add_view(Controller(Areas, db.session))
admin.add_view(Controller(Profession, db.session))
admin.add_view(Controller(Post, db.session))
