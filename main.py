from flask import Flask, render_template,redirect,url_for,request,session
from model import db, user as user_model , staff as staff_model , trek as trek_model , booking as booking_model


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






# LOGIN
@app.route('/user_login',methods=['GET','POST'])
def user_login():
    if request.method=='GET':
        return render_template('user_login.html')
    
    elif request.method=='POST':
        
        email = request.form.get('email')
        password = request.form.get('password')

        # check_admin = user_model.query.filter_by(email='admin@gmail.com',password='admin').first()
        check_user = user_model.query.filter_by(email=email,password=password,role='user').first()

        if check_user:
            session['user_id'] = check_user.user_id
            session['role'] = check_user.role
            return redirect(url_for('user_dashboard'))
        else:
            return render_template('user_login.html',error="Invalid credentials")



@app.route('/staff_login',methods=['GET','POST'])
def staff_login():
    if request.method=='GET':
        return render_template('staff_login.html')
    
    elif request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        check_staff = user_model.query.filter_by(email=email,password=password,role='staff').first()

        if check_staff:
            if not check_staff.is_approved:
                return render_template('staff_login.html', error="Wait for admin approval")

            session['user_id'] = check_staff.user_id
            session['role'] = check_staff.role

            # ✅ FIX: redirect (NOT render)
            return redirect(url_for('staff_dashboard'))

        else:
            return render_template('staff_login.html',error="Invalid credentials")




@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method=='GET':
        return render_template('admin_login.html')
    
    elif request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        check_admin = user_model.query.filter_by(email=email,password=password,role='admin').first()

        if check_admin:
            session['user_id'] = check_admin.user_id
            session['role'] = check_admin.role
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html',error="Invalid credentials")






# SIGNUP
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
            return render_template('home.html')

        if role == 'staff':
            is_approved = False
        else:
            is_approved = True

        user_details = user_model(
            username=username,
            email=email,
            password=password,
            role=role,
            is_approved=is_approved
        )

        db.session.add(user_details)
        db.session.commit()

        return render_template('home.html')





# DASHBOARDS
@app.route('/user_dashboard',methods=['GET','POST'])
def user_dashboard():
    if 'role' not in session or session['role'] != 'user':
        return redirect(url_for('user_login'))
    return render_template('user_dashboard.html')


@app.route('/admin_dashboard',methods=['GET','POST'])
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html')


@app.route('/staff_dashboard',methods=['GET','POST'])
def staff_dashboard():
    if 'role' not in session or session['role'] != 'staff':
        return redirect(url_for('staff_login'))
    return render_template('staff_dashboard.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))




# @app.route('/search/<string:name>',methods=['GET'])
# def search(name):
#     return render_template('search.html')






# @app.route('/staff_register',methods=['GET','POST'])
# def staff_register():
#     if request.method=='GET':
#         return render_template('staff_register.html')
#     elif request.method=='POST':
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         check_staff = staff_model.query.filter_by(email=email).first()

#         if check_staff:
#             return render_template('login.html')
#         elif not check_staff:
#             user_details = staff_model(username=username,email=email,password=password,role='user')
#             db.session.add(user_details)
#             db.session.commit()
#             return render_template('login.html')




app.run(debug=True)