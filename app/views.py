from app.models import ProductInformation
from app import sa
from flask import Blueprint, render_template, request, redirect, url_for, flash

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("home.html")

@views.route('/adminDashboard')
def adminDashboard():
    product_data = ProductInformation.query.all()

    return render_template('adminDashboard.html', products = product_data)

@views.route('/insert', methods= ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form['desc']
        category = request.form['category']
        price = request.form['price']
        url = request.form['url']

        product_info = ProductInformation(name, desc, category, price, url)
        sa.session.add(product_info)
        sa.session.commit()

        flash("Product Added Successfully")

        return redirect (url_for('views.adminDashboard'))

@views.route('/update', methods= ['GET', 'POST'])
def update():
    if request.method == 'POST':
        product_info = ProductInformation.query.get(request.form.get('id'))
        
        product_info.name = request.form.get('name')
        product_info.desc = request.form.get('desc')
        product_info.category = request.form.get('category')
        product_info.price = request.form.get('price')
        product_info.url = request.form.get('url')

        sa.session.commit()
        
        flash("Product Updated Successfully")

        return redirect (url_for('views.adminDashboard'))

@views.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        product_info = ProductInformation.query.get(request.form.get('id'))
        sa.session.delete(product_info)
        sa.session.commit()

        flash("Product Deleted Successfully")

        return redirect (url_for('views.adminDashboard'))