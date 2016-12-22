*Initial installation
- install python3-virtualenv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python run.py

*To start server
start_server.sh

*CLI tests
curl "http://localhost:5000/api/v0/stock/product?api_key=2" -H 'Content-Type: application/json' -X POST -d '{"name":"t11","category_id":7}' -v
curl "http://localhost:5000/api/v0/stock/products_by_category_id/4?api_key=2"
curl "http://localhost:5000/api/v0/stock/product/12?api_key=2" -H 'Content-Type: application/json' -X PUT -d '{"name":"t11","category_id":1,"id":12}' -v
curl "http://localhost:5000/api/v0/stock/product/12?api_key=2" -H 'Content-Type: application/json' -X DELETE
