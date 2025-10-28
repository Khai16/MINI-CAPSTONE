from flask import Flask, render_template, redirect, url_for, request, flash, session
from datetime import datetime
import pymysql

app = Flask(__name__)
app.secret_key = "supersecretkey123"

# --- DB connection
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='@Francisco1146',
    database='medical',
    cursorclass=pymysql.cursors.DictCursor
)

# Landing / static pages
@app.route("/")
def landing_page():
    return render_template("Welcome.html")

@app.route("/login")
def login_page():
    return render_template("Login.html")

@app.route('/loginAdmin_page')
def loginAdmin_page():
    return render_template('loginAdmin.html')

@app.route('/signup_page')
def signup_page():
    return render_template("signup.html")

@app.route("/signupAdmin_page")
def signupAdmin_page():
    return render_template("signupAdmin.html")

@app.route('/dashboardAdmin_page')
def dashboardAdmin_page():
    return redirect(url_for('dashboardAdmin_'))

@app.route('/dashboardUser_page')
def dashboardUser_page():
    return redirect(url_for('dashboardUser_'))


@app.route('/aboutus')
def aboutUs_page():
    return render_template("AboutUs.html")

@app.route('/emergency')
def emergency_contacts_page():
    return render_template('emergency.html')

@app.route('/homepage')
def homepage_page():
    return render_template("Homepage.html")

@app.route("/feedback", methods=['GET'])
def feedback_page():
    return render_template("feedback.html")

@app.route("/consultation_page")
def consultation_page():
    return render_template("consultation.html")



# --- Login / Signup processes ---

@app.route('/loginAdmin_process', methods=['POST'])
def loginAdmin_process():
    email = request.form.get('email')
    password = request.form.get('password')

    with connection.cursor() as cursor:
        sql = "SELECT * FROM admin WHERE email = %s AND password = %s"
        cursor.execute(sql, (email, password))
        account = cursor.fetchone()

    if account:
        session['admin_id'] = account['admin_id']
        session['admin_name'] = account['name']
        return redirect(url_for('dashboardAdmin_'))
    else:
        error = "Invalid email or password."
        return render_template('loginAdmin.html', error=error)
    

# USER LOGIN FORM
@app.route('/login_process', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    with connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(sql, (email, password))
        account = cursor.fetchone()

    if account:
     
        session['user_id'] = account.get('user_id')
        session['user_name'] = account.get('name')
        return redirect(url_for('homepage_page'))
    else:
        flash("Invalid credentials.")
        return redirect(url_for('login_page'))

# SIGNUP USER
@app.route('/signup_process', methods=['POST'])
def signup_process():
    name = request.form.get('username')
    gender = request.form.get('gender')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash("Passwords do not match.")
        return redirect(url_for('signup_page'))

    with connection.cursor() as cursor:
        sql = "INSERT INTO users (name, gender, email, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, gender, email, password))
        connection.commit()

    flash("Signup successful. Please log in.")
    return redirect(url_for('login_page'))


# sIGN UP ADMIN
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

        with connection.cursor() as cursor:
            sql = "INSERT INTO admin (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, email, password))
            connection.commit()

        return redirect(url_for('loginAdmin_page'))

    return render_template('signupAdmin.html')

@app.route('/dashboardUser_process')
def dashboardUser_():
    if 'user_name' not in session:
        flash("Please log in first.")
        return redirect(url_for('login_page'))

    user_name = session['user_name']

    with connection.cursor() as cursor:
        # Get user info
        cursor.execute("""
            SELECT name, gender, email
            FROM users
            WHERE name = %s
        """, (user_name,))
        user_info = cursor.fetchone()

        # Get consultation history by name
        cursor.execute("""
            SELECT consult_id, role, mood, symptom, pain, contact, created_at
            FROM consultations
            WHERE name = %s
            ORDER BY created_at DESC
        """, (user_name,))
        consultations = cursor.fetchall()

    return render_template(
        'dashboardUser.html',
        user_name=user_name,
        user_info=user_info,
        consultations=consultations
    )


# Protected dashboard renderer (computes totals)
@app.route('/dashboardAdmin_process')  # keeps the previous name; your login redirects here
def dashboardAdmin_():
    if 'admin_name' not in session:
        return redirect(url_for('loginAdmin_page'))

    admin_name = session['admin_name']

    with connection.cursor() as cursor:
        # total users
        cursor.execute("SELECT COUNT(*) AS users_count FROM users")
        users = cursor.fetchone().get('users_count', 0)

        # total feedback
        cursor.execute("SELECT COUNT(*) AS feedback_count FROM feedback")
        feedback = cursor.fetchone().get('feedback_count', 0)

        # total consultations
        cursor.execute("SELECT COUNT(*) AS consultations_count FROM consultations")
        consultations = cursor.fetchone().get('consultations_count', 0)

    return render_template(
        'dashboardAdmin.html',
        admin_name=admin_name,
        total_users=users,
        total_feedback=feedback,
        total_consultations=consultations
    )

# Delete user (admin)
@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        connection.commit()
    flash("User deleted successfully.")
    return redirect(url_for('dashboardAdmin_page'))

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('loginAdmin_page'))

# Bulletin
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
    for b in bulletins:
        dt = datetime.strptime(b["date"], "%Y-%m-%d")
        b["month"] = dt.strftime("%b")
        b["day"] = dt.day
    return render_template('bulletin.html', bulletins=bulletins)

# Consultation form processing
@app.route('/consultation_process', methods=['POST'])
def consultation_process():
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login_page'))

    name = session.get('user_name')
    role = request.form.get('role')
    feeling = request.form.get('feeling')
    symptom = request.form.get('symptoms')
    pain = request.form.get('urgency')
    contact = request.form.get('contact')

    with connection.cursor() as cursor:
        sql = """
            INSERT INTO consultations (name, role, mood, symptom, pain, contact, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(sql, (name, role, feeling, symptom, pain, contact))
        connection.commit()

    flash("Consultation request submitted.")
    return redirect(url_for('dashboardUser_'))

# Feedback processing (POST)
@app.route("/feedback", methods=["POST"])
def feedback_process():
    name = request.form.get("name")
    email = request.form.get("email")
    rating = request.form.get("rate")
    feedback_text = request.form.get("feedback")

    with connection.cursor() as cursor:
        sql = "INSERT INTO feedback (name, email, rating, feedback) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, email, rating, feedback_text))
        connection.commit()
    return redirect(url_for("home_page"))

# Home page that lists users (example)
@app.route("/home_page")
def home_page():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    return render_template("Homepage.html", users=users)


@app.route('/admin/users')
def admin_users():
    if 'admin_name' not in session:
        return redirect(url_for('loginAdmin_page'))

    with connection.cursor() as cursor:
        cursor.execute("SELECT user_id, name, gender, email FROM users")
        users = cursor.fetchall()

    return render_template(
        'dashboardAdmin.html',
        admin_name=session['admin_name'],
        view='users',
        users=users
    )


@app.route('/admin/consultations')
def admin_consultations():
    if 'admin_name' not in session:
        return redirect(url_for('loginAdmin_page'))

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM consultations")
        consultations = cursor.fetchall()

    return render_template(
        'dashboardAdmin.html',
        admin_name=session['admin_name'],
        view='consultations',
        consultations=consultations
    )


@app.route('/admin/feedback')
def admin_feedback():
    if 'admin_name' not in session:
        return redirect(url_for('loginAdmin_page'))

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, email, rating, feedback FROM feedback")
        feedback = cursor.fetchall()

    return render_template(
        'dashboardAdmin.html',
        admin_name=session['admin_name'],
        view='feedback',
        feedback=feedback
    )


if __name__ == '__main__':
    app.run(debug=True)
