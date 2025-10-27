from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime
import pymysql

app = Flask(__name__)

app.secret_key = "supersecretkey123"

connection =  pymysql.connect(
        host='localhost',
        user='root',
        password='@Francisco1146',
        database='medical',
        cursorclass=pymysql.cursors.DictCursor
        )

cursor = connection.cursor(pymysql.cursors.DictCursor)

#landing
@app.route("/")
def landing_page():
        return render_template("Welcome.html")

#login
@app.route("/login")
def login_page():
        return render_template("Login.html")

@app.route('/loginAdmin_page')
def loginAdmin_page():
    return render_template('loginAdmin.html')

@app.route('/dashboardAdmin_page')  
def dashboardAdmin_page():
    return render_template('dashboardAdmin.html')

@app.route('/dashboard_page')  # allow GET by default
def dashboard_page():
    return render_template('dashboard.html')

#SignUp
@app.route("/signup_page")
def signup_page():
        return render_template("signup.html")

@app.route("/signupAdmin_page")
def signupAdmin_page():
    return render_template("signupAdmin.html")

#AboutUs
@app.route('/aboutus')
def aboutUs_page():
        return render_template("AboutUs.html")

#Emegency
@app.route('/emergency')
def emergency_contacts_page():
        return render_template('emergency.html')

#homepage
@app.route('/homepage') 
def homepage_page():
        return render_template("Homepage.html")

#Feedback
@app.route("/feedback")
def feedback_page():
    return render_template("feedback.html")


@app.route("/home_page")
def home_page():
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        users = cursor.fetchall()
        return render_template("Homepage.html", users=users)

@app.route("/consultation_page")
def consultation_page():
       return render_template("consultation.html")

        
#LoginAdmin
from flask import session

@app.route('/loginAdmin_process', methods=['POST'])
def loginAdmin_process():
    email = request.form.get('email')
    password = request.form.get('password')

    sql = "SELECT * FROM admin WHERE email = %s AND password = %s"
    cursor.execute(sql, (email, password))
    account = cursor.fetchone()

    if account:
        session['admin_id'] = account['admin_id']
        session['admin_name'] = account['name']
        return redirect(url_for('dashboardAdmin_page'))
    else:
        error = "Invalid email or password."
        return render_template('loginAdmin.html', error=error)

#LoginUser
@app.route('/login_process', methods=['POST'])
def login_process():
        email = request.form.get('email')
        password = request.form.get('password')

        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(sql, (email, password))
        account = cursor.fetchone()

        if account:
            return redirect (url_for('homepage_page'))
        else:
            return redirect(url_for('login_page'))
        
#SignUP as User        
@app.route('/signup_process', methods=['POST'])
def signup_process():
        name = request.form.get('username')
        gender = request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
         
        if password == confirm_password:
                sql = "INSERT INTO users (name, gender, email, password)  VALUES (%s, %s, %s, %s)"
                cursor.execute(sql,(name, gender, email, confirm_password))
                connection.commit()
                return redirect(url_for('login_page'))
        else:
               return redirect(url_for('signup.html'))
        
#SignUp as Admin
@app.route('/signupAdmin_process', methods=['GET', 'POST'])
def signupAdmin_process():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        access_code = request.form.get('access_code')

        SECRET_CODE = "PHINMAADMIN2025"

        if access_code != SECRET_CODE:
            return render_template('signupAdmin.html', error="❌ Invalid Admin Access Code")

        if password != confirm_password:
            return render_template('signupAdmin.html', error="❌ Passwords do not match")

        sql = "INSERT INTO admin (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, password))
        connection.commit()

        return redirect(url_for('loginAdmin_page'))
    
    return render_template('signupAdmin.html')
        
    # Feature pages
@app.route('/dashboard_process', methods=['POST'])
def dashboard_():
        if request.method == 'POST':
            # handle login logic here
            return render_template('dashboard.html')
        return redirect(url_for('login_page'))

@app.route('/dashboardAdmin_process')
def dashboardAdmin_():
    # ✅ Check if admin is logged in
    if 'admin_id' not in session:
        return redirect(url_for('loginAdmin_page'))

    admin_name = session.get('admin_name', 'Admin')

    try:
        # ✅ Get total users
        cursor.execute("SELECT COUNT(*) AS total_users FROM users")
        total_users = cursor.fetchone()['total_users']

        # ✅ Get total consultations
        cursor.execute("SELECT COUNT(*) AS total_consults FROM consultations")
        total_consults = cursor.fetchone()['total_consults']

        # ✅ Get total feedbacks
        cursor.execute("SELECT COUNT(*) AS total_feedback FROM feedback")
        total_feedback = cursor.fetchone()['total_feedback']

        # ✅ Fetch all users
        cursor.execute("SELECT user_id, name, email FROM users ORDER BY user_id DESC")
        users = cursor.fetchall()

        # ✅ Fetch all consultations
        cursor.execute("SELECT name, role, mood, symptom, pain, contact FROM consultations ORDER BY id DESC")
        consultations = cursor.fetchall()

        # ✅ Fetch all feedbacks
        cursor.execute("SELECT name, email, rating, feedback FROM feedback ORDER BY id DESC")
        feedbacks = cursor.fetchall()

    except Exception as e:
        print("⚠️ SQL ERROR:", e)
        total_users = total_consults = total_feedback = 0
        users = consultations = feedbacks = []

    print("✅ Dashboard Data:", total_users, total_consults, total_feedback)

    return render_template(
        'dashboardAdmin.html',
        admin_name=admin_name,
        total_users=total_users,
        total_consults=total_consults,
        total_feedback=total_feedback,
        users=users,
        consultations=consultations,
        feedbacks=feedbacks
    )



@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    connection.commit()
    flash("User deleted successfully.")
    return redirect(url_for('dashboardAdmin_page'))


@app.route('/logout')
def logout():
    flash("You have been logged out.")
    return redirect(url_for('loginAdmin_page'))


@app.route('/bulletin')
def health_bulletin_page():
        bulletins = [
            {"title": "Blood Donation Drive",
            "description": "Join our annual blood donation to save lives. Open for students and faculty.",
            "date": "2025-10-15",
            "category": "events",
            "link": "#"},
            {"title": "Mental Health Awareness Talk",
            "description": "Learn about stress management, mindfulness, and self-care with experts.",
            "date": "2025-11-08",
            "category": "announcements",
            "link": "#"},
            {"title": "Community Wellness Fair",
            "description": "Free check-ups, health talks, and wellness booths open for all students.",
            "date": "2025-12-02",
            "category": "events",
            "link": "#"}
        ]
        # compute month 
        for b in bulletins:
            dt = datetime.strptime(b["date"], "%Y-%m-%d")
            b["month"] = dt.strftime("%b")
            b["day"] = dt.day
        return render_template('bulletin.html', bulletins=bulletins)

@app.route('/consultation_process', methods=['POST'])
def consultation_process():
       name = request.form.get('name')
       role = request.form.get('role')
       feeling = request.form.get('feeling')
       symptom = request.form.get('symptoms')
       pain = request.form.get('urgency')
       contact = request.form.get('contact')

       sql = "INSERT INTO consultations (name, role, mood, symptom, pain, contact) VALUES (%s, %s, %s, %s, %s, %s)"
       cursor.execute("SELECT COUNT(*) AS total_consults FROM consultation")
       cursor.execute(sql,(name, role, feeling, symptom, pain, contact))
       connection.commit()
       result = cursor.fetchall()
       return redirect(url_for('home_page'))
       print(result)

@app.route("/feedback", methods=["POST"])
def feedback_process():
    name = request.form.get("name")
    email = request.form.get("email")
    rating = request.form.get("rate")
    feedback = request.form.get("feedback")

    sql = "INSERT INTO feedback (name, email, rating, feedback) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, email, rating, feedback))
    connection.commit()

    print("Feedback saved successfully!")
    flash("Thank you for your feedback!")
    return redirect(url_for("home_page"))

if __name__ == '__main__':
        app.run(debug=True)
