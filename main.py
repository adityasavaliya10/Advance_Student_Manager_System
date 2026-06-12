
"""
ADVANCED STUDENT TRACKER (Single File)
Features:
- SQLite database
- Admin login
- Add / Update / Delete students
- Search students
- Ranking system
- GPA calculation
- Attendance tracking
- Dashboard analytics
- CSV export
- JSON backup
- Scholarship eligibility
"""

import sqlite3
import csv
import json
from datetime import datetime

DB = "students.db"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"


class StudentTracker:
    def __init__(self):
        self.conn = sqlite3.connect(DB)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS students(
            student_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            grade TEXT,
            math REAL,
            science REAL,
            english REAL,
            attendance REAL,
            created_at TEXT
        )
        """)
        self.conn.commit()

    def percentage(self, m, s, e):
        return round((m + s + e) / 300 * 100, 2)

    def gpa(self, pct):
        if pct >= 90: return 4.0
        if pct >= 80: return 3.7
        if pct >= 70: return 3.0
        if pct >= 60: return 2.5
        if pct >= 50: return 2.0
        return 0.0

    def performance(self, pct):
        if pct >= 90: return "Excellent"
        if pct >= 75: return "Very Good"
        if pct >= 60: return "Good"
        if pct >= 40: return "Average"
        return "Needs Improvement"

    def scholarship(self, pct, attendance):
        return "Eligible" if pct >= 85 and attendance >= 90 else "Not Eligible"

    def add_student(self):
        sid = input("Student ID: ")
        name = input("Name: ")
        age = int(input("Age: "))
        grade = input("Grade: ")
        math = float(input("Math: "))
        science = float(input("Science: "))
        english = float(input("English: "))
        attendance = float(input("Attendance %: "))

        try:
            self.cur.execute("""
            INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?)
            """, (
                sid, name, age, grade,
                math, science, english,
                attendance,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            self.conn.commit()
            print("Student added successfully.")
        except sqlite3.IntegrityError:
            print("Student ID already exists.")

    def view_students(self):
        rows = self.cur.execute("SELECT * FROM students").fetchall()

        if not rows:
            print("No students found.")
            return

        ranked = []

        for r in rows:
            pct = self.percentage(r[4], r[5], r[6])
            ranked.append((pct, r))

        ranked.sort(reverse=True)

        print("\nRANK LIST")
        print("-" * 120)

        for rank, (_, r) in enumerate(ranked, start=1):
            pct = self.percentage(r[4], r[5], r[6])
            gpa = self.gpa(pct)

            print(
                f"#{rank} | {r[0]} | {r[1]} | "
                f"{pct}% | GPA:{gpa} | Attendance:{r[7]}%"
            )

    def search_student(self):
        keyword = input("Name or ID: ")

        rows = self.cur.execute("""
        SELECT * FROM students
        WHERE student_id LIKE ? OR name LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%")).fetchall()

        for r in rows:
            pct = self.percentage(r[4], r[5], r[6])

            print("\n--------------------")
            print("ID:", r[0])
            print("Name:", r[1])
            print("Percentage:", pct)
            print("Performance:", self.performance(pct))
            print("--------------------")

    def update_student(self):
        sid = input("Student ID: ")

        row = self.cur.execute(
            "SELECT * FROM students WHERE student_id=?",
            (sid,)
        ).fetchone()

        if not row:
            print("Student not found.")
            return

        name = input(f"Name ({row[1]}): ") or row[1]
        age = input(f"Age ({row[2]}): ") or row[2]
        grade = input(f"Grade ({row[3]}): ") or row[3]

        math = input(f"Math ({row[4]}): ") or row[4]
        science = input(f"Science ({row[5]}): ") or row[5]
        english = input(f"English ({row[6]}): ") or row[6]
        attendance = input(f"Attendance ({row[7]}): ") or row[7]

        self.cur.execute("""
        UPDATE students
        SET name=?,age=?,grade=?,
            math=?,science=?,english=?,
            attendance=?
        WHERE student_id=?
        """, (
            name, age, grade,
            math, science, english,
            attendance, sid
        ))
        self.conn.commit()

        print("Updated successfully.")

    def delete_student(self):
        sid = input("Student ID: ")

        self.cur.execute(
            "DELETE FROM students WHERE student_id=?",
            (sid,)
        )

        self.conn.commit()
        print("Deleted successfully.")

    def dashboard(self):
        rows = self.cur.execute(
            "SELECT * FROM students"
        ).fetchall()

        if not rows:
            print("No data.")
            return

        percentages = [
            self.percentage(r[4], r[5], r[6])
            for r in rows
        ]

        avg = round(sum(percentages) / len(percentages), 2)
        top = max(percentages)
        low = min(percentages)

        print("\n===== DASHBOARD =====")
        print("Total Students :", len(rows))
        print("Average %      :", avg)
        print("Highest %      :", top)
        print("Lowest %       :", low)

        failed = sum(1 for p in percentages if p < 40)
        print("Failed Students:", failed)

    def topper(self):
        rows = self.cur.execute(
            "SELECT * FROM students"
        ).fetchall()

        if not rows:
            return

        best = None
        best_pct = -1

        for r in rows:
            pct = self.percentage(r[4], r[5], r[6])

            if pct > best_pct:
                best_pct = pct
                best = r

        print("\nTOPPER")
        print(best[1], "-", best_pct, "%")

    def scholarship_report(self):
        rows = self.cur.execute(
            "SELECT * FROM students"
        ).fetchall()

        print("\nSCHOLARSHIP REPORT")

        for r in rows:
            pct = self.percentage(r[4], r[5], r[6])

            print(
                r[1],
                "->",
                self.scholarship(pct, r[7])
            )

    def export_csv(self):
        rows = self.cur.execute(
            "SELECT * FROM students"
        ).fetchall()

        with open("students_export.csv", "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow([
                "ID","Name","Age","Grade",
                "Math","Science","English",
                "Attendance","Percentage"
            ])

            for r in rows:
                writer.writerow([
                    r[0], r[1], r[2], r[3],
                    r[4], r[5], r[6], r[7],
                    self.percentage(r[4], r[5], r[6])
                ])

        print("CSV exported.")

    def backup_json(self):
        rows = self.cur.execute(
            "SELECT * FROM students"
        ).fetchall()

        data = []

        for r in rows:
            data.append({
                "student_id": r[0],
                "name": r[1],
                "age": r[2],
                "grade": r[3],
                "math": r[4],
                "science": r[5],
                "english": r[6],
                "attendance": r[7],
                "created_at": r[8]
            })

        with open("backup.json", "w") as f:
            json.dump(data, f, indent=4)

        print("Backup created.")

    def menu(self):
        while True:
            print("\n" + "=" * 40)
            print("ADVANCED STUDENT TRACKER")
            print("=" * 40)
            print("1. Add Student")
            print("2. View Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Dashboard")
            print("7. Topper")
            print("8. Scholarship Report")
            print("9. Export CSV")
            print("10. Backup JSON")
            print("11. Exit")

            choice = input("Choose: ")

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.update_student()
            elif choice == "5":
                self.delete_student()
            elif choice == "6":
                self.dashboard()
            elif choice == "7":
                self.topper()
            elif choice == "8":
                self.scholarship_report()
            elif choice == "9":
                self.export_csv()
            elif choice == "10":
                self.backup_json()
            elif choice == "11":
                break
            else:
                print("Invalid choice.")


def login():
    print("=" * 40)
    print("ADMIN LOGIN")
    print("=" * 40)

    user = input("Username: ")
    password = input("Password: ")

    return user == ADMIN_USER and password == ADMIN_PASS


if __name__ == "__main__":
    if login():
        app = StudentTracker()
        app.menu()
    else:
        print("Access denied.")
