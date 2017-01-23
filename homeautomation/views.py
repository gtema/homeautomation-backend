from flask import render_template, request,\
                  url_for, session, redirect, flash, abort
from flask_login import login_user, logout_user, login_required
from . import app, lm
from .models import User
from .forms import LoginForm
''', PostForm'''
# from StockManager import lm
# from StockManager import models

# @lm.user_loader
# def load_user(user_id):
#    ''' Load loggedin user from the DB'''
#    print ('load_user ', user_id)
#    return User.query.filter(User.id == user_id).first()
#
# @lm.request_loader
# def load_user_from_request(req):
#    print ('load_user_from_request')
#    api_key = req.args.get('api_key')
#    if (api_key):
#        return User.query.filter(User.id == 1).first()
#    return None
#    '''User.query.filter(User.id == user_id).first()'''


@lm.user_loader
def load_user(user_id):
    ''' Load loggedin user from the DB'''
    '''print('load_user ', user_id)'''
    return User.query.filter(User.id == user_id).first()


@lm.request_loader
def load_user_from_request(req):
    '''print('load_user_from_request')'''
    api_key = req.args.get('api_key')
    if (api_key):
        return User.query.filter(User.api_key == api_key).first()
    return None


def next_is_valid(next):
    ''' Check privs for accessing next page '''
    return True


@app.route('/')
def index():
    return render_template('index.html', title="StockManager")


# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' Login handler'''
    form = LoginForm()
    if form.validate_on_submit():
        print('userdata=', form.username.data)
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)
            flash('Logged in successfully')

            next = request.args.get('next')

            if not next_is_valid(next):
                return abort(404)

            return redirect(next or url_for('index'))
    print('not valid')
    return render_template('login.html', form=form, title='My app login')


@app.route('/logout')
@login_required
def logout():
    ''' Logout page'''
    session.pop('username', None)
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('index'))


@app.route('/catalogue')
@login_required
def catalogue():
    "Catalogue page"
    return render_template('cat.html', title='StockManager Catalogue')
