from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv
import os

from flask_security.utils import encrypt_password
from homeautomation import create_app
from homeautomation.models import db, StockProductCategory, StockProduct,\
                                  StockProductItem, User, Role, roles_users, user_datastore

class herokuConfig(object):
    # Setup an in-memory SQLite DB, create schema
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

app = create_app(herokuConfig)

with app.app_context():
    db.drop_all()
    db.create_all()
    with open('categories.csv') as f:
        # assume first line is header
        cf = csv.DictReader(f, delimiter=',')
        for row in cf:
            db.session.add(
                StockProductCategory(
                    id=row.get('Id'),
                    parent_id=row.get('Parent_id'),
                    name=row.get('Name'),
                    prio=row.get('Prio')
                )
            )

    with open('products.csv') as f:
        # assume first line is header
        cf = csv.DictReader(f, delimiter=',')
        for row in cf:
            db.session.add(
                StockProduct(
                    id=row.get('Id'),
                    category_id=row.get('Category_id'),
                    name=row.get('Name'),
                    volume=row.get('Volume'),
                    sum_amounts=row.get('Sum_amounts')
                )
            )

    # Create the default roles
    basic = user_datastore.find_or_create_role(name='User', description="Basic user")
    admin = user_datastore.find_or_create_role(name='Admin', description='API Administrator')

    # Create the default users
    user_datastore.create_user(username='papa', email='test1@gmail.com', password=encrypt_password('apap'), first_name="Papa", last_name="Family", api_key="bla")
    user_datastore.create_user(username='mama', email='test2@gmail.com', password=encrypt_password('amam'), first_name="Mama", last_name="Family")
    user_datastore.create_user(username='child', email='test3@gmail.com', password=encrypt_password('dlihc'), first_name="Child", last_name="Family")

    papa = user_datastore.find_user(username='papa')
    mama = user_datastore.find_user(username='mama')
    child = user_datastore.find_user(username='child')

    user_datastore.activate_user(papa)
    user_datastore.activate_user(mama)
    user_datastore.activate_user(child)

    user_datastore.add_role_to_user(papa, admin)
    user_datastore.add_role_to_user(mama, admin)
    user_datastore.add_role_to_user(child, basic)

    # Save users
    db.session.commit()
