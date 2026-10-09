<div align="center">

# 🚀 Face Recognition Attendance System

### Smart • Automated • Efficient

A Python-based web application for student attendance management using face recognition.

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
</p>

<br>

<a href="https://face-recognition-attendance-system-vnsj.onrender.com/">
  <img src="https://img.shields.io/badge/🚀_OPEN-LIVE_DEMO-2EA44F?style=for-the-badge" alt="Live Demo">
</a>

<a href="https://github.com/lalitjagid/Face-Recognition-Attendance-System">
  <img src="https://img.shields.io/badge/VIEW-SOURCE_CODE-181717?style=for-the-badge&logo=github" alt="Source Code">
</a>

</div>

---

## 📌 About the Project

The **Face Recognition Attendance System** is a Python-based web application designed to simplify student attendance management.

The system combines Flask, OpenCV, and SQLite to provide student registration, facial recognition, and attendance management functionality.

It aims to reduce manual attendance-taking effort and maintain organized student attendance records.

## ✨ Features

### 👨‍🎓 Student Management
- Register new students.
- Store student ID, name, roll number, and course.
- View registered students.
- Edit student information.
- Delete student records.
- View individual student profiles.

### 📸 Face Registration
- Capture student face images using a camera.
- Detect faces using OpenCV Haar Cascade.
- Process and save facial images.
- Associate face images with registered students.

### 🤖 Face Recognition
- Detect faces using OpenCV.
- Recognize faces using the LBPH Face Recognizer.
- Match detected faces against the trained model.
- Identify registered students for attendance marking.

### 📅 Attendance Management
- Mark attendance after successful face recognition.
- Prevent duplicate attendance entries for the same student on the same day.
- Store attendance dates and times.
- View attendance records.
- Calculate attendance percentages.

### 🔐 Admin Dashboard
- Admin login.
- Student record management.
- Attendance management.
- Dashboard for accessing application features.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| OpenCV | Face detection and recognition |
| LBPH | Face recognition algorithm |
| SQLite | Database management |
| HTML5 | Web page structure |
| CSS3 | User interface design |
| Jinja2 | Dynamic HTML templates |

## 🖥️ Application Workflow

```text
Student Registration
        |
        v
Capture Face Image
        |
        v
Train Recognition Model
        |
        v
Recognize Student
        |
        v
Verify Recognition
        |
        v
Mark Attendance
        |
        v
Store Attendance in Database
        |
        v
View Attendance Records
```

## ⚙️ Installation

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/lalitjagid/Face-Recognition-Attendance-System.git
```

### 2. Open the Project Directory

```bash
cd Face-Recognition-Attendance-System
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

Open the local address displayed in your terminal.

> Note: The application requires the appropriate Python dependencies, database initialization, and face recognition model configuration.

## 🌐 Live Demo

Try the deployed application:

### 👉 [Open Face Recognition Attendance System](https://face-recognition-attendance-system-vnsj.onrender.com/)

The application is hosted on Render. Camera functionality and database persistence depend on the deployment configuration.

## 🎯 Project Objectives

- Automate student attendance management.
- Reduce manual attendance-taking effort.
- Maintain organized student records.
- Apply computer vision to a practical problem.
- Gain hands-on experience with Python web development.

## 🔮 Future Improvements

- Export attendance records to CSV or Excel.
- Add date-wise attendance reports.
- Improve face recognition accuracy.
- Add attendance analytics.
- Improve application security.
- Enhance responsive user interface design.

## 👨‍💻 Developer

<div align="center">

### Lalit Jangid

**BCA Student | Aspiring Software Developer**

Interested in Python, Java, and Web Development.

<a href="https://github.com/lalitjagid">
  <img src="https://img.shields.io/badge/GitHub-Visit_My_Profile-181717?style=for-the-badge&logo=github" alt="GitHub Profile">
</a>

</div>

---

<div align="center">

### 💙 Built with Python and OpenCV

⭐ If you find this project interesting, consider starring the repository!

</div>
