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



@app.route("/")
def home():
    return render_template('home.html')



@app.route('/home/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       

        cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
        cursor.nextset()
        user = cursor.fetchone()


        if user and user['password'] == password:
            session['user_id'] = user['id']
            return redirect('/user_dashboard')
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

        return redirect('/home/user_login')

    return render_template('signup.html', role='user')


@app.route('/user_dashboard')
def user_dashboard():
    user_id = session.get('user_id')
    if user_id:
        cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        cursor.execute("SELECT * FROM vaccination_center")
        centers = cursor.fetchall()

        return render_template('user_dashboard.html', user=user, centers=centers)
    else:
        return redirect('/home/user_login')


@app.route('/search_vaccination_centers')
def search_vaccination_centers():
    cursor.execute("SELECT * FROM vaccination_center")
    centers = cursor.fetchall()

    return render_template('vaccination_centers.html', centers=centers)


@app.route('/apply_vaccination_slot/<int:center_id>', methods=['GET', 'POST'])
def apply_vaccination_slot(center_id):
    user_id = session.get('user_id')
    if user_id:
        if request.method == 'POST':
            slot_date = request.form['slot_date']
            slot_time = request.form['slot_time']

            cursor.execute("SELECT * FROM vaccination_center WHERE id = %s", (center_id,))
            center = cursor.fetchone()

            if center:
                # Check available slots for the selected date
                cursor.execute("SELECT COUNT(*) AS slots_count FROM vaccination_slot WHERE center_id = %s AND slot_date = %s",
                               (center_id, slot_date))
                slots_count = cursor.fetchone()['slots_count']

                if slots_count < 10:
                    # Insert new slot
                    cursor.execute("INSERT INTO vaccination_slot (center_id, user_id, slot_date, slot_time) "
                                   "VALUES (%s, %s, %s, %s)",
                                   (center_id, user_id, slot_date, slot_time))
                    db.commit()

                    success_message = 'Vaccination slot booked successfully!'
                    return render_template('apply_slot.html', center=center, success_message=success_message)
                else:
                    error_message = 'No available slots for the selected date.'
                    return render_template('apply_slot.html', center=center, error_message=error_message)
            else:
                error_message = 'Invalid vaccination center.'
                return redirect('/search_vaccination_centers')

        cursor.execute("SELECT * FROM vaccination_center WHERE id = %s", (center_id,))
        center = cursor.fetchone()

        if center:
            return render_template('apply_slot.html', center=center)
        else:
            return redirect('/search_vaccination_centers')
    else:
        return redirect('/home/user_login')




@app.route('/login/admin', methods=['GET', 'POST'])

def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        
        if username == 'admin' and password == 'admin123':
            
            return redirect(url_for('admin_dashboard'))

        flash('Invalid username or password', 'error')

   
    return render_template('admin_login.html')





@app.route('/admin_dashboard')
def admin_dashboard():
    admin_id = session.get('admin_id')
    if admin_id:
        cursor.execute("SELECT * FROM admin WHERE id = %s", (admin_id,))
        admin = cursor.fetchone()

        cursor.execute("SELECT vaccination_center.id, vaccination_center.name, "
                       "COUNT(vaccination_slot.id) AS slots_count "
                       "FROM vaccination_center "
                       "LEFT JOIN vaccination_slot ON vaccination_center.id = vaccination_slot.center_id "
                       "GROUP BY vaccination_center.id, vaccination_center.name")
        dosage_details = cursor.fetchall()

        return render_template('admin_dashboard.html', admin=admin, dosage_details=dosage_details)
    else:
        return redirect('/login/admin')


@app.route('/add_vaccination_center', methods=['GET', 'POST'])
def add_vaccination_center():
    if request.method == 'POST':
        name = request.form['name']
        working_hours = request.form['working_hours']

        cursor.execute("INSERT INTO vaccination_center (name, working_hours) VALUES (%s, %s)",
                       (name, working_hours))
        db.commit()

        return redirect('/admin_dashboard')

    return render_template('add_vaccination_center.html')


@app.route('/remove_vaccination_center/<int:center_id>')
def remove_vaccination_center(center_id):
    cursor.execute("DELETE FROM vaccination_center WHERE id = %s", (center_id,))
    db.commit()

    return redirect('/admin_dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
