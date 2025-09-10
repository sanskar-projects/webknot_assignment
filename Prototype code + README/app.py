from flask import Flask, request, jsonify
import mysql.connector

# -------------------------
# DATABASE CONFIG
# -------------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # change if you set a password in XAMPP
    'password': '',          # default empty for XAMPP
    'database': 'campus_events'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# -------------------------
# FLASK APP INIT
# -------------------------
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return """
    <html>
        <head>
            <title>Campus Event Management API</title>
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1>🎓 Welcome to Campus Event Management API 🚀</h1>
            <p>Use the available endpoints to manage events, students, attendance, and reports.</p>
            <hr/>
            <p><b>Example Endpoints:</b></p>
            <ul style="list-style:none;">
                <li>POST /events</li>
                <li>POST /students</li>
                <li>POST /events/&lt;event_id&gt;/register</li>
                <li>POST /attendance/mark</li>
                <li>POST /feedback</li>
                <li>GET /reports/event-popularity</li>
                <li>GET /reports/student-participation/&lt;student_id&gt;</li>
            </ul>
        </body>
    </html>
    """

# -------------------------
# 1. EVENT CREATION
# -------------------------
@app.route('/events', methods=['POST'])
def create_event():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """INSERT INTO events (college_id, title, event_type, date, description) 
               VALUES (%s, %s, %s, %s, %s)"""
    cursor.execute(query, (data['college_id'], data['title'], data['event_type'],
                           data['date'], data.get('description', '')))
    conn.commit()
    event_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Event created", "event_id": event_id}), 201

# -------------------------
# 2. STUDENT REGISTRATION
# -------------------------
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO students (college_id, name, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (data['college_id'], data['name'], data['email']))
    conn.commit()
    student_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({"message": "Student added", "student_id": student_id}), 201

@app.route('/events/<int:event_id>/register', methods=['POST'])
def register_student(event_id):
    data = request.json
    student_id = data['student_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """INSERT INTO registrations (student_id, event_id) VALUES (%s, %s)"""
    try:
        cursor.execute(query, (student_id, event_id))
        conn.commit()
        reg_id = cursor.lastrowid
        msg = {"message": "Registration successful", "registration_id": reg_id}
        status = 201
    except mysql.connector.Error as e:
        msg = {"error": str(e)}
        status = 400
    cursor.close()
    conn.close()
    return jsonify(msg), status

# -------------------------
# 3. ATTENDANCE
# -------------------------
@app.route('/attendance/mark', methods=['POST'])
def mark_attendance():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """INSERT INTO attendance (registration_id, status, checkin_time) 
               VALUES (%s, %s, NOW())"""
    cursor.execute(query, (data['registration_id'], data.get('status', 'Present')))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Attendance marked"}), 201

# -------------------------
# 4. FEEDBACK
# -------------------------
@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """INSERT INTO feedback (registration_id, rating, comments) 
               VALUES (%s, %s, %s)"""
    cursor.execute(query, (data['registration_id'], data['rating'], data.get('comments', '')))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Feedback submitted"}), 201

# -------------------------
# 5. REPORTS
# -------------------------
@app.route('/reports/event-popularity', methods=['GET'])
def event_popularity():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """SELECT e.event_id, e.title, COUNT(r.registration_id) as total_registrations
               FROM events e
               LEFT JOIN registrations r ON e.event_id = r.event_id
               GROUP BY e.event_id
               ORDER BY total_registrations DESC"""
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)

@app.route('/reports/student-participation/<int:student_id>', methods=['GET'])
def student_participation(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """SELECT COUNT(a.attendance_id) as events_attended
               FROM registrations r
               JOIN attendance a ON r.registration_id = a.registration_id
               WHERE r.student_id = %s AND a.status='Present'"""
    cursor.execute(query, (student_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(result)

# -------------------------
# MAIN
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
