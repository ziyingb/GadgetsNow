from app.models import ProductInformation, ShoppingCart
from app import sa
from flask import Blueprint, session, render_template, request, redirect, url_for, flash
import flask
import csv
from app.forms import *



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
def view_products(category):
    products = ProductInformation.query.filter_by(category = category).all()
    return render_template('view_products.html', products = products)


@views.route('/view_products/item/<productid>', methods = ['POST', 'GET'])
def product(productid):
    if request.method == 'POST':
        if '_id' in  session:
            uid = session['_id']
            prod_id = productid
            prod_price_stripe = request.form.get('prod_price_stripe', '', type=str)
            prod_price = request.form.get('prod_price', '', type=str)
            prod_quantity = request.form.get('quantity', '', type=int)
            prod_url = request.form.get('prod_url', '', type=str)
            prod_name = request.form.get('prod_name', '', type=str)
            prod_category = request.form.get('prod_category', '', type=str)
            checkIfExist = ShoppingCart.query.filter_by(uid = uid, prod_id = prod_id).first()
            if checkIfExist:
                checkIfExist.add_quantity(prod_quantity)
            else:
                cart_item = ShoppingCart(uid, prod_quantity, prod_id, prod_name, prod_category, prod_price, prod_price_stripe, prod_url)
                cart_item.add()
            flask.flash('Product successfully added to cart.')
        else:
            return redirect(url_for('auth.login'))
    product = ProductInformation.query.filter_by(id = productid).first()
    form = addToCart(request.form)
    return render_template('product.html', product = product, form = form)


@views.route('/unsuccessful')
def unsuccessful():
    return render_template('unsuccessful.html')


@views.route('/adminDashboard')
def adminDashboard():
    if 'priviledge' in session:
        if session['priviledge'] == 'admin':
            product_data = ProductInformation.query.all()
            return render_template('adminDashboard.html', products = product_data)
    return redirect(url_for('auth.login'))


@views.route('/insert', methods= ['POST'])
def insert():
    if 'priviledge' in session:
        if session['priviledge'] == 'admin':
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
        else:
            return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))

@views.route('/update', methods= ['GET', 'POST'])
def update():
    if 'priviledge' in session:
        if session['priviledge'] == 'admin':
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
                
        else:
            return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))



@views.route('/delete', methods = ['GET', 'POST'])
def delete():
    if 'priviledge' in session:
        if session['priviledge'] == 'admin':
            if request.method == 'POST':
                product_info = ProductInformation.query.get(request.form.get('id'))
                product_info.delete()
                flash("Product Deleted Successfully")
                return redirect (url_for('views.adminDashboard'))
        else:
            return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))

