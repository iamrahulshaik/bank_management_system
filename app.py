from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import mysql.connector as db
import random

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# DB connection
con = db.connect(
    host="localhost",   
    user="root",
    password="mysql",
    database="bank",
    auth_plugin="mysql_native_password"
)

# -------------------- ROUTES --------------------

@app.route('/')
def role_selection():
    return render_template("index.html")

# -------------------- USER --------------------

@app.route('/user-login')
def user_login_page():
    return render_template("user-login.html")

@app.route('/user-dashboard')
def user_dashboard_page():
    return render_template("user-dashboard.html")



@app.route('/register-page')
def register_page():
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def register():
    data = request.form
    name, ac_type, contact, location, pin = data['name'].upper(), data['ac_type'].upper(), data['contact'], data['location'].upper(), data['pin']
    ac_number = str(random.randint(1000000000, 9999999999))
    amount = 0
    cur = con.cursor()
    try:
        cur.execute("INSERT INTO register (name, ac_type, contact, location, pin, ac_number, amount) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (name, ac_type, contact, location, pin, ac_number, amount))
        con.commit()
        return f"✅ Account Registered! Your Account No: {ac_number}"
    except Exception as e:
        return f"❌ Registration failed: {e}"
    finally:
        cur.close()





@app.route('/login', methods=['POST'])
def user_login():
    data = request.form
    ac_number, pin = data['ac_number'], data['pin']
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM register WHERE ac_number=%s AND pin=%s", (ac_number, pin))
    user = cur.fetchone()
    cur.close()
    if user:
        return jsonify({"status": "success", "data": user})
    return jsonify({"status": "fail", "message": "❌ Invalid account or PIN"})

@app.route('/credit', methods=['POST'])
def credit():
    data = request.form
    ac_number, amount = data['ac_number'], int(data['amount'])
    cur = con.cursor()
    try:
        cur.execute("UPDATE register SET amount = amount + %s WHERE ac_number = %s", (amount, ac_number))
        con.commit()
        cur.execute("SELECT amount FROM register WHERE ac_number = %s", (ac_number,))
        new_balance = cur.fetchone()[0]
        cur.execute("INSERT INTO transactions (ac_number, transaction_type, amount, balance_after) VALUES (%s, 'credit', %s, %s)",
                    (ac_number, amount, new_balance))
        con.commit()
        return f"✅ ₹{amount} credited. New balance: ₹{new_balance}"
    except Exception as e:
        con.rollback()
        return f"❌ Credit failed: {e}"
    finally:
        cur.close()

@app.route('/debit', methods=['POST'])
def debit():
    data = request.form
    ac_number, amount = data['ac_number'], int(data['amount'])
    cur = con.cursor()
    try:
        cur.execute("SELECT amount FROM register WHERE ac_number = %s", (ac_number,))
        balance = cur.fetchone()[0]
        if amount > balance:
            return "❌ Insufficient balance"
        cur.execute("UPDATE register SET amount = amount - %s WHERE ac_number = %s", (amount, ac_number))
        con.commit()
        cur.execute("SELECT amount FROM register WHERE ac_number = %s", (ac_number,))
        new_balance = cur.fetchone()[0]
        cur.execute("INSERT INTO transactions (ac_number, transaction_type, amount, balance_after) VALUES (%s, 'debit', %s, %s)",
                    (ac_number, amount, new_balance))
        con.commit()
        return f"✅ ₹{amount} debited. New balance: ₹{new_balance}"
    except Exception as e:
        con.rollback()
        return f"❌ Debit failed: {e}"
    finally:
        cur.close()


@app.route('/change-pin', methods=['POST'])
def change_pin():
    data = request.form
    ac_number = data['ac_number'].strip()
    old_pin = data['old_pin'].strip()
    new_pin = data['new_pin'].strip()

    cur = con.cursor()
    try:
        # Fetch the correct PIN from DB
        cur.execute("SELECT pin FROM register WHERE ac_number = %s", (ac_number,))
        record = cur.fetchone()

        if not record:
            return "❌ Account not found."

        # Compare as strings (to avoid type mismatch issues)
        if str(record[0]) != str(old_pin):
            return "❌ Old PIN is incorrect."

        # Update PIN
        cur.execute("UPDATE register SET pin = %s WHERE ac_number = %s", (new_pin, ac_number))
        con.commit()
        return "✅ PIN updated successfully."
    except Exception as e:
        con.rollback()
        return f"❌ Failed to update PIN: {e}"
    finally:
        cur.close()


@app.route('/transactions/<ac_number>')
def transactions(ac_number):
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM transactions WHERE ac_number = %s ORDER BY timestamp DESC", (ac_number,))
    return jsonify(cur.fetchall())

# -------------------- ADMIN --------------------

@app.route('/admin-login')
def admin_login_page():
    return render_template("admin-login.html")



@app.route('/admin-dashboard')
def admin_dashboard_page():
    # You'll need session or a proper login mechanism
    return render_template("admin-dashboard.html", admin={"admin_id": "Admin"})


@app.route('/admin-auth', methods=['POST'])
def admin_auth():
    data = request.form
    admin_id = data['admin_id']
    password = data['password']
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM employee WHERE admin_id = %s AND password = %s", (admin_id, password))
    admin = cur.fetchone()
    cur.close()
    if admin:
        return jsonify({"status": "success", "admin_id": admin_id})
    return jsonify({"status": "fail", "message": "❌ Invalid Admin Credentials"})

@app.route('/admin/accounts')
def admin_all_accounts():
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT name, ac_number, amount FROM register")
    return jsonify(cur.fetchall())

@app.route('/admin/account/<ac_number>')
def admin_view_account(ac_number):
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM register WHERE ac_number = %s", (ac_number,))
    row = cur.fetchone()
    return jsonify(row if row else {"error": "Account not found"})

@app.route('/admin/transactions/<date>')
def admin_txn_date(date):
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM transactions WHERE DATE(timestamp) = %s", (date,))
    return jsonify(cur.fetchall())

# -------------------- MAIN --------------------
if __name__ == '__main__':
    app.run(debug=True)
