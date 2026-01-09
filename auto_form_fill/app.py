from flask import Flask, render_template, request, redirect, flash, session
import json, os
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)
app.secret_key = "secret123"

USERS_FILE = "users.json"
UPLOAD_ROOT = "static/uploads"

os.makedirs(UPLOAD_ROOT, exist_ok=True)

# -------------------------------
# INIT USERS FILE
# -------------------------------
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

# -------------------------------
# LIGHTWEIGHT AI FIELD MODEL
# -------------------------------
FIELD_MODEL = {
    "full_name": ["name", "full", "applicant", "candidate", "student"],
    "email": ["email", "mail", "e-mail"],
    "phone": ["phone", "mobile", "contact", "number"],
    "address": ["address", "location", "residence", "permanent"],
    "photo": ["photo", "image", "passport", "picture"],
    "income": ["income", "salary", "certificate", "proof"],
    "tenth": ["10th", "ssc", "secondary","10th Result","tenth_result"],
    "twelfth": ["12th", "hsc", "higher", "intermediate","12th Result","twelfth_result"]
}
def extract_text(el):
    attrs = [
        el.get_attribute("name"),
        el.get_attribute("id"),
        el.get_attribute("placeholder"),
        el.get_attribute("aria-label")
    ]
    return " ".join([a.lower() for a in attrs if a])

def predict_field(text):
    scores = {}
    for field, keywords in FIELD_MODEL.items():
        scores[field] = sum(1 for kw in keywords if kw in text)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else None

# -------------------------------
# AUTH ROUTES
# -------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open(USERS_FILE) as f:
            users = json.load(f)

        if username in users:
            flash("Account already exists")
            return redirect('/login')

        users[username] = password
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)

        os.makedirs(f"{UPLOAD_ROOT}/{username}", exist_ok=True)

        session['user'] = username
        flash("Account created successfully")
        return redirect('/')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with open(USERS_FILE) as f:
            users = json.load(f)

        if users.get(username) == password:
            session['user'] = username
            flash("Login successful")
            return redirect('/')

        flash("Invalid credentials")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# -------------------------------
# FORM FILLING PAGE
# -------------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect('/login')

    user = session['user']
    data_file = f"user_data_{user}.json"
    upload_dir = f"{UPLOAD_ROOT}/{user}"
    os.makedirs(upload_dir, exist_ok=True)

    data = None
    if os.path.exists(data_file):
        with open(data_file) as f:
            data = json.load(f)

    if request.method == 'POST':
        data = {
            "full_name": "",
            "email": "",
            "phone": "",
            "address": "",
            "documents": {}
        }
        if os.path.exists(data_file):
            with open(data_file) as f:
                data = json.load(f)

        if request.method == 'POST':
        # Update text fields
            data["full_name"] = request.form.get('full_name')
            data["email"] = request.form.get('email')
            data["phone"] = request.form.get('phone')
            data["address"] = request.form.get('address')

        for doc in ['photo', 'tenth', 'twelfth', 'income']:
            file = request.files.get(doc)

            if file and file.filename:
                path = os.path.join(upload_dir, file.filename)
                file.save(path)
                data["documents"][doc] = path

        with open(data_file, 'w') as f:
            json.dump(data, f, indent=4)

        flash("Data saved successfully")

    return render_template('index.html', data=data, user=user)

# -------------------------------
# AI FORM AUTO FILL
# -------------------------------
@app.route('/fill', methods=['POST'])
def fill():
    if 'user' not in session:
        return redirect('/login')

    url = request.form['form_url']
    user = session['user']
    data_file = f"user_data_{user}.json"

    if not os.path.exists(data_file):
        flash("No data found")
        return redirect('/')

    with open(data_file) as f:
        data = json.load(f)

    driver = webdriver.Chrome()
    driver.get(url)

    inputs = driver.find_elements(By.XPATH, "//input | //textarea")

    for el in inputs:
        text = extract_text(el)
        field = predict_field(text)

        if not field:
            continue

        if el.get_attribute("type") == "file":
            if field in data["documents"]:
                el.send_keys(os.path.abspath(data["documents"][field]))
        else:
            if field in data:
                el.send_keys(data[field])

    flash("Form filled using AI")
    return redirect('/')


@app.route('/load')
def load():
    if 'user' not in session:
        flash("Please login first")
        return redirect("/login")

    user = session['user']
    data_file = f"user_data_{user}.json"

    if not os.path.exists(data_file):
        flash("No saved data found")
        return redirect('/')

    with open(data_file) as f:
        data = json.load(f)

    flash("Data loaded successfully")
    return render_template('index.html', data=data, user=user)


@app.route('/delete')
def delete():
    if 'user' not in session:
        flash("Please login first")
        return redirect("/login")

    user = session['user']
    data_file = f"user_data_{user}.json"

    if os.path.exists(data_file):
        os.remove(data_file)
        flash("User data deleted successfully")
    else:
        flash("No data to delete")

    return redirect('/')


# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
