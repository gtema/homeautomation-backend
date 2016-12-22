from homeautomation import db
from homeautomation.models import *

db.drop_all()

db.create_all()

user = User(username='admin', password='test')

db.session.add(user)

#Category = StockProductCategory(id = 1,  parent_id = 0,  name = 'g1')

db.session.add(StockProductCategory(id = 1,  parent_id = 0,  name = 'Lebensmittel'))
db.session.add(StockProductCategory(id = 2,  parent_id = 0,  name = 'Drogerie'))
db.session.add(StockProductCategory(id = 3,  parent_id = 0,  name = 'Haushaltmittel'))
db.session.add(StockProductCategory(id = 4,  parent_id = 1,  name = 'Milchprodukte'))
db.session.add(StockProductCategory(id = 5,  parent_id = 1,  name = 'Obst'))
db.session.add(StockProductCategory(id = 6,  parent_id = 1,  name = 'Gemüse'))
db.session.add(StockProductCategory(id = 7,  parent_id = 4,  name = 'Milch'))
db.session.add(StockProductCategory(id = 8,  parent_id = 4,  name = 'Käse'))
db.session.add(StockProductCategory(id = 9,  parent_id = 4,  name = 'Joghurt'))

db.session.add(StockProduct(id = 1,  category_id= 5,  name = 'p1',  count_quantities = False))
db.session.add(StockProduct(id = 2,  category_id= 4,  name = 'p2'))
db.session.add(StockProduct(id = 3,  category_id= 4,  name = 'p3',  count_quantities = False))
db.session.add(StockProduct(id = 4,  category_id= 2,  name = 'p4'))
db.session.add(StockProduct(id = 5,  category_id= 7,  name = 'Milch 1,5%'))
db.session.add(StockProduct(id = 6,  category_id= 7,  name = 'Milch 3%'))

db.session.add(StockProductItem(id = 1,  product_id= 1, amount = 2, is_started = True))
db.session.add(StockProductItem(id = 2,  product_id= 1, amount= 4))

db.session.add(StockProductItem(id = 3,  product_id= 2, amount = 2))
db.session.add(StockProductItem(id = 4,  product_id= 2, amount= 4, is_started=True))

db.session.add(StockProductItem(id = 5,  product_id= 3, amount = 2))
db.session.add(StockProductItem(id = 6,  product_id= 3, amount= 4))

db.session.commit()
