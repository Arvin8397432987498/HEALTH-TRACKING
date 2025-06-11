    from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

# Create the database table if it doesn't exist
def init_db():
    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS health
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 entry_date TEXT,
                 weight REAL,
                 sleep_hours REAL,
                 water_intake REAL,
                 notes TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    c.execute("SELECT * FROM health ORDER BY entry_date DESC")
    entries = c.fetchall()
    conn.close()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    entry_date = request.form['entry_date']
    weight = request.form['weight']
    sleep_hours = request.form['sleep_hours']
    water_intake = request.form['water_intake']
    notes = request.form['notes']

    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    c.execute("INSERT INTO health (entry_date, weight, sleep_hours, water_intake, notes) VALUES (?, ?, ?, ?, ?)",
              (entry_date, weight, sleep_hours, water_intake, notes))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit(entry_id):
    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    if request.method == 'POST':
        c.execute("""UPDATE health SET entry_date=?, weight=?, sleep_hours=?, water_intake=?, notes=? WHERE id=?""",
                  (request.form['entry_date'], request.form['weight'], request.form['sleep_hours'],
                   request.form['water_intake'], request.form['notes'], entry_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM health WHERE id=?", (entry_id,))
        entry = c.fetchone()
        conn.close()
        return render_template('edit.html', entry=entry)

@app.route('/delete/<int:entry_id>')
def delete(entry_id):
    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    c.execute("DELETE FROM health WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
