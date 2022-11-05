from app.models import ProductInformation
from app.models import User
from app import sa
from flask import Blueprint, render_template, request, redirect, url_for, flash
import csv


views = Blueprint('views', __name__)


@views.route('/')
def index():
    if ProductInformation.query.first():
        return render_template("home.html")
    else:    
        with open('app\static\products\dataset.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    product_info = ProductInformation(row[0], row[1], row[2], row[3], row[4], row[5])
                    product_info.save() 
                    line_count += 1
        return render_template("home.html")


@views.route('/success')
def success():
    return render_template('success.html')


@views.route('/view_products/<category>')
def product(category):
    products = ProductInformation.query.filter_by(category = category).all()
    return render_template('view_products.html', products = products)


@views.route('/unsuccessful')
def unsuccessful():
    return render_template('unsuccessful.html')


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
        price_stripe = request.form['price_stripe']

        product_info = ProductInformation(name, desc, category, price, url, price_stripe)
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
        product_info.price_stripe = request.form.get('price_stripe')
        product_info.save()
        
        flash("Product Updated Successfully")

        return redirect (url_for('views.adminDashboard'))


@views.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        product_info = ProductInformation.query.get(request.form.get('id'))
        product_info.delete()
        flash("Product Deleted Successfully")
        return redirect (url_for('views.adminDashboard'))