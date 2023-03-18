import mysql.connector


MYSQL_DATABASE="UMS"
MYSQL_USER="root"
MYSQL_ROOT_PASSWORD=""
MYSQL_PASSWORD=""
MYSQL_HOST="localhost"

connection = mysql.connector.connect(
  host=MYSQL_HOST,
  user=MYSQL_USER,
  password=MYSQL_PASSWORD,
  database=MYSQL_DATABASE,
  auth_plugin='mysql_native_password'
)

cursor= connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
  student_id INT PRIMARY KEY AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(100) UNIQUE,
  password VARCHAR(255),
  phone_number VARCHAR(20),
  department_id INT,
  FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Departments (
  department_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,
  location VARCHAR(100),
  budget DECIMAL(10,2)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Teachers (
  teacher_id INT PRIMARY KEY AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(100) UNIQUE,
  password VARCHAR(255),
  phone_number VARCHAR(20),
  department_id INT,
  hire_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Admin (
  admin_id INT PRIMARY KEY AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(100) UNIQUE,
  password VARCHAR(255),
  phone_number VARCHAR(20),
  hire_date DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS course (
  course_id INT PRIMARY KEY AUTO_INCREMENT,
  course_name VARCHAR(255),
  department_id INT,
  teacher_id INT,
  CONSTRAINT fk_course_department
    FOREIGN KEY (department_id)
    REFERENCES Departments(department_id),
  CONSTRAINT fk_course_teacher
    FOREIGN KEY (teacher_id)
    REFERENCES Teachers(teacher_id)
);
""")
