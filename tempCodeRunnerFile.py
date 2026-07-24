
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='GET':
        return render_template('signup.html')
    elif request.method=='POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        check_user = user_model.query.filter_by(email=email).first()
        print(check_user)
        if check_user:
            flash(f"{email} is already a user!")
            return render_template('login.html')
        else:
            user_details = user_model(username=username,email=email,password=password)
            db.session.add(user_details)
            db.session.commit()
            return render_template('login.html')
