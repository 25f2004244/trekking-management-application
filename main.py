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


with app.app_context():
    username = 'admin'
    role = 'admin'
    password= 'admin'
    email = 'admin@gmail.com'
    check_admin=user_model.query.filter_by(email=email,role=role).first()
    if not check_admin:
        admin_details = user_model(username=username,email=email,password=password, role=role,is_approved=True)
        db.session.add(admin_details)
        db.session.commit()


@app.route("/")
def home():
    return render_template('home.html')




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

        check_staff = user_model.query.filter_by(email=email,password=password,role='staff',is_active=True,is_approved=True).first()

        if check_staff:
            if not (check_staff.is_approved):
                return render_template('staff_login.html', error="Wait for admin approval")

            session['user_id'] = check_staff.user_id
            session['role'] = check_staff.role
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
    
    total_staff = user_model.query.filter_by(role='staff',is_active=True,is_approved=True).count()
    approved_staff = user_model.query.filter_by(role='staff', is_approved=True,is_active=True).all()
    not_approved_staff = user_model.query.filter_by(role='staff', is_approved=False,is_active=True).all()
    blacklisted_staff = user_model.query.filter_by(role='staff', is_active=False).all()

    blacklisted_users = user_model.query.filter_by(role='user', is_active=False).all()
    total_users = user_model.query.filter_by(role='user',is_active=True).count()

    total_treks = trek_model.query.count()

    total_bookings = booking_model.query.count()

    if section == 'users':
        data = user_model.query.filter_by(role='user',is_active=True).all()

    elif section == 'staff':
        data = user_model.query.filter_by(role='staff').all()

    elif section == 'bookings':
        data = trek_model.query.order_by(trek_model.trek_id.desc()).all()

    elif section == 'treks':
        data = trek_model.query.all()

    return render_template('admin_dashboard.html',section=section,data=data,total_users=total_users,total_staff=total_staff,total_treks=total_treks,total_bookings=total_bookings,approved_staff=approved_staff,not_approved_staff=not_approved_staff,blacklisted_staff=blacklisted_staff,blacklisted_users=blacklisted_users)


@app.route('/add_trek',methods=['POST'])
def add_trek():
    name = request.form['name']
    difficulty = request.form['difficulty']
    duration = request.form['duration']
    slots = request.form['slots']

    staff_id=request.form.get('staff_id')
    if staff_id=="":
        staff_id=None
    location=request.form.get('location')
    if not location:
        location = "to be announced"
    

    new_trek = trek_model(name=name,difficulty=difficulty,duration=duration,slots=slots,assigned_staff=staff_id,status='open',location=location)
    db.session.add(new_trek)
    db.session.commit()
    return redirect(url_for('admin_dashboard', section='treks'))


@app.route('/assign_staff/<int:trek_id>', methods=['POST'])
def assign_staff(trek_id):
    staff_id = request.form.get('staff_id')

    trek = trek_model.query.get(trek_id)

    if staff_id:
        trek.assigned_staff = int(staff_id)
        db.session.commit()

    return redirect(url_for('admin_dashboard',section='treks'))


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



@app.route('/delete_trek/<int:id>',methods=['POST'])
def delete_trek(id):
    trek = db.session.get(trek_model, id)
    if not trek:
        return 'Trek Not Found'
    db.session.delete(trek)
    db.session.commit()
    return redirect(url_for('admin_dashboard', section='treks'))








@app.route('/user_dashboard',methods=['GET','POST'])
def user_dashboard():
    if 'role' not in session or session['role'] != 'user':
        return redirect(url_for('user_login'))

    section = request.args.get('section','dashboard')
    data=None

    user=user_model.query.get(session['user_id'])

    bookings=booking_model.query.filter_by(user_id=session['user_id']).all()
    user_treks = [b.trek_id for b in bookings]

    if request.method == 'POST' and section == 'settings':

        if 'update_username' in request.form:
            user.username = request.form.get('username')

        elif 'update_email' in request.form:
            new_email = request.form.get('email')
            existing = user_model.query.filter_by(email=new_email).first()

            if existing and existing.user_id != user.user_id:
                return "Email already exists!"

            user.email = new_email

        elif 'update_password' in request.form:
            user.password = request.form.get('password')

        db.session.commit()

        return redirect(url_for('user_dashboard', section='settings'))

    if section == 'treks':
        data=trek_model.query.all()
   
    return render_template('user_dashboard.html',section=section,data=data,bookings=bookings,user_treks=user_treks,user=user)


@app.route('/book_trek/<int:id>', methods=['POST'])
def book_trek(id):
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    existing = booking_model.query.filter_by(
        user_id=session['user_id'],
        trek_id=id
    ).first()

    if existing:
        return "Already booked"

    t = trek_model.query.get(id)
    if not t:
        return 'Trek Not Found'
    if t.status != 'open':
        return "Booking not allowed for this trek"
    approved_count = booking_model.query.filter_by(trek_id=id,booking_status='approved').count()

    if approved_count >= t.slots:
        return "No slots available"
    
    new_booking = booking_model(user_id=session['user_id'],trek_id=id,booking_status='pending')

    db.session.add(new_booking)
    db.session.commit()

    return redirect(url_for('user_dashboard', section='treks'))








@app.route('/staff_dashboard',methods=['GET','POST'])
def staff_dashboard():
    if 'role' not in session or session['role']!='staff':
        return redirect(url_for('staff_login'))

    user = user_model.query.get(session['user_id'])


    section = request.args.get('section','dashboard')
    data=None
    if request.method == 'POST' and section == 'settings':

        if 'update_username' in request.form:
            user.username = request.form.get('username')

        elif 'update_email' in request.form:
            new_email = request.form.get('email')
            existing = user_model.query.filter_by(email=new_email).first()

            if existing and existing.user_id != user.user_id:
                return "Email already exists!"

            user.email = new_email

        elif 'update_password' in request.form:
            user.password = request.form.get('password')

        db.session.commit()

        return redirect(url_for('staff_dashboard', section='dashboard'))
    

    if section=='treks':
        data=trek_model.query.filter_by(assigned_staff=session['user_id']).all()


    return render_template('staff_dashboard.html',data=data,section=section,user=user)





@app.route('/update_slots_staff/<int:id>', methods=['POST'])
def update_slots_staff(id):
    trek = trek_model.query.filter_by(
        trek_id=id,
        assigned_staff=session['user_id']
    ).first()

    if trek:
        slots = int(request.form['slots'])
        if slots<1:
            return "Invalid Slots!"
        trek.slots = slots
        db.session.commit()

    return redirect(url_for('staff_dashboard', section='treks'))


@app.route('/update_slots_admin/<int:id>', methods=['POST'])
def update_slots_admin(id):
    trek = trek_model.query.filter_by(trek_id=id).first()

    if not trek:
        return "Trek not found"

    slots = int(request.form['slots'])

    if slots < 1:
        return "Invalid slot value"

    trek.slots = slots
    db.session.commit()

    return redirect(url_for('admin_dashboard', section='treks'))


@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):

    trek = trek_model.query.filter_by(trek_id=id).first()
    if not trek:
        return "Trek not found"

    if session['role'] == 'staff':
        if trek.assigned_staff != session['user_id']:
            return "Unauthorized"

    trek.status = request.form['status']
    db.session.commit()

    # 🔄 redirect based on role
    if session['role'] == 'staff':
        return redirect(url_for('staff_dashboard', section='treks'))

    elif session['role'] == 'admin':
        return redirect(url_for('admin_dashboard', section='treks'))

    return "Unauthorized"



@app.route('/update_booking_status/<int:id>', methods=['POST'])
def update_booking_status(id):

    booking = booking_model.query.get(id)

    if not booking:
        return "Booking not found"

    if session['role'] == 'staff':
        if booking.trek.assigned_staff != session['user_id']:
            return "Unauthorized"

    new_status = request.form['status']

    if new_status == 'approved':
        approved_count = booking_model.query.filter_by(
            trek_id=booking.trek_id,
            booking_status='approved'
        ).count()
        if booking.trek.status != 'open':
            return "Trek not open"

        if approved_count >= booking.trek.slots:
            return "No slots available"

    booking.booking_status = new_status
    db.session.commit()

    if session['role'] == 'staff':
        return redirect(url_for('staff_dashboard', section='treks'))

    elif session['role'] == 'admin':
        return redirect(url_for('admin_dashboard', section='bookings'))

    return "Unauthorized"




app.run(debug=True)