# 🏦 Bank Management System with Admin & User Authentication

This is a complete web-based banking system built using **HTML, CSS, JavaScript, Python (Flask)**, and **MySQL**. It supports secure login for both **users** and **admins**, and provides a functional **dashboard for transactions, PIN changes, and account management**.

---

## 📌 Features

### 🔐 Login System (User & Admin)
- Separate login for Users (via Account Number + PIN) and Admins (via Admin ID + Password)
- Credentials are securely stored and verified using MySQL
- Session management using `sessionStorage`

### 📝 User Dashboard
- View personal account details (name, contact, location, balance, etc.)
- Perform **credit** or **debit** transactions
- View **transaction history**
- Change PIN securely
- Logout option

### 🛠️ Admin Dashboard
- Login using Admin ID and password (stored in MySQL `admin` table)
- View **all user accounts**
- Search by **account number**
- View transactions by **account or date**
- Admin logout

---

## 💡 UI Highlights
- Responsive design with mobile-friendly layout
- Blurred background with transparent glassmorphism effect
- Styled alerts and messages (green for success, red for error)
- Clean dashboard with organized sections (details, transactions, PIN, etc.)

---

## 🚀 Getting Started

### 📁 Project Structure


---

## 🛠️ How to Use


---


Let me know if you'd like me to:
- Generate `db_config.py` sample code  
- Write the `requirements.txt`  
- Help with deployment instructions for Render, Heroku, or Replit


### 1. Clone the Repository
##path
app/
- ├── static/
- │ └── style.css # Global styles
- | |__ bank.img
- ├── templates/
- │ ├── register.html # User Registration Form
- │ ├── login.html # User Login Page
- │ ├── admin-login.html # Admin Login Page
- | ├── user-dashboard.html # User Dashboard
- │ └── admin-dashboard.html # Admin Dashboard
- ├── app.py # Flask app with routes and logic
- └── db_config.py # MySQL database connection setup

```bash

python app.py



