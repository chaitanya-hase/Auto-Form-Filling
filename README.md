#  AI-Powered Auto Form Filler

An intelligent web application that stores user personal details and documents securely and automatically fills online forms using AI-based field matching with Selenium.

---

##  Features

-  User Authentication (Signup / Login / Logout)
-  Store Personal Information
-  Upload & Manage Documents
-  AI-Based Field Detection for Form Filling
-  Auto-fill Online Forms using Selenium
-  Persistent User Data Storage
-  Clean & Professional UI

---

##  Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS  
- **Automation:** Selenium  
- **AI Logic:** Keyword-based intelligent field matching  
- **Storage:** JSON, File System  

---
## Requirements
```bash
Flask==2.3.3
selenium==4.15.2
Werkzeug==2.3.7
```

##  Installation & Setup

### 1️ Clone the Repository
```bash
- git clone https://github.com/your-username/auto-form-filler.git
- cd auto-form-filler
```
### Install Dependencies
```bash
- pip install -r requirements.txt
```
### Run the Application
```bash
- python app.py
```
### Open in Browser
```bash
- http://127.0.0.1:5000
```

### Project Structure
``` bash
auto-form-filler/
│
├── app.py
├── users.json
├── user_data_<username>.json
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── login.html
│   └── signup.html
│
└── static/
    ├── css/
    │   └── style.css
    └── uploads/
        └── <username>/
```




