from flask import Flask, render_template,redirect,url_for,request,flash
from model import db, user as user_model


app = Flask(__name__)
app.secret_key='trek-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)


with app.app_context():
    db.create_all()


# with app.app_context():
#     username = 'admin'
#     role = 'admin'
#     password= 'admin'
#     email = 'admin@gmail.com'
#     check_admin=user_model.query.filter_by(email=email,role=role).first()
#     if not check_admin:
#         admin_details = user_model(username=username,email=email,password=password, role=role)
#         db.session.add(admin_details)
#         db.session.commit()


@app.route("/")
def home():
    return render_template('home.html')


# @app.route("/search/<string:something>",methods=['GET'])
# def search(something):
#     data = ...

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    
    elif request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # check_admin = user_model.query.filter_by(email='admin@gmail.com',password='admin').first()
        check_user = user_model.query.filter_by(email=email,password=password).first()

        if check_user:
            return render_template('user_dashboard.html',email=email,password=password)
        elif not check_user:
            return render_template('login.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    elif request.method=='POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        check_user = user_model.query.filter_by(email=email).first()

        if check_user:
            message = 'Already a user!'
            return render_template('login.html',msg=message)
        elif not check_user:
            user_details = user_model(username=username,email=email,password=password,role=role)
            db.session.add(user_details)
            db.session.commit()
            message = 'Signup Successful'
            return render_template('login.html',msg=message)





@app.route('/admin_login')
def admin_login():
    if request.method=='GET':
        return render_template('admin_login.html')
    elif request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        check_admin = user_model.query.filter_by(email=email,password=password).first()

        if check_admin:
            return render_template('admin_dashboard.html')
        elif not check_admin:
            return render_template('admin_login.html')




app.run(debug=True)