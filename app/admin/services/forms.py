from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Optional


class CarForm(FlaskForm):
    id = StringField("id")
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
    id = StringField("id")
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
    id = StringField("id")
    customer_id = StringField("customer_id")
    purchase_time = StringField("purchase_time")
    selling_price = StringField("selling_price", validators=[Optional()])
    status = StringField("status")
    note = StringField("note")
    car_id = StringField("car_id")
