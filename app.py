from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3

app = Flask(__name__)
DB = "students.db"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Student CRUD App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body{font-family:Arial;background:#f2f5f9;margin:0;color:#222}
        header{background:#243b53;color:white;padding:20px;text-align:center}
        .container{max-width:1000px;margin:25px auto;background:white;padding:20px;border-radius:10px}
        input,button{padding:10px;margin:5px;border-radius:5px;border:1px solid #bbb}
        button,.btn{background:#2563eb;color:white;border:0;text-decoration:none;padding:10px 14px;border-radius:5px}
        .delete{background:#dc2626}.edit{background:#16a34a}
        table{width:100%;border-collapse:collapse;margin-top:20px}
        th,td{border:1px solid #ddd;padding:10px;text-align:center}
        th{background:#e2e8f0}
        .message{background:#d1fae5;padding:10px;border-radius:5px;margin:10px 0}
        @media(max-width:650px){table{font-size:12px}input{width:90%}}
    </style>
</head>
<body>
<header><h1>Student Management System</h1></header>
<div class="container">
    {% for message in get_flashed_messages() %}
        <div class="message">{{ message }}</div>
    {% endfor %}

    <h2>{{ "Edit Student" if student else "Add Student" }}</h2>
    <form method="POST" action="{{ url_for('save_student', student_id=student[0] if student else 0) }}">
        <input name="name" placeholder="Student Name" required value="{{ student[1] if student else '' }}">
        <input name="email" type="email" placeholder="Email" required value="{{ student[2] if student else '' }}">
        <input name="department" placeholder="Department" required value="{{ student[3] if student else '' }}">
        <input name="year" type="number" min="1" max="4" placeholder="Year (1-4)" required value="{{ student[4] if student else '' }}">
        <button type="submit">{{ "Update" if student else "Add Student" }}</button>
        {% if student %}<a class="btn" href="{{ url_for('home') }}">Cancel</a>{% endif %}
    </form>

    <h2>Student Records</h2>
    <form method="GET">
        <input name="search" placeholder="Search students" value="{{ search }}">
        <button type="submit">Search</button>
        <a class="btn" href="{{ url_for('home') }}">Clear</a>
    </form>

    <table>
        <tr><th>ID</th><th>Name</th><th>Email</th><th>Department</th><th>Year</th><th>Actions</th></tr>
        {% for s in students %}
        <tr>
            <td>{{ s[0] }}</td><td>{{ s[1] }}</td><td>{{ s[2] }}</td>
            <td>{{ s[3] }}</td><td>{{ s[4] }}</td>
            <td>
                <a class="btn edit" href="{{ url_for('edit_student', student_id=s[0]) }}">Edit</a>
                <a class="btn delete" href="{{ url_for('delete_student', student_id=s[0]) }}"
                   onclick="return confirm('Delete this student?')">Delete</a>
            </td>
        </tr>
        {% else %}
        <tr><td colspan="6">No records found</td></tr>
        {% endfor %}
    </table>
</div>
</body>
</html>
"""

def connect_db():
    connection = sqlite3.connect(DB)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            year INTEGER NOT NULL CHECK(year BETWEEN 1 AND 4)
        )
    """)
    connection.commit()
    return connection

@app.route("/")
def home():
    search = request.args.get("search", "")
    db = connect_db()
    if search:
        students = db.execute("""
            SELECT * FROM students
            WHERE name LIKE ? OR email LIKE ? OR department LIKE ?
            ORDER BY id DESC
        """, (f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()
    else:
        students = db.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    db.close()
    return render_template_string(HTML, students=students, student=None, search=search)

@app.route("/add", methods=["POST"])
@app.route("/save/<int:student_id>", methods=["POST"])
def save_student(student_id=0):
    name = request.form["name"].strip()
    email = request.form["email"].strip()
    department = request.form["department"].strip()
    year = request.form["year"].strip()

    if not name or not email or not department:
        return "All fields are required"

    try:
        year = int(year)
        if year not in [1, 2, 3, 4]:
            return "Year must be between 1 and 4"

        db = connect_db()
        if student_id == 0:
            db.execute(
                "INSERT INTO students(name,email,department,year) VALUES(?,?,?,?)",
                (name, email, department, year)
            )
        else:
            db.execute("""
                UPDATE students
                SET name=?, email=?, department=?, year=?
                WHERE id=?
            """, (name, email, department, year, student_id))
        db.commit()
        db.close()
        return redirect(url_for("home"))
    except sqlite3.IntegrityError:
        return "Error: Email already exists"
    except ValueError:
        return "Year must be a number from 1 to 4"

@app.route("/edit/<int:student_id>")
def edit_student(student_id):
    db = connect_db()
    student = db.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    students = db.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
    db.close()
    return render_template_string(HTML, students=students, student=student, search="")

@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    db = connect_db()
    db.execute("DELETE FROM students WHERE id=?", (student_id,))
    db.commit()
    db.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    connect_db().close()
    app.run(debug=True)
