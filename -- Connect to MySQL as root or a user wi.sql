-- Connect to MySQL as root or a user with appropriate privileges
CREATE DATABASE school_management;

USE school_management;

CREATE TABLE classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(100),
    num_students INT DEFAULT 0
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    class_id INT,
    scores JSON,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);
