# import mysql.connector

# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Sankalp@2024"
# )
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM student_dashboard.Student;")
# data=cursor.fetchall();
# for row in data:
#     print(row)

# schema_sql = """
# CREATE DATABASE IF NOT EXISTS student_dashboard;
# USE student_dashboard;

# CREATE TABLE IF NOT EXISTS Student (
#     student_id INT AUTO_INCREMENT PRIMARY KEY,
#     first_name VARCHAR(50),
#     last_name VARCHAR(50),
#     email VARCHAR(100) UNIQUE,
#     department VARCHAR(50),
#     enrollment_year INT
# );

# # CREATE TABLE IF NOT EXISTS Course (
# #     course_id INT AUTO_INCREMENT PRIMARY KEY,
# #     course_name VARCHAR(100),
# #     course_code VARCHAR(20) UNIQUE,
# #     credits INT
# # );

# # CREATE TABLE IF NOT EXISTS StudentCourse (
# #     id INT AUTO_INCREMENT PRIMARY KEY,
# #     student_id INT,
# #     course_id INT,
# #     grade VARCHAR(2),
# #     FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE,
# #     FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE
# # );

# # CREATE TABLE IF NOT EXISTS Project (
# #     project_id INT AUTO_INCREMENT PRIMARY KEY,
# #     student_id INT,
# #     project_title VARCHAR(100),
# #     description TEXT,
# #     grade VARCHAR(2),
# #     FOREIGN KEY (student_id) REFERENCES Student(student_id) ON DELETE CASCADE
# # );

# # CREATE TABLE IF NOT EXISTS Admin (
# #     admin_id INT AUTO_INCREMENT PRIMARY KEY,
# #     username VARCHAR(50) UNIQUE,
# #     password_hash VARCHAR(255),
# #     role VARCHAR(20) DEFAULT 'admin'
# # );

# # INSERT INTO Student (first_name, last_name, email, department, enrollment_year)
# # VALUES
# # ('Aarav', 'Sharma', 'aarav.sharma@example.com', 'Computer Science', 2022),
# # ('Riya', 'Patel', 'riya.patel@example.com', 'Information Technology', 2023),
# # ('Karan', 'Verma', 'karan.verma@example.com', 'Electronics', 2022),
# # ('Sneha', 'Singh', 'sneha.singh@example.com', 'Mechanical', 2021),
# # ('Ananya', 'Mehta', 'ananya.mehta@example.com', 'Computer Science', 2023),
# # ('Ishan', 'Gupta', 'ishan.gupta@example.com', 'Civil', 2022),
# # ('Tanya', 'Rao', 'tanya.rao@example.com', 'Information Technology', 2021);

# # INSERT INTO Course (course_name, course_code, credits)
# # VALUES
# # ('Database Management Systems', 'CS301', 4),
# # ('Data Structures', 'CS201', 3),
# # ('Operating Systems', 'CS303', 4),
# # ('Machine Learning', 'CS401', 4),
# # ('Computer Networks', 'CS305', 3),
# # ('Software Engineering', 'CS306', 3);

# # INSERT INTO StudentCourse (student_id, course_id, grade)
# # VALUES
# # (1, 1, 'A'), (1, 2, 'B'),
# # (2, 1, 'A'), (2, 4, 'A'),
# # (3, 3, 'B'), (3, 5, 'A'),
# # (4, 6, 'C'), (4, 3, 'B'),
# # (5, 1, 'A'), (5, 2, 'A'),
# # (6, 5, 'B'),
# # (7, 4, 'A');

# # INSERT INTO Project (student_id, project_title, description, grade)
# # VALUES
# # (1, 'Library Management System', 'A web app to manage library books and students.', 'A'),
# # (2, 'AI Chatbot', 'Conversational chatbot using NLP.', 'A'),
# # (3, 'IoT Smart Home', 'Controlling home appliances using Arduino.', 'B'),
# # (4, 'Mechanical Arm', 'Automated robotic arm using sensors.', 'B'),
# # (5, 'E-commerce Website', 'Full-stack online store platform.', 'A'),
# # (7, 'Traffic Management AI', 'AI-based model for optimizing traffic lights.', 'A');

# # INSERT INTO Admin (username, password_hash, role)
# # VALUES
# # ('admin', SHA2('admin123', 256), 'superadmin'),
# # ('faculty1', SHA2('password1', 256), 'faculty');
# # """

# for statement in schema_sql.split(';'):
#     if statement.strip():
#         cursor.execute(statement)

# conn.commit()
# cursor.close()
# conn.close()

# print("Database 'student_dashboard' created and sample data inserted successfully.")
