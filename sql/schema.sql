
-- =========================================
-- FULL RESET (SAFE TO RERUN)
-- =========================================
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

GRANT ALL ON SCHEMA public TO user_college;
GRANT ALL ON SCHEMA public TO public;


-- PROGRAMS
-- =========================
CREATE TABLE programs (
    program_id SERIAL PRIMARY KEY,
    program_name VARCHAR(100) NOT NULL UNIQUE
);

-- =========================
-- SEMESTERS
-- =========================
CREATE TABLE semesters (
    semester_id SERIAL PRIMARY KEY,
    semester_number INT NOT NULL UNIQUE
);

-- =========================
-- TEACHERS
-- =========================
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    teacher_name VARCHAR(100) NOT NULL UNIQUE,
    department VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20)
);

-- =========================
-- STUDENTS (✅ semester_id added)
-- =========================
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    registration_number VARCHAR(50) NOT NULL UNIQUE,
    roll_no VARCHAR(20) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    gender VARCHAR(10),
    date_of_birth DATE,
    program_id INT NOT NULL REFERENCES programs(program_id),
    semester_id INT NOT NULL REFERENCES semesters(semester_id),
    admission_year INT,
    CONSTRAINT uq_roll_per_semester UNIQUE (semester_id, roll_no)
);
-- =========================
-- SUBJECTS
-- =========================
CREATE TABLE subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_code VARCHAR(20) NOT NULL UNIQUE,
    subject_name VARCHAR(100) NOT NULL,
    program_id INT NOT NULL REFERENCES programs(program_id),
    semester_id INT NOT NULL REFERENCES semesters(semester_id),
    subject_type VARCHAR(20) NOT NULL
        CHECK (subject_type IN ('THEORY', 'LAB'))
);

-- =========================
-- SUBJECT ↔ TEACHER
-- =========================
CREATE TABLE subject_teacher (
    id SERIAL PRIMARY KEY,
    subject_id INT NOT NULL REFERENCES subjects(subject_id),
    teacher_id INT NOT NULL REFERENCES teachers(teacher_id),
    teacher_role VARCHAR(10) NOT NULL
        CHECK (teacher_role IN ('THEORY', 'LAB')),
    CONSTRAINT uq_subject_teacher UNIQUE (subject_id, teacher_id, teacher_role)
);

-- =========================
-- ENROLLMENTS
-- Semester is derived from students
-- =========================
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id),
    semester_id INT NOT NULL REFERENCES semesters(semester_id),
    academic_year VARCHAR(20) NOT NULL,
    CONSTRAINT uq_enrollment UNIQUE (student_id, semester_id, academic_year)
);

-- =========================
-- EXAMS
-- =========================
CREATE TABLE exams (
    exam_id SERIAL PRIMARY KEY,
    exam_name VARCHAR(50) NOT NULL UNIQUE,
    applies_to VARCHAR(10) NOT NULL
        CHECK (applies_to IN ('THEORY', 'LAB', 'BOTH'))
);

-- =========================
-- MARKS
-- =========================
CREATE TABLE marks (
    mark_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id),
    subject_id INT NOT NULL REFERENCES subjects(subject_id),
    exam_id INT NOT NULL REFERENCES exams(exam_id),
    marks INT,
    CONSTRAINT uq_marks UNIQUE (student_id, subject_id, exam_id)
);

-- =========================
-- THEORY ATTENDANCE
-- =========================
CREATE TABLE theory_attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id),
    subject_id INT NOT NULL REFERENCES subjects(subject_id),
    attendance_date DATE NOT NULL,
    is_present BOOLEAN DEFAULT FALSE,
    CONSTRAINT uq_theory_attendance
        UNIQUE (student_id, subject_id, attendance_date)
);

-- =========================
-- LAB ATTENDANCE
-- =========================
CREATE TABLE lab_attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(student_id),
    subject_id INT NOT NULL REFERENCES subjects(subject_id),
    attendance_date DATE NOT NULL,
    is_present BOOLEAN DEFAULT FALSE,
    CONSTRAINT uq_lab_attendance
        UNIQUE (student_id, subject_id, attendance_date)
);