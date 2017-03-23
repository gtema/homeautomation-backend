# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
import csv
import os
import sys
# import random
from base64 import b64encode

from flask_security.utils import encrypt_password
from homeautomation import create_app
from homeautomation.models import db, StockProductCategory, StockProduct,\
                                  user_datastore

app = create_app()

with app.app_context():
    app.logger.info('Recreating DB')
    db.drop_all()
    db.create_all()
    app.logger.info('Filling DB with test data')

    # Create the default roles
    app.logger.info('Filling DB with users')
    try:
        basic = user_datastore.find_or_create_role(name='User',
                                                   description="Basic user")
        admin = user_datastore.find_or_create_role(name='Admin',
                                                   description='API Administrator')

        # Create the default users
        user_datastore.create_user(username='papa',
                                   email='test1@gmail.com',
                                   password=encrypt_password('apap'),
                                   first_name="Papa",
                                   last_name="Family",
                                   api_key=b64encode(os.urandom(48)).decode('ascii'))
        user_datastore.create_user(username='mama',
                                   email='test2@gmail.com',
                                   password=encrypt_password('amam'),
                                   first_name="Mama",
                                   last_name="Family",
                                   api_key=b64encode(os.urandom(48)).decode('ascii'))
        user_datastore.create_user(username='child',
                                   email='test3@gmail.com',
                                   password=encrypt_password('dlihc'),
                                   first_name="Child",
                                   last_name="Family")

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
    except:
        app.logger.exception('Exception occured during installing users',
                             sys.exc_info()[0])
        raise

    try:
        app.logger.info('Filling DB with categories')
        with open('categories.csv', encoding='utf-8') as f:
            # assume first line is header
            cf = csv.DictReader(f, delimiter=',')
            for row in cf:
                parent_id = row.get('Parent_id')
                db.session.add(
                    StockProductCategory(
                        id=int(row.get('Id')),
                        parent_id=int(parent_id) if parent_id != '' else None,
                        name=row.get('Name'),
                        prio=row.get('Prio')
                    )
                )

        db.session.commit()

        app.logger.info('Filling DB with products')
        with open('products.csv', encoding='utf-8') as f:
            # assume first line is header
            cf = csv.DictReader(f, delimiter=',')
            for row in cf:
                db.session.add(
                    StockProduct(
                        id=int(row.get('Id')),
                        category_id=int(row.get('Category_id')),
                        name=row.get('Name'),
                        volume=row.get('Volume'),
                        sum_amounts=row.get('Sum_amounts')
                    )
                )
        db.session.commit()
    except:
        app.logger.exception('Exception occured during installing data',
                             sys.exc_info()[0])
        raise
