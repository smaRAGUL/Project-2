from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('teachers.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS teachers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    email TEXT,
                    phone TEXT,
                    department TEXT);''')
    conn.commit()
    # Sample data insertion
    conn.execute("INSERT INTO teachers (name, subject, email, phone, department) VALUES ('John Doe', 'Mathematics', 'john@example.com', '9876543210', 'Science')")
    conn.execute("INSERT INTO teachers (name, subject, email, phone, department) VALUES ('Jane Smith', 'English', 'jane@example.com', '8765432109', 'Arts')")
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('teachers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers")
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', teachers=data)

@app.route('/add', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        conn = sqlite3.connect('teachers.db')
        conn.execute("INSERT INTO teachers (name, subject, email, phone, department) VALUES (?, ?, ?, ?, ?)",
                     (name, subject, email, phone, department))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_teacher(id):
    conn = sqlite3.connect('teachers.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        cursor.execute("UPDATE teachers SET name=?, subject=?, email=?, phone=?, department=? WHERE id=?",
                       (name, subject, email, phone, department, id))
        conn.commit()
        conn.close()
        return redirect('/')
    cursor.execute("SELECT * FROM teachers WHERE id=?", (id,))
    data = cursor.fetchone()
    conn.close()
    return render_template('edit.html', teacher=data)

@app.route('/delete/<int:id>')
def delete_teacher(id):
    conn = sqlite3.connect('teachers.db')
    conn.execute("DELETE FROM teachers WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
