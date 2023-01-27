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

vehi = Blueprint('vehi', __name__)


@ vehi.route('/uservehicle/add', methods=['GET', 'POST'])
@ login_required
def uservehicle():
    form = VehicleForm()
    uservehicle = Uservehicle.query.order_by(
        Uservehicle.id.desc()).filter_by(user_id=current_user.id)
    colours = ["White", "Yellow", "Grey", "Red", "Blue", "Black", "Orange"]
    insurance = ["None", "Adamjee", "Askari", "UIC", "TPL", "IGI",
                 "EFU", "Pak Qatar", "Century", "Salam Takafull"]
    form.vbodycolor.choices = [(colours) for colours in colours]
    form.vinsurance.choices = [(insurance) for insurance in insurance]
    form.vmake.choices = [(vmake.id, vmake.vehicle_make)
                          for vmake in Vehiclemake.query.all()]
    form.vmakemodel.choices = [(vmakemodel.id, vmakemodel.vehicle_make_model)
                               for vmakemodel in Vehiclemakemodel.query.all()]
    form.vmodelyear.choices = [(vmodelyear.id, vmodelyear.vehicle_year)
                               for vmodelyear in Vehiclemodelyear.query.all()]
    form.vbodytype.choices = [(vbodytype.id, vbodytype.vehicle_body_type)
                              for vbodytype in Vehiclebodytype.query.all()]
    if form.validate_on_submit():
        v_make_id = form.vmake.data
        v_make_model_id = form.vmakemodel.data
        v_year_id = form.vmodelyear.data
        v_body_type_id = form.vbodytype.data
        v_make_str = Vehiclemake.query.filter_by(id=v_make_id).first()
        v_make_model_str = Vehiclemakemodel.query.filter_by(
            id=v_make_model_id).first()
        v_year_str = Vehiclemodelyear.query.filter_by(id=v_year_id).first()
        v_body_type_str = Vehiclebodytype.query.filter_by(
            id=v_body_type_id).first()
        add_vehicle = Uservehicle(reg_plate=form.regplate.data,
                                  owner_name=form.ownername.data,
                                  v_body_color=form.vbodycolor.data, v_engine_no=form.vengineno.data,
                                  v_tax_expire=form.vtaxexpire.data,
                                  v_insurance=form.vinsurance.data, v_make=form.vmake.data,
                                  v_make_model=form.vmakemodel.data, v_model_year=form.vmodelyear.data,
                                  v_body_type=form.vbodytype.data, user_id=current_user.id,
                                  v_makes=v_make_str.vehicle_make, v_make_models=v_make_model_str.vehicle_make_model,
                                  v_years=v_year_str.vehicle_year, v_body_types=v_body_type_str.vehicle_body_type
                                  )
        db.session.add(add_vehicle)
        db.session.commit()
        flash(
            f'Your vehicle has been added.', 'success')
        return redirect(url_for('auth.uservehicle'))
    return render_template('user_vehicle.html', title='User Vehicle', legend='Add Vehicle',
                           legendright='Vehicle List', form=form, vehiclelists=uservehicle)


@ vehi.route('/vmakemodel/<get_vmake_id>')
def vmakemodelbyvmake(get_vmake_id):
    vmakemodel_data = Vehiclemakemodel.query.filter_by(
        v_make=get_vmake_id).all()
    vmakemodelArray = []
    for vmakemodel in vmakemodel_data:
        vmakemodelObj = {}
        vmakemodelObj['id'] = vmakemodel.id
        vmakemodelObj['makemodel'] = vmakemodel.vehicle_make_model
        vmakemodelArray.append(vmakemodelObj)
    return jsonify({'vmakmodellist': vmakemodelArray})
