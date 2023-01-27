from flask import Blueprint, render_template
from flask_login import login_required
from .models import Itemcond, Brand, Color, Placementofvehicle, Material, Country
from .forms import AddProd
prod = Blueprint('prod', __name__)


@prod.route('/prod')
@login_required
def full_prod():

    return render_template('product.html', title='Product info')


@prod.route('/add_prod')
@login_required
def add_prod():
    form = AddProd()
    form.item_cond.choices = [(itemcond.id, itemcond.cond_name)
                              for itemcond in Itemcond.query.all()]
    form.item_brand.choices = [(brand.id, brand.brand_name)
                               for brand in Brand.query.all()]
    form.color.choices = [(color.id, color.color_name)
                          for color in Color.query.all()]
    form.pov.choices = [(pov.id, pov.pov_name)
                        for pov in Placementofvehicle.query.all()]
    form.material.choices = [(material.id, material.material_name)
                             for material in Material.query.all()]
    form.c_r_o_manufacture.choices = [
        (country.id, country.country) for country in Country.query.all()]
    return render_template('create_product.html', title='Add Product', form=form, legend='Add Product')
