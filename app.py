from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="reddy@6319nr",
    database="student_db"
)

cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template("index.html", students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        marks = request.form['marks']

        query = "INSERT INTO students (name, email, course, marks) VALUES (%s, %s, %s, %s)"
        values = (name, email, course, marks)

        cursor.execute(query, values)
        db.commit()

        return redirect('/')

    return render_template("add_student.html")

@app.route('/delete/<int:id>')
def delete_student(id):
    query = "DELETE FROM students WHERE id = %s"
    value = (id,)

    cursor.execute(query, value)
    db.commit()

    return redirect('/')    

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        marks = request.form['marks']

        query = """
        UPDATE students
        SET name=%s, email=%s, course=%s, marks=%s
        WHERE id=%s
        """
        values = (name, email, course, marks, id)

        cursor.execute(query, values)
        db.commit()

        return redirect('/')

    query = "SELECT * FROM students WHERE id = %s"
    value = (id,)
    cursor.execute(query, value)

    student = cursor.fetchone()

    return render_template("update_student.html", student=student)
print("Update route loaded")    

if __name__ == '__main__':
    app.run(debug=True)
