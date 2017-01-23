from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from flask_login import UserMixin
import datetime
from . import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    api_key = db.Column(db.String(255), nullable=True, default='')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def is_correct_password(self, plaintext):
        self.__auth = (self._password == plaintext)
        return self.__auth

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def __set_password(self, plaintext):
        self._password = plaintext

    @staticmethod
    def get(id):
        print('get user with id=', id)
        user = User()
        user.id = id
        return user


class StockProductCategory(db.Model):
    __tablename__ = "cat_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer,  db.ForeignKey('cat_category.id'))
    name = db.Column(db.String(255), nullable=False)
    prio = db.Column(db.Integer, default=0)
#    products = db.relationship("Products",  backref = "parent")


class StockProductItem(db.Model):
    __tablename__ = "cat_prod_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer,
                           db.ForeignKey('cat_product.id'),
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


class StockProduct(db.Model):
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
