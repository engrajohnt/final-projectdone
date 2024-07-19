import pygame
import mysql.connector
import json

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT = pygame.font.Font(None, 32)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("School Data Management System")

# Database setup
DATABASE_CONFIG = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'school_management'
}

def connect_db():
    return mysql.connector.connect(**DATABASE_CONFIG)

def add_student(name, class_id, scores):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, class_id, scores) VALUES (%s, %s, %s)",
                   (name, class_id, json.dumps(scores)))
    cursor.execute("UPDATE classes SET num_students = num_students + 1 WHERE class_id = %s", (class_id,))
    conn.commit()
    conn.close()

def get_students():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return students

def update_student(student_id, scores):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET scores = %s WHERE student_id = %s",
                   (json.dumps(scores), student_id))
    conn.commit()
    conn.close()

def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT class_id FROM students WHERE student_id = %s", (student_id,))
    class_id = cursor.fetchone()[0]
    cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
    cursor.execute("UPDATE classes SET num_students = num_students - 1 WHERE class_id = %s", (class_id,))
    conn.commit()
    conn.close()

def reallocate_student(student_id, new_class_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT class_id FROM students WHERE student_id = %s", (student_id,))
    old_class_id = cursor.fetchone()[0]
    cursor.execute("UPDATE students SET class_id = %s WHERE student_id = %s", (new_class_id, student_id))
    cursor.execute("UPDATE classes SET num_students = num_students - 1 WHERE class_id = %s", (old_class_id,))
    cursor.execute("UPDATE classes SET num_students = num_students + 1 WHERE class_id = %s", (new_class_id,))
    conn.commit()
    conn.close()

def calculate_grade(score):
    if score < 60:
        return 'F'
    elif score < 70:
        return 'C'
    elif score < 80:
        return 'B'
    else:
        return 'A'

def get_class_average(class_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT scores FROM students WHERE class_id = %s", (class_id,))
    scores = cursor.fetchall()
   
    subject_totals = {}
    subject_counts = {}
   
    for score in scores:
        student_scores = json.loads(score[0])
        for subject, mark in student_scores.items():
            if subject not in subject_totals:
                subject_totals[subject] = 0
                subject_counts[subject] = 0
            subject_totals[subject] += mark
            subject_counts[subject] += 1
   
    averages = {subject: total / count for subject, total, count in zip(subject_totals.keys(), subject_totals.values(), subject_counts.values())}
   
    conn.close()
    return averages

# Initialize the database (dummy function for MySQL as tables are already created)
def initialize_db():
    pass

# Pygame UI elements (simplified for demonstration purposes)
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill screen with white color
        screen.fill(WHITE)

        # UI Elements
        draw_text('School Data Management System', FONT, BLACK, screen, 20, 20)

        # Display students (for demonstration)
        students = get_students()
        y_offset = 60
        for student in students:
            draw_text(f'ID: {student[0]}, Name: {student[1]}, Class ID: {student[2]}, Scores: {student[3]}', FONT, BLACK, screen, 20, y_offset)
            y_offset += 30

        pygame.display.flip()

    pygame.quit()

if _name_ == '_main_':
    main()





