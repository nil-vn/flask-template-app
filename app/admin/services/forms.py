from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Optional, Email, Length, EqualTo


class CarForm(FlaskForm):
    id = IntegerField("id")
    name = StringField("name", validators=[DataRequired()])
    vin = StringField("vin")
    model = StringField("model")
    branch = StringField("branch")
    color = StringField("color")
    traded_company = StringField("traded_company")
    imported_date = StringField("imported_date")
    inspection_from = StringField("inspection_from")
    inspection_to = StringField("inspection_to")
    year_of_manufacture = StringField("year_of_manufacture")
    purchase_price = IntegerField("purchase_price", validators=[Optional()])
    expected_selling_price = IntegerField(
        "expected_selling_price", validators=[Optional()]
    )
    actual_selling_price = IntegerField("actual_selling_price", validators=[Optional()])
    status = StringField("status")
    note = StringField("note")
    license_plate_no = StringField("license_plate_no")


class CustomerForm(FlaskForm):
    id = IntegerField("id")
    name = StringField("name", validators=[DataRequired()])
    gender = StringField("gender")
    birth_day = StringField("birth_day")
    facebook = StringField("facebook")
    phone = StringField("phone")
    address = StringField("address")
    license_img = StringField("license_img")
    gallery_id = StringField("gallery_id")
    lead_source = StringField("lead_source")
    status = StringField("status")
    note = StringField("note")


class TransactionForm(FlaskForm):
    id = IntegerField("id")
    customer_id = StringField("customer_id")
    purchase_date = StringField("purchase_date")
    selling_price = IntegerField("selling_price", validators=[Optional()])
    status = StringField("status")
    note = StringField("note")
    car_id = StringField("car_id")


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField(
        "username", validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField("email", validators=[Optional(), Email()])
    password = PasswordField("password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "confirm password", validators=[DataRequired(), EqualTo("password")]
    )
    role = StringField("role", validators=[Optional()])


class UserUpdateForm(FlaskForm):
    username = StringField(
        "username", validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField("email", validators=[Optional(), Email()])
    password = PasswordField("password", validators=[Optional(), Length(min=6)])
    role = StringField("role", validators=[Optional()])
