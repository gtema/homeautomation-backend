from homeautomation import db
from homeautomation.models import StockProductCategory, StockProduct,\
                                  StockProductItem, User
import csv

db.drop_all()
db.create_all()

user = User(username='admin', password='test', api_key='23')
db.session.add(user)

# Category=StockProductCategory(id=1, parent_id=0, name='g1')

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


# db.session.add(StockProductCategory(id=1, parent_id=0, name='Lebensmittel', prio=0))
# db.session.add(StockProductCategory(id=2, parent_id=0, name='Drogerie', prio=2))
# db.session.add(StockProductCategory(id=3, parent_id=0, name='Haushaltmittel', prio=3))
# db.session.add(StockProductCategory(id=4, parent_id=1, name='Milchprodukte', prio=0))
# db.session.add(StockProductCategory(id=5, parent_id=1, name='Obst', prio=2))
# db.session.add(StockProductCategory(id=6, parent_id=1, name='Gemüse', prio=1))
# db.session.add(StockProductCategory(id=7, parent_id=4, name='Milch'))
# db.session.add(StockProductCategory(id=8, parent_id=4, name='Käse'))
# db.session.add(StockProductCategory(id=9, parent_id=4, name='Joghurt'))
#
# db.session.add(StockProduct(id=1, category_id=5, name='p1',
#                             count_quantities=False))
# db.session.add(StockProduct(id=2, category_id=4, name='p2'))
# db.session.add(StockProduct(id=3, category_id=4, name='p3',
#                             count_quantities=False))
# db.session.add(StockProduct(id=4, category_id=2, name='p4'))
# db.session.add(StockProduct(id=5, category_id=7, name='Milch 1,5%'))
# db.session.add(StockProduct(id=6, category_id=7, name='Milch 3%'))
#
# db.session.add(StockProductItem(id=1, product_id=1, amount=2, is_started=True))
# db.session.add(StockProductItem(id=2, product_id=1, amount=4))
#
# db.session.add(StockProductItem(id=3, product_id=2, amount=2))
# db.session.add(StockProductItem(id=4, product_id=2, amount=4, is_started=True))
#
# db.session.add(StockProductItem(id=5, product_id=3, amount=2))
# db.session.add(StockProductItem(id=6, product_id=3, amount=4))

db.session.commit()
