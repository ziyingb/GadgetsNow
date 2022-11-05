from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired
from .validators import *
import re

class LoginForm(FlaskForm):
	recaptcha = RecaptchaField()
	usernameoremail = StringField  (u'UsernameOrEmail' , validators=[DataRequired()])
	password = PasswordField(u'Password' , validators=[DataRequired()])
	remember_me = BooleanField()
	

class RegisterForm(FlaskForm):
# 	def validate_password(form, field):	
# 		msg = ""
# 		password = field.data
# 		if len(password)<5 and len(password)>15:
# 			msg = "Password denied: must be between 5 and 15 characters long."
# 		elif re.search('[0-9]',password) is None:
# 			msg = "Password denied: must contain a number between 0 and 9"
# 		elif re.search('[A-Z]',password) is None:
# 			msg = "Password denied: must contain a capital letter."
# 		elif re.search('[a-z]',password) is None:
# 			msg = "Password denied: must contain a lowercase letter."
# 		elif re.search('[!@#$%&()\-_[\]{\};:"./<>?]', password) is None:
# 			msg = "Password denied: must contain a special character"           
# 		if msg != "":
# 			raise ValidationError(msg)
			
	recaptcha = RecaptchaField()
	username = StringField  (u'Username' , validators=[DataRequired()])
	password = PasswordField(u'Password' , validators=[DataRequired()])
	email = StringField  (u'Email' , validators=[DataRequired(), Email()])


class VerifyUser(FlaskForm):
	otp_code = StringField  (u'Verification' , validators=[DataRequired()])


class UpdateProfile(FlaskForm):
	first_name = StringField(u'First Name')
	last_name = StringField(u'Last Name')
	mobile_no = StringField(u'Mobile number')
	country_list = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua &amp; Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia &amp; Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Cote D Ivoire","Croatia","Cruise Ship","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Polynesia","French West Indies","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Guernsey","Guinea","Guinea Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyz Republic","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Mauritania","Mauritius","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Namibia","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russia","Rwanda","Saint Pierre &amp; Miquelon","Samoa","San Marino","Satellite","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","South Africa","South Korea","Spain","Sri Lanka","St Kitts &amp; Nevis","St Lucia","St Vincent","St. Lucia","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Timor L'Este","Togo","Tonga","Trinidad &amp; Tobago","Tunisia","Turkey","Turkmenistan","Turks &amp; Caicos","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Venezuela","Vietnam","Virgin Islands (US)","Yemen","Zambia","Zimbabwe"]
	country = SelectField('Delivery Types', choices=country_list, default=1)
	address = StringField(u'Address')
	city = StringField(u'City')
	postal_code = StringField(u'Postal Code')


class addToCart(FlaskForm):
	def quantity_range(form, field):
		quantity = field.data
		msg = ""
		if quantity >999 or quantity<1:
			msg = "Invalid quantity. Please try again"
			raise ValidationError(msg)
	quantity = IntegerField(u'Quantity', validators=[quantity_range], default = 1)
	prod_id = HiddenField(u'Product ID')
	prod_name = HiddenField(u'Product Name')
	prod_category = HiddenField(u'Product Category')
	prod_price_stripe = HiddenField(u'Product Price Stripe')
	prod_price = HiddenField(u'Product Price')
	prod_url = HiddenField(u'Product URL')
	

class updateProdDetail(FlaskForm):
	prod_id = HiddenField(u'Product ID')
	prod_name = StringField(u'Product Name')
	prod_desc = StringField(u'Product Description')
	prod_category = StringField(u'Product Category')
	prod_price = StringField(u'Product Price')
	prod_url = StringField(u'Product URL')
	prod_stripe = StringField(u'Product Stripe')


class ForgetPasswordForm(FlaskForm):
	recaptcha = RecaptchaField()
	usernameoremail = StringField  (u'UsernameOrEmail' , validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
	password = PasswordField(u'Password' , validators=[DataRequired()])
	passwordCheck = PasswordField(u'Password' , validators=[DataRequired()])
