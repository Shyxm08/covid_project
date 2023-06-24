from flask import Flask, render_template, request, redirect, session, url_for,flash
import mysql.connector
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)


db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='mydata'
)

cursor = db.cursor(dictionary=True)


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')



@app.route("/")
def home():
    return render_template('home.html')



# @app.route('/home/user_login', methods=['GET', 'POST'])
# def user_login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
       

#         cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
#         #cursor.nextset()
#         user = cursor.fetchone()


#         if user and user['password'] == password:
#             session['user_id'] = user['id']
#             return redirect(url_for('user_dashboard'))
#         else:
#             error = 'Invalid credentials. Please try again.'
#             return render_template('user_login.html', error=error)

#     return render_template('user_login.html')
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        users = cursor.fetchall()  # Consume the result set

        user = next((user for user in users if user['password'] == password), None)

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('user_dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('user_login.html', error=error)

    return render_template('user_login.html')




@app.route('/user_signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
        db.commit()

        return redirect(url_for('user_login'))

    return render_template('signup.html', role='user')


@app.route('/user_dashboard')
def user_dashboard():
    
    cursor.execute("SELECT id, name, working_hours, dosage_count FROM vaccination_center")
    vaccination_centers = cursor.fetchall()

    return render_template('user_dashboard.html', vaccination_centers=vaccination_centers)



@app.route('/apply_slot/<int:center_id>', methods=['GET', 'POST'])
def apply_slot(center_id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        date = request.form['date']
        time = request.form['time']

        
        dosage_count = 0 
        cursor.execute("SELECT dosage_count FROM vaccination_center WHERE id = %s", (center_id,))
        result = cursor.fetchone()
        if result is not None:
            dosage_count = result['dosage_count']

        if dosage_count > 0:
      
            cursor.execute("UPDATE vaccination_center SET dosage_count = dosage_count - 1 WHERE id = %s", (center_id,))
            db.commit()

            flash('Slot applied successfully! Please be there on time.', 'success')
            return redirect('/user_dashboard')

    
    cursor.execute("SELECT name, working_hours, dosage_count FROM vaccination_center WHERE id = %s", (center_id,))
    center = cursor.fetchone()

    return render_template('apply_slot.html', center=center)






@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM admin WHERE username = %s", (username,))
        admins = cursor.fetchall() 

        admin = next((admin for admin in admins if admin['password'] == password), None)

        if admin:
            session['admin_id'] = admin['id']
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('admin_login.html', error=error)

    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    admin_id = session.get('admin_id')
    if admin_id:
        cursor.execute("SELECT * FROM admin WHERE id = %s", (admin_id,))
        admin = cursor.fetchone()
        return render_template('admin_dashboard.html', admin=admin)
    else:
        return redirect('/login/admin')

@app.route('/dosage_details')
def dosage_details():
    cursor.execute("SELECT name, dosage_count FROM vaccination_center")
    dosage_details = cursor.fetchall()
    return render_template('dosage_details.html', dosage_details=dosage_details)




@app.route('/add_vaccination_centre', methods=['GET', 'POST'])
def add_vaccination_centre():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        working_hours = request.form['working_hours']

        cursor.execute("INSERT INTO vaccination_center (id, name, working_hours, dosage_count) "
                       "VALUES (%s, %s, %s, 10)", (id, name, working_hours))

        flash('Vaccination centre added successfully!', 'success')
        db.commit()
        return redirect('/admin_dashboard')

    return render_template('add_vaccination_centre.html')


@app.route('/remove_vaccination_centre', methods=['GET', 'POST'])
def remove_vaccination_centre():
    if request.method == 'POST':
       
        centre_id = request.form['centre_id']
        
       
        cursor.execute("DELETE FROM vaccination_center WHERE id = %s", (centre_id,))
        db.commit()  
        
        flash('Vaccination centre removed successfully!', 'success')
        return redirect('/admin_dashboard')
    
  
    return render_template('remove_vaccination_centre.html')




@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
