# 🎓 Campus Event Management API

This project is a simple **Campus Event Management System** built with **Flask** and **MySQL**.
It allows colleges to create events, students to register, attendance to be tracked, and reports to be generated.

---

## ⚡ Features

* Create and manage events
* Add students and register them for events
* Mark attendance
* Collect feedback (rating + comments)
* Generate reports:

  * Event popularity (by registrations)
  * Student participation (events attended)

---

## 🛠️ Tech Stack

* **Python 3**
* **Flask** (REST API framework)
* **MySQL (XAMPP)** as database
* **Postman** for testing

---

## 📂 Project Setup

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/campus-event-management.git
cd campus-event-management
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

*(If you don’t have `requirements.txt`, just run)*

```bash
pip install flask mysql-connector-python
```

---

## 🗄️ Database Setup (XAMPP MySQL)

1. Start **Apache** + **MySQL** in XAMPP.
2. Open [http://localhost/phpmyadmin](http://localhost/phpmyadmin).
3. Create database + tables:

   * Go to **SQL tab**.
   * Paste and run the SQL script from `/db_schema.sql` (or the one I shared).
4. By default, MySQL user is `root` with no password.
   If you’ve set a password, update it in `app.py` under `DB_CONFIG`.

---

## 🚀 Run the App

```bash
python app.py
```

App runs at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔗 API Endpoints

### Home (HTML Welcome Page)

`GET /` → Shows links to reports

### Events

* `POST /events` → Create new event

  ```json
  {
    "college_id": 1,
    "title": "Hackathon 2025",
    "event_type": "Hackathon",
    "date": "2025-09-20",
    "description": "48-hour coding marathon"
  }
  ```

### Students

* `POST /students` → Add new student

### Registrations

* `POST /events/<event_id>/register` → Register student for event

### Attendance

* `POST /attendance/mark` → Mark attendance

### Feedback

* `POST /feedback` → Submit feedback

### Reports

* `GET /reports/event-popularity` → Events sorted by registrations
* `GET /reports/student-participation/<student_id>` → How many events a student attended

---

## 🧪 Testing with Postman

A **ready-to-use Postman collection** is included:
`CampusEvents.postman_collection.json`

Steps:

1. Import into Postman.
2. Make sure your server is running (`python app.py`).
3. Run requests in order → Create Event → Add Student → Register → Mark Attendance → Feedback → Reports.

---

## 📌 Notes

* Each student can register for an event only once (duplicate prevention).
* Reports are based on real-time data.
* Database is small-scale (\~50 colleges × 500 students × 20 events).

---

## 👨‍💻 Author

This project was developed as part of **Webknot Technologies Campus Drive Assignment**.
