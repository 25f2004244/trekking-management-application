from flask import Flask, render_template,redirect,url_for,request,session
from model import db, user as user_model , trek as trek_model , booking as booking_model


app = Flask(__name__)
app.secret_key='trek-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

# users = user_model.query.all()
# for user in users:
#     user.is_active = True
# db.session.commit()




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
        check_user = user_model.query.filter_by(email=email,password=password,role='user',is_active=True).first()

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

        check_staff = user_model.query.filter_by(email=email,password=password,role='staff',is_active=True).first()

        if check_staff:
            if not (check_staff.is_approved):
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

        user_details = user_model(username=username,email=email,password=password,role=role,is_approved=is_approved)

        db.session.add(user_details)
        db.session.commit()

        return render_template('home.html')





# DASHBOARDS
@app.route('/user_dashboard',methods=['GET','POST'])
def user_dashboard():
    if 'role' not in session or session['role'] != 'user':
        return redirect(url_for('user_login'))
    return render_template('user_dashboard.html')




@app.route('/staff_dashboard',methods=['GET','POST'])
def staff_dashboard():
    if 'role' not in session or session['role'] != 'staff':
        return redirect(url_for('staff_login'))
    return render_template('staff_dashboard.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))







@app.route('/admin_dashboard',methods=['GET','POST'])
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))


    section=request.args.get('section','dashboard')
    data = None
    approved_staff = user_model.query.filter_by(role='staff', is_approved=True,is_active=True).all()
    not_approved_staff = user_model.query.filter_by(role='staff', is_approved=False,is_active=True).all()
    blacklisted_staff = user_model.query.filter_by(role='staff', is_active=False).all()

    blacklisted_users = user_model.query.filter_by(role='user', is_active=False).all()


    total_users = user_model.query.filter_by(role='user',is_active=True).count()
    # users = user_model.query.filter_by(role='user',is_active=True).all()

    total_staff = user_model.query.filter_by(role='staff',is_active=True,is_approved=True).count()

    total_treks = trek_model.query.count()
    # treks = trek_model.query.all()

    total_bookings = booking_model.query.count()
    # bookings = booking_model.query.all()


    if section == 'users':
        data = user_model.query.filter_by(role='user',is_active=True).all()

    elif section == 'staff':
        data = user_model.query.filter_by(role='staff').all()


    elif section == 'bookings':
        data = booking_model.query.all()

    elif section == 'treks':
        data = trek_model.query.all()

    return render_template('admin_dashboard.html',section=section,data=data,total_users=total_users,total_staff=total_staff,total_treks=total_treks,total_bookings=total_bookings,approved_staff=approved_staff,not_approved_staff=not_approved_staff,blacklisted_staff=blacklisted_staff,blacklisted_users=blacklisted_users)


@app.route('/add_trek',methods=['POST'])
def add_trek():
    name = request.form['name']
    difficulty = request.form['difficulty']
    duration = request.form['duration']
    slots = request.form['slots']

    new_trek = trek_model(name=name,difficulty=difficulty,duration=duration,slots=slots,assigned_staff=1)
    db.session.add(new_trek)
    db.session.commit()
    return redirect(url_for('admin_dashboard', section='treks'))


@app.route('/approve_staff/<int:id>')
def approve_staff(id):
    user = db.session.get(user_model, id)
    user.is_approved = True
    db.session.commit()
    return redirect(url_for('admin_dashboard', section='staff'))

@app.route('/remove_staff/<int:id>')
def remove_staff(id):
    user = db.session.get(user_model,id)
    user.is_approved = False
    db.session.commit()
    return redirect(url_for('admin_dashboard',section='staff'))

@app.route('/reject_staff/<int:id>',methods=['POST'])
def reject_staff(id):
    user = db.session.get(user_model,id)
    user.is_approved = False
    db.session.commit()
    return redirect(url_for('admin_dashboard' , section='staff'))


@app.route('/blacklist/<int:id>')
def blacklist(id):
    user = db.session.get(user_model,id)
    if user.role=='staff':
        user.is_active = False
        db.session.commit()
        return redirect(url_for('admin_dashboard', section='staff'))
    elif user.role=='user':
        user.is_active=False
        db.session.commit()
        return redirect(url_for('admin_dashboard',section='users'))


@app.route('/remove_staff_blacklist/<int:id>')
def remove_staff_blacklist(id):
    user = db.session.get(user_model,id)
    user.is_active = True
    db.session.commit()
    return redirect(url_for('admin_dashboard' , section='staff'))

@app.route('/remove_user_blacklist/<int:id>')
def remove_user_blacklist(id):
    user = db.session.get(user_model,id)
    user.is_active = True
    db.session.commit()
    return redirect(url_for('admin_dashboard' , section='users'))



@app.route('/delete_trek/<int:id>')
def delete_trek(id):
    trek = db.session.get(user_model, id)
    db.session.delete(trek)
    db.commit()
    return redirect(url_for('admin_dashboard', section='treks'))




@app.route('/trek_manage')
def trek_manage():
    return render_template("trek_manage")


@app.route('/staff_manage')
def staff_manage():
    return render_template("staff_manage")


@app.route('/user_manage')
def user_manage():
    return render_template("user_manage")


@app.route('/bookings_manage')
def bookings_manage():
    return render_template("bookings_manage")












app.run(debug=True)