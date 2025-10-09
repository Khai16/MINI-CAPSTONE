from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def landing_page():
    # render the welcome page
    return render_template('Welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # TODO: replace placeholder auth with real verification (DB / hashing)
        if email and password:
            return redirect(url_for('dashboard_page'))
        return render_template('Login.html', error='Invalid credentials')
    return render_template("Login.html")

@app.route('/signup_page', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if username and email and password:
            # on successful signup redirect to login (or dashboard)
            return redirect(url_for('login_page'))
        return render_template('signup.html', error='Please fill all required fields')
    return render_template('signup.html')

@app.route('/aboutus')
def aboutUs_page():
    return render_template("AboutUs.html")


@app.route('/homepage') # / acts as the landing page
def homepage_page():
    return render_template("Homepage.html")


# Feature pages
@app.route('/dashboard_page', methods=['GET', 'POST'])
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
        # handle form submission here later
        return redirect(url_for('consultation_page'))
    return render_template('consultation.html')


@app.route('/form', methods=['GET', 'POST'])
def form_page():
    if request.method == 'POST':
        # process submitted form data
        return redirect(url_for('dashboard_page'))
    return render_template('form.html')


@app.route('/symptom-checker')
def symptom_checker_page():
    return render_template('symptom_checker.html')


@app.route('/emergency')
def emergency_contacts_page():
    return render_template('emergency.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    if request.method == 'POST':
        # capture feedback submission
        return redirect(url_for('dashboard_page'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True) # to easily changes