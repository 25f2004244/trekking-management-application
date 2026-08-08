from flask import Flask, render_template,redirect,url_for,request,session
from model import db, user as user_model , trek as trek_model , booking as booking_model


app = Flask(__name__)
app.secret_key='trek-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

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




######################################## LOGIN ####################################################
@app.route('/user_login',methods=['GET','POST'])
def user_login():
    if request.method=='GET':
        return render_template('user_login.html')
    
    elif request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
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





######################################## SIGNUP ####################################################
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    
    elif request.method=='POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        if role not in ('user', 'staff'):
            return "Invalid role"
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







######################################## ADMIN ####################################################
@app.route('/admin_dashboard',methods=['GET','POST'])
def admin_dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))

    section=request.args.get('section','dashboard')
    search_query = request.args.get('search', '').strip()
    data = None
    total_staff = user_model.query.filter_by(role='staff',is_active=True,is_approved=True).count()
    total_users = user_model.query.filter_by(role='user',is_active=True).count()
    total_treks = trek_model.query.count()
    total_bookings = booking_model.query.count()

    name_filter = None
    if search_query:
        name_filter = (user_model.username.ilike(f'%{search_query}%')) | (user_model.email.ilike(f'%{search_query}%'))

    approved_staff_q = user_model.query.filter_by(role='staff', is_approved=True, is_active=True)
    not_approved_staff_q = user_model.query.filter_by(role='staff', is_approved=False, is_active=True)
    blacklisted_staff_q = user_model.query.filter_by(role='staff', is_active=False)

    if section == 'staff' and name_filter is not None:
        approved_staff = approved_staff_q.filter(name_filter).all()
        not_approved_staff = not_approved_staff_q.filter(name_filter).all()
        blacklisted_staff = blacklisted_staff_q.filter(name_filter).all()
    else:
        approved_staff = approved_staff_q.all()
        not_approved_staff = not_approved_staff_q.all()
        blacklisted_staff = blacklisted_staff_q.all()

    active_users_q = user_model.query.filter_by(role='user', is_active=True)
    blacklisted_users_q = user_model.query.filter_by(role='user', is_active=False)

    if section == 'users' and name_filter is not None:
        data = active_users_q.filter(name_filter).all()
        blacklisted_users = blacklisted_users_q.filter(name_filter).all()
    else:
        data = active_users_q.all()
        blacklisted_users = blacklisted_users_q.all()

    if section == 'treks':
        if search_query:
            data = trek_model.query.filter(
                (trek_model.name.ilike(f'%{search_query}%')) | (trek_model.location.ilike(f'%{search_query}%'))
            ).all()
        else:
            data = trek_model.query.all()

    elif section == 'bookings':
        if search_query:
            data = trek_model.query.filter(trek_model.name.ilike(f'%{search_query}%')).order_by(trek_model.trek_id.desc()).all()
        else:
            data = trek_model.query.order_by(trek_model.trek_id.desc()).all()

    return render_template('admin_dashboard.html',section=section,data=data,total_users=total_users,total_staff=total_staff,total_treks=total_treks,total_bookings=total_bookings,approved_staff=approved_staff,not_approved_staff=not_approved_staff,blacklisted_staff=blacklisted_staff,blacklisted_users=blacklisted_users,search_query=search_query)


@app.route('/add_trek',methods=['POST'])
def add_trek():
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    name = request.form['name']
    difficulty = request.form['difficulty']
    duration = int(request.form['duration'])
    slots = int(request.form['slots'])

    staff_id=request.form.get('staff_id')
    if staff_id:
        staff_id = int(staff_id)
    else:
        staff_id = None

    location=request.form.get('location')
    if not location:
        location = "to be announced"

    new_trek = trek_model(name=name,difficulty=difficulty,duration=duration,slots=slots,assigned_staff=staff_id,status='Open',location=location)
    db.session.add(new_trek)
    db.session.commit()
    return redirect(url_for('admin_dashboard', section='treks'))


@app.route('/approve_staff/<int:id>')
def approve_staff(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    user = db.session.get(user_model, id)
    user.is_approved = True
    db.session.commit()
    return redirect(url_for('admin_dashboard', section='staff'))


@app.route('/remove_staff/<int:id>')
def remove_staff(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    user = db.session.get(user_model,id)
    user.is_approved = False
    db.session.commit()
    return redirect(url_for('admin_dashboard',section='staff'))



@app.route('/blacklist/<int:id>')
def blacklist(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    user = db.session.get(user_model,id)
    if user.role=='staff':
        user.is_active = False
        db.session.commit()
        return redirect(url_for('admin_dashboard', section='staff'))
    elif user.role=='user':
        user.is_active=False
        db.session.commit()
        return redirect(url_for('admin_dashboard',section='users'))
    else:
        return "Cannot blacklist Admin!"


@app.route('/remove_staff_blacklist/<int:id>')
def remove_staff_blacklist(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    user = db.session.get(user_model,id)
    user.is_active = True
    db.session.commit()
    return redirect(url_for('admin_dashboard' , section='staff'))


@app.route('/remove_user_blacklist/<int:id>')
def remove_user_blacklist(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    user = db.session.get(user_model,id)
    user.is_active = True
    db.session.commit()
    return redirect(url_for('admin_dashboard' , section='users'))


@app.route('/delete_trek/<int:id>',methods=['POST'])
def delete_trek(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    trek = db.session.get(trek_model, id)
    db.session.delete(trek)
    db.session.commit()
    return redirect(url_for('admin_dashboard', section='treks'))




@app.route('/edit_trek/<int:trek_id>', methods=['GET', 'POST'])
def edit_trek(trek_id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect(url_for('admin_login'))
    trek = db.session.get(trek_model,trek_id)
    if not trek:
        return "Trek not found"
    
    staff = user_model.query.filter_by(role='staff', is_approved=True,is_active=True).all()

    if request.method == 'POST':
        trek.name = request.form.get('name')
        trek.location = request.form.get('location')
        trek.slots = int(request.form.get('slots'))
        trek.status = request.form.get('status')

        staff_id = request.form.get('staff_id')
        if staff_id:
            trek.assigned_staff = int(staff_id)
        else:
            trek.assigned_staff = None
        db.session.commit()
        return redirect(url_for('admin_dashboard', section='treks'))

    return render_template('edit_trek.html', trek=trek, staff=staff)








######################################## USER ####################################################
@app.route('/user_dashboard',methods=['GET','POST'])
def user_dashboard():
    if 'role' not in session or session['role'] != 'user':
        return redirect(url_for('user_login'))

    section = request.args.get('section','dashboard')
    data=None

    user=user_model.query.get(session['user_id'])
    bookings=booking_model.query.filter_by(user_id=session['user_id']).all()
    user_treks = [b.trek_id for b in bookings if b.booking_status in ('pending', 'approved')]

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

    search_query = request.args.get('search', '').strip()

    if section == 'treks':
        if search_query:
            data = trek_model.query.filter(
                (trek_model.name.ilike(f'%{search_query}%')) | (trek_model.location.ilike(f'%{search_query}%'))
            ).all()
        else:
            data = trek_model.query.all()

    return render_template('user_dashboard.html',section=section,data=data,bookings=bookings,user_treks=user_treks,user=user,search_query=search_query)



@app.route('/book_trek/<int:id>', methods=['POST'])
def book_trek(id):
    if 'role' not in session or session['role'] != 'user':
        return redirect(url_for('user_login'))

    existing = booking_model.query.filter_by(user_id=session['user_id'],trek_id=id).first()

    if existing:
        return "Already booked"

    t = trek_model.query.get(id)
    if not t:
        return 'Trek Not Found'
    if t.status != 'Open':
        return "Booking not allowed for this trek"
    approved_count = booking_model.query.filter_by(trek_id=id,booking_status='approved').count()

    if approved_count >= t.slots:
        return "No slots available"
    
    new_booking = booking_model(user_id=session['user_id'],trek_id=id,booking_status='pending')

    db.session.add(new_booking)
    db.session.commit()
    return redirect(url_for('user_dashboard', section='treks'))







######################################## STAFF ####################################################
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

    search_query = request.args.get('search', '').strip()
    if section=='dashboard':
        data=trek_model.query.filter_by(assigned_staff=session['user_id']).all()
    elif section=='treks':
        base_query = trek_model.query.filter_by(assigned_staff=session['user_id'])
        if search_query:
            base_query = base_query.filter(
                (trek_model.name.ilike(f'%{search_query}%')) | (trek_model.location.ilike(f'%{search_query}%'))
            )
        data = base_query.all()

    return render_template('staff_dashboard.html',data=data,section=section,user=user,search_query=search_query)



@app.route('/update_slots_staff/<int:id>', methods=['POST'])
def update_slots_staff(id):
    if 'role' not in session or session['role'] != 'staff':
        return redirect(url_for('staff_login'))
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


@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    if 'role' not in session or session['role'] not in ('staff', 'admin'):
        return redirect(url_for('home'))

    trek = trek_model.query.filter_by(trek_id=id).first()
    if not trek:
        return "Trek not found"
    if session['role'] == 'staff':
        if trek.assigned_staff != session['user_id']:
            return "Unauthorized"

    trek.status = request.form['status']
    db.session.commit()

    if session['role'] == 'staff':
        return redirect(url_for('staff_dashboard', section='treks'))
    elif session['role'] == 'admin':
        return redirect(url_for('admin_dashboard', section='treks'))



@app.route('/update_booking_status/<int:id>', methods=['POST'])
def update_booking_status(id):
    if 'role' not in session or session['role'] not in ('staff', 'admin'):
        return redirect(url_for('home'))

    booking = booking_model.query.get(id)
    if not booking:
        return "Booking not found"

    if session['role'] == 'staff':
        if booking.trek.assigned_staff != session['user_id']:
            return "Unauthorized"

    new_status = request.form['status']

    if new_status == 'approved':
        approved_count = booking_model.query.filter_by(trek_id=booking.trek_id,booking_status='approved').count()
        if booking.trek.status != 'Open':
            return "Trek not open"
        if approved_count >= booking.trek.slots:
            return "No slots available"

    booking.booking_status = new_status
    db.session.commit()

    if session['role'] == 'staff':
        return redirect(url_for('staff_dashboard', section='treks'))
    elif session['role'] == 'admin':
        return redirect(url_for('admin_dashboard', section='bookings'))



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


app.run(debug=True)