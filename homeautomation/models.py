import datetime
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore


db = SQLAlchemy()


class BaseCrud():
    '''
    Base CRUD Enservices Entity class
    it requires SQLAlchemy model, Marshmallow schema
    '''
    def add(self, entity):
        '''
        ADD entity from the model itself
        '''
        db.session.add(entity)
        db.session.commit()

    def update(self, schema, json):
        '''
        UPDATE the entity
        '''
        data, errors = schema.load(json,
                                   instance=self,
                                   session=db.session)

        if not errors:
            db.session.commit()

        return data, errors

    def delete(self, item):
        '''
        DELETE method to drop product
        '''
        db.session.delete(item)
        db.session.commit()


# https://pythonhosted.org/Flask-Security/quickstart.html
# Association Table for Roles and Users
roles_users = db.Table('roles_users',
                       db.Column('user_id',
                                 db.Integer(),
                                 db.ForeignKey('user.id')
                                 ),
                       db.Column('role_id',
                                 db.Integer(),
                                 db.ForeignKey('role.id')
                                 )
                       )


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<models.Role[name=%s]>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    api_key = db.Column(db.String(255))
    # confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer())

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    def __repr__(self):
        return '<models.User[username=%s]>' % self.username


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


# homeautomation models

class StockProductCategory(db.Model, BaseCrud):
    '''
    Category model
    '''

    __tablename__ = "cat_category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('cat_category.id',
                                                    ondelete='CASCADE'))
    name = db.Column(db.String(255), nullable=False)
    prio = db.Column(db.Integer, default=0)


class StockProductItem(db.Model, BaseCrud):
    '''
    Product item model
    '''
    __tablename__ = "cat_prod_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('cat_product.id',
                                         ondelete='CASCADE',
                                         onupdate='CASCADE'),
                           nullable=False)
    amount = db.Column(db.Integer, default=1)
    is_started = db.Column(db.Boolean, default=False)
    is_disposed = db.Column(db.Boolean, default=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    expiry_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_valid = db.column_property(is_disposed == False and amount > 0)

    # @hybrid_property
    # def is_valid(self):
    #     if self.amount > 0 and not self.is_disposed:
    #         return True
    #     return False


class StockProduct(db.Model, BaseCrud):
    '''
    Product model
    '''
    __tablename__ = "cat_product"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('cat_category.id'),
                            nullable=False)
    name = db.Column(db.String(255), nullable=False)
    volume = db.Column(db.String(64), nullable=True)
    sum_amounts = db.Column(db.Boolean, default=True)

    @hybrid_property
    def valid_items(self):
        return StockProductItem.query.filter(
                            StockProductItem.product_id == self.id,
                            StockProductItem.is_valid)

    @hybrid_property
    def open_items(self):
        return self.valid_items.filter(
                            StockProductItem.is_started)

    @hybrid_property
    def amount(self):
        if (self.sum_amounts is False):
            result = self.valid_items.count()
        else:
            result = sum(elem.amount for elem in self.valid_items.all())
        return result

    @hybrid_property
    def first_started_id(self):
        item = self.open_items.\
                    order_by(StockProductItem.expiry_date).\
                    first()
        return item.id

    @hybrid_property
    def first_started_ed(self):
        item = self.open_items.\
                    order_by(StockProductItem.expiry_date).\
                    first()
        return item.expiry_date
