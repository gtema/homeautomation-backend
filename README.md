# README # [![Build Status](https://travis-ci.org/gtema/homeautomation-backend.svg?branch=master)](https://travis-ci.org/gtema/homeautomation-backend)

My HomeAutomation project [HomeAutomation project](https://github.org/gtema/homeautomation) is an attempt to optimize some of the household activities and their efficiency. One of the most noticable examples for that is to keep track of groceries and household products to avoid their disposal or sudden lack. Sometimes you come from the shop and figure out that you have already few packages of flour. On the other hand you start coocking and figure out, that you have no milk. In order to solve this problem and potentially some others this project was created.

There is no idea to make this project public or to provide/guarantee any support to anybody, who would like to use it. However it is not in any way prohibited for anyone to use it.

# Quick summary #

The project consists currently from two independend modules: API (the backend) and the web UI (the frontend).
This project is a REST API module to cover all required services. It is build using Flask framework. The connection to the database is required


## Version

Heavy development stage, therefore just 0.0.3


### How do I get set up? ###

#### Use of local python
 - install python3-virtualenv
 - virtualenv venv
 - source venv/bin/activate
 - pip install -r requirements_nopg.txt (nopg has no postgresql dependency for a lighter dev setup)
 - python run.py (starts the server)

#### Use Heroku PaaS
  - Create account on Heroku, create python application for the server, add database. Use git push heroku master to push current repo as your app. For the setup trigger 'init' target to set up db tables and some test data (taken from categories.csv, products.csv)
  In the application config variables set the APP_SETTINGS=config.HerokuConfig. Then the DATABASE_URL variable will be respected and used as a DB

#### Custom PaaS
  - build and push container and deploy it how the platform requires

#### Configuration

Api configuration is present under the backend/{config.py,instance/config.py}
`APP_SETTINGS` variable allows to choose from different preconfigured setups (see config.py for details):
- *config.HerokuConfig* - deploy to Heroku. Will respect DATABASE_URL variable for the db configuration
- *config.Travis* - configuration for the Travis CI
- *config.Local* - default confiuration object

Apart of that variable FLASKR_SETTINGS can contain file name with the configuration to override defaults

#### Dependencies

Quite a few, see requirements.txt (or requirements_nopg.txt for a SQLite setup)

#### Database configuration

Up to now a local SQLite DB is used (app.SQLite) for development purposes. Repo contains init.py script, which creates the DB schema according to the configured connection and populates it with my "development" data. Feel free to modify it for your needs.


### Testing

- CLI tests (curl of API). Do not forget your auth
  - `curl "http://localhost:5000/api/v0/stock/product" -H 'Content-Type: application/json' -X POST -d '{"name":"t11","category_id":7}' -v`
  - `curl "http://localhost:5000/api/v0/stock/products_by_category_id/4"`
  - `curl "http://localhost:5000/api/v0/stock/product/12" -H 'Content-Type: application/json' -X PUT -d '{"name":"t11","category_id":1,"id":12}' -v`
  - `curl "http://localhost:5000/api/v0/stock/product/12" -H 'Content-Type: application/json' -X DELETE`
- python tests
  - `python test.py`

### Security

Backend REST API access is protected by the Basic auth or API_KEY authorization token. In order to use API authorize yourself first at the
given auth point (by default configured /auth) and add received token (or the API_KEY) to the headers of all further API requests. Alternatively simply provide credentials with each API request (basic auth). User creation is not supported so far (during the db initialization few example users are being created)

### Deployment instructions

I'm planning to run the project on the RaspberryPi V1. So most likely it would be deployed under mod_wsgi@apache application serving also compacted JS due to the performance lack. However there are multiple possibilities for deployment:

- docker containers (standalone containers, mixed container with mod_fsgi + compacted JS, docker-compose, docker cloud)
- Standalone apps: API (Flask server, any other Python web server, mod_fsgi) and Web (node.js, minimized JS on a static web werver)
- PaaS:
  - Heroku: API is deployable to the Heroku with no changes now. Just set the config variable APP_SETTINGS=config.HerokuConfig and configure a PG addon
- [AtomicApp](https://github.com/projectatomic/atomicapp) is in a concept stage and will be prepared as a separate repo

There is small helper script for deployment in the repo root. It currently supports deployment to my home RaspberryPi and Heroku.

The only rule for deployment: connect API with DB of your choice, configure Frontend to provide correct link to API from browsers.

### UML diagrams

update coming soon...
