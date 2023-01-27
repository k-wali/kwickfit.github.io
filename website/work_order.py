import os
import secrets
import PIL
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, jsonify, json
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, New_OrderForm
from .models import User, Profession, Neworder, Uservehicle, Vehiclemake, Country, Province, City, Districts, Town, Areas
from werkzeug.security import generate_password_hash, check_password_hash
from website import db, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

work_order = Blueprint('work_order', __name__)


@work_order.route('/workorder/create_work_order', methods=['GET', 'POST'])
@login_required
def create_work_order():
    form = New_OrderForm()
    form.svehicle.choices = [(svehicle.id, svehicle.reg_plate)
                             for svehicle in Uservehicle.query.filter_by(user_id=current_user.id).all()]
    if form.validate_on_submit():

        post = Neworder(order=form.title.data,
                        order_content=form.content.data, author=current_user, user_vehicles=form.svehicle.data)
        db.session.add(post)
        db.session.commit()
        flash('Your vehicle inspection has been created!', 'success')
        return redirect(url_for('views.home'))

    return render_template('create_work_order.html', title='New Order', form=form, legend='Create Order', legendright='Order History')


@work_order.route('/workorder/<int:order_id>')
def orderview(order_id):
    order = Neworder.query.get_or_404(order_id)
    return render_template('order.html', title=order.title, order=order)
