from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime
import pymysql

app = Flask(__name__)

connection =  pymysql.connect(
            host='localhost',
            user='root',
            password='@Francisco1146',
            database='medical',
            cursorclass=pymysql.cursors.DictCursor
        )

cursor = connection.cursor(pymysql.cursors.DictCursor)

@app.route("/")
def landing_page():
        return render_template("Welcome.html")

@app.route("/login")
def login_page():
        return render_template("Login.html")

@app.route('/aboutus')
def aboutUs_page():
        return render_template("AboutUs.html")


@app.route('/homepage') 
def homepage_page():
        return render_template("Homepage.html")

@app.route("/signup_page")
def signup_page():
        return render_template("signup.html")

@app.route('/emergency')
def emergency_contacts_page():
        return render_template('emergency.html')


@app.route("/home_page")
def home_page():
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        users = cursor.fetchall()
        return render_template("Homepage.html", users=users)

@app.route('/login_process', methods=['POST'])
def login_process():
        email = request.form.get('email')
        password = request.form.get('password')

        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        cursor.execute(sql, (email, password))
        account = cursor.fetchone()

        if account:
            return redirect (url_for('home_page'))
        else:
            return redirect(url_for('login_page'))
        
@app.route('/signup_process', methods=['POST'])
def signup_process():
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')


            sql = "INSERT INTO users (user_name, email, password)  VALUES (%s, %s, %s)"
            cursor.execute(sql,(username, email, password))
            connection.commit()
            return redirect('login_page')
    # Feature pages
@app.route('/dashboard_page', methods=['POST'])
def dashboard_page():
        if request.method == 'POST':
            # handle login logic here
            return render_template('dashboard.html')
        return redirect(url_for('login_page'))


@app.route('/records')
def medical_records_page():
        return render_template('records.html')

    # Health Bulletin page 

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


    # Consultation page with form handling
@app.route('/consultation', methods=['GET', 'POST'])
def consultation_page():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            return render_template('consultation.html', success=True)

        return render_template('consultation.html')


@app.route('/feedback', methods=['POST'])
def feedback_page():
        if request.method == 'POST':
            # capture feedback submission
            return redirect(url_for('dashboard_page'))
        return render_template('feedback.html')

if __name__ == '__main__':
        app.run(debug=True)