from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(host="localhost", user="root", password="", database="attendance_db")

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Attendance ORDER BY Timestamp DESC")
    data = cursor.fetchall()
    conn.close()
    return render_template("index.html", records=data)

if __name__ == "__main__":
    app.run(debug=True)
