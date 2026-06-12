# =========================================================
# ADVANCED STUDENT TRACKER WEB APPLICATION
# Full Flask + Python + HTML + CSS Project
# Single File Project
# =========================================================

from flask import Flask, render_template_string, request, redirect, url_for
import json
import os
import csv

app = Flask(__name__)

DATA_FILE = "students.json"

# =========================================================
# STUDENT CLASS
# =========================================================

class Student:

    def __init__(
        self,
        student_id,
        name,
        age,
        grade,
        marks,
        attendance
    ):

        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.marks = marks
        self.attendance = attendance

    # -----------------------------------------------------

    def total_marks(self):
        return sum(self.marks.values())

    # -----------------------------------------------------

    def percentage(self):

        if len(self.marks) == 0:
            return 0

        total = len(self.marks) * 100

        return round(
            (self.total_marks() / total) * 100,
            2
        )

    # -----------------------------------------------------

    def gpa(self):

        p = self.percentage()

        if p >= 90:
            return 4.0

        elif p >= 80:
            return 3.7

        elif p >= 70:
            return 3.0

        elif p >= 60:
            return 2.5

        elif p >= 50:
            return 2.0

        return 0.0

    # -----------------------------------------------------

    def performance(self):

        p = self.percentage()

        if p >= 90:
            return "Excellent"

        elif p >= 75:
            return "Very Good"

        elif p >= 60:
            return "Good"

        elif p >= 40:
            return "Average"

        return "Needs Improvement"

    # -----------------------------------------------------

    def to_dict(self):

        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "marks": self.marks,
            "attendance": self.attendance
        }


# =========================================================
# DATA FUNCTIONS
# =========================================================

def load_students():

    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:

        data = json.load(file)

    students = []

    for s in data:

        student = Student(
            s["student_id"],
            s["name"],
            s["age"],
            s["grade"],
            s["marks"],
            s["attendance"]
        )

        students.append(student)

    return students


# =========================================================

def save_students(students):

    data = []

    for student in students:
        data.append(student.to_dict())

    with open(DATA_FILE, "w") as file:

        json.dump(data, file, indent=4)


# =========================================================
# HTML TEMPLATE
# =========================================================

HTML = """

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Advanced Student Tracker</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:'Poppins',sans-serif;
}

body{
    background:linear-gradient(135deg,#0f172a,#1e293b,#111827);
    color:white;
    min-height:100vh;
}

/* NAVBAR */

.navbar{
    width:100%;
    padding:20px 40px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(12px);
    border-bottom:1px solid rgba(255,255,255,0.1);
}

.logo{
    font-size:30px;
    font-weight:700;
    color:#38bdf8;
}

.nav-links{
    display:flex;
    gap:25px;
}

.nav-links a{
    text-decoration:none;
    color:white;
    transition:0.3s;
}

.nav-links a:hover{
    color:#38bdf8;
}

/* HERO */

.hero{
    text-align:center;
    padding:60px 20px;
}

.hero h1{
    font-size:55px;
    background:linear-gradient(to right,#38bdf8,#818cf8);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero p{
    color:#cbd5e1;
    margin-top:15px;
}

/* CONTAINER */

.container{
    width:95%;
    max-width:1400px;
    margin:auto;
}

/* DASHBOARD */

.dashboard{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
    gap:25px;
    margin-bottom:40px;
}

.card{
    background:rgba(255,255,255,0.06);
    border-radius:20px;
    padding:30px;
    border:1px solid rgba(255,255,255,0.1);
    backdrop-filter:blur(10px);
    transition:0.3s;
}

.card:hover{
    transform:translateY(-5px);
}

.card h2{
    color:#38bdf8;
    font-size:42px;
}

.card p{
    margin-top:10px;
    color:#cbd5e1;
}

/* FORMS */

.form-section{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:30px;
    margin-bottom:40px;
}

.form-box{
    background:rgba(255,255,255,0.06);
    border-radius:20px;
    padding:30px;
}

.form-box h2{
    margin-bottom:20px;
    color:#38bdf8;
}

.input-group{
    margin-bottom:20px;
}

.input-group input{
    width:100%;
    padding:15px;
    border:none;
    border-radius:12px;
    background:rgba(255,255,255,0.08);
    color:white;
    outline:none;
}

.input-group input::placeholder{
    color:#94a3b8;
}

.btn{
    width:100%;
    padding:15px;
    border:none;
    border-radius:12px;
    background:linear-gradient(45deg,#38bdf8,#6366f1);
    color:white;
    font-size:16px;
    cursor:pointer;
    transition:0.3s;
    font-weight:600;
}

.btn:hover{
    transform:scale(1.02);
}

/* TABLE */

.table-box{
    background:rgba(255,255,255,0.06);
    padding:30px;
    border-radius:20px;
    overflow-x:auto;
}

.table-box h2{
    margin-bottom:20px;
    color:#38bdf8;
}

table{
    width:100%;
    border-collapse:collapse;
}

th{
    padding:16px;
    text-align:left;
    color:#38bdf8;
    background:rgba(255,255,255,0.06);
}

td{
    padding:16px;
    border-bottom:1px solid rgba(255,255,255,0.08);
}

tr:hover{
    background:rgba(255,255,255,0.05);
}

/* BADGES */

.rank{
    background:#22c55e;
    padding:7px 12px;
    border-radius:10px;
    font-weight:bold;
}

.performance{
    color:#38bdf8;
    font-weight:600;
}

/* FOOTER */

.footer{
    text-align:center;
    padding:40px;
    color:#94a3b8;
}

/* RESPONSIVE */

@media(max-width:900px){

    .form-section{
        grid-template-columns:1fr;
    }

    .hero h1{
        font-size:38px;
    }

}

</style>

</head>

<body>

<div class="navbar">

    <div class="logo">
        🎓 Student Tracker
    </div>

    <div class="nav-links">
        <a href="/">Dashboard</a>
        <a href="/">Students</a>
        <a href="/export">Export CSV</a>
    </div>

</div>

<div class="hero">

    <h1>Advanced Student Tracker</h1>

    <p>
        Modern Flask Web Application for Student Management
    </p>

</div>

<div class="container">

    <!-- DASHBOARD -->

    <div class="dashboard">

        <div class="card">
            <h2>{{ total_students }}</h2>
            <p>Total Students</p>
        </div>

        <div class="card">
            <h2>{{ average_percentage }}%</h2>
            <p>Average Percentage</p>
        </div>

        <div class="card">
            <h2>{{ top_score }}%</h2>
            <p>Highest Score</p>
        </div>

    </div>

    <!-- FORMS -->

    <div class="form-section">

        <!-- ADD FORM -->

        <div class="form-box">

            <h2>Add Student</h2>

            <form method="POST" action="/add">

                <div class="input-group">
                    <input type="text" name="student_id" placeholder="Student ID" required>
                </div>

                <div class="input-group">
                    <input type="text" name="name" placeholder="Student Name" required>
                </div>

                <div class="input-group">
                    <input type="number" name="age" placeholder="Age" required>
                </div>

                <div class="input-group">
                    <input type="text" name="grade" placeholder="Grade/Class" required>
                </div>

                <div class="input-group">
                    <input type="number" name="math" placeholder="Math Marks" required>
                </div>

                <div class="input-group">
                    <input type="number" name="science" placeholder="Science Marks" required>
                </div>

                <div class="input-group">
                    <input type="number" name="english" placeholder="English Marks" required>
                </div>

                <div class="input-group">
                    <input type="number" name="attendance" placeholder="Attendance %" required>
                </div>

                <button class="btn">
                    ➕ Add Student
                </button>

            </form>

        </div>

        <!-- SEARCH -->

        <div class="form-box">

            <h2>Search Student</h2>

            <form method="GET" action="/">

                <div class="input-group">
                    <input type="text" name="search" placeholder="Search by Name">
                </div>

                <button class="btn">
                    🔍 Search Student
                </button>

            </form>

        </div>

    </div>

    <!-- TABLE -->

    <div class="table-box">

        <h2>🏆 Student Rank List</h2>

        <table>

            <thead>

                <tr>

                    <th>Rank</th>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Grade</th>
                    <th>Percentage</th>
                    <th>GPA</th>
                    <th>Performance</th>
                    <th>Attendance</th>

                </tr>

            </thead>

            <tbody>

                {% for student in students %}

                <tr>

                    <td>
                        <span class="rank">
                            #{{ loop.index }}
                        </span>
                    </td>

                    <td>{{ student.student_id }}</td>

                    <td>{{ student.name }}</td>

                    <td>{{ student.grade }}</td>

                    <td>{{ student.percentage() }}%</td>

                    <td>{{ student.gpa() }}</td>

                    <td class="performance">
                        {{ student.performance() }}
                    </td>

                    <td>{{ student.attendance }}%</td>

                </tr>

                {% endfor %}

            </tbody>

        </table>

    </div>

    <div class="footer">
        Built with Flask • Python • HTML • CSS
    </div>

</div>

</body>
</html>

"""

# =========================================================
# HOME ROUTE
# =========================================================

@app.route("/")
def home():

    students = load_students()

    search = request.args.get("search")

    if search:

        students = [
            s for s in students
            if search.lower() in s.name.lower()
        ]

    students = sorted(
        students,
        key=lambda s: s.percentage(),
        reverse=True
    )

    total_students = len(students)

    average_percentage = 0

    if total_students > 0:

        average_percentage = round(
            sum(s.percentage() for s in students)
            / total_students,
            2
        )

    top_score = 0

    if students:
        top_score = students[0].percentage()

    return render_template_string(

        HTML,

        students=students,

        total_students=total_students,

        average_percentage=average_percentage,

        top_score=top_score
    )


# =========================================================
# ADD STUDENT
# =========================================================

@app.route("/add", methods=["POST"])
def add_student():

    students = load_students()

    student_id = request.form["student_id"]
    name = request.form["name"]
    age = int(request.form["age"])
    grade = request.form["grade"]

    math = float(request.form["math"])
    science = float(request.form["science"])
    english = float(request.form["english"])

    attendance = float(request.form["attendance"])

    marks = {

        "Math": math,
        "Science": science,
        "English": english
    }

    student = Student(

        student_id,
        name,
        age,
        grade,
        marks,
        attendance
    )

    students.append(student)

    save_students(students)

    return redirect(url_for("home"))


# =========================================================
# EXPORT CSV
# =========================================================

@app.route("/export")
def export_csv():

    students = load_students()

    with open(
        "students.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            "Student ID",
            "Name",
            "Age",
            "Grade",
            "Percentage",
            "GPA",
            "Attendance"

        ])

        for s in students:

            writer.writerow([

                s.student_id,
                s.name,
                s.age,
                s.grade,
                s.percentage(),
                s.gpa(),
                s.attendance

            ])

    return redirect(url_for("home"))


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)