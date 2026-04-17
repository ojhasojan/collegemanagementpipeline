-- =========================
-- PROGRAMS TABLE
-- =========================
CREATE TABLE programs (
    program_id SERIAL PRIMARY KEY,
    program_name VARCHAR(100) NOT NULL UNIQUE
);

-- =========================
-- SEMESTERS TABLE
-- =========================
CREATE TABLE semesters (
    semester_id SERIAL PRIMARY KEY,
    semester_number INT NOT NULL UNIQUE
);

-- =========================
-- STUDENTS TABLE
-- =========================
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    registration_number VARCHAR(50) UNIQUE NOT NULL,
    roll_no VARCHAR(20) UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50),
    gender VARCHAR(10),
    date_of_birth DATE,
    program_id INT REFERENCES programs(program_id),
    admission_year INT
);

-- =========================
-- TEACHERS TABLE
-- =========================
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    teacher_name VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    email VARCHAR(100)
);

-- =========================
-- SUBJECTS TABLE
-- =========================
CREATE TABLE subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_code VARCHAR(20) UNIQUE,
    subject_name VARCHAR(100) NOT NULL,
    program_id INT REFERENCES programs(program_id),
    semester_id INT REFERENCES semesters(semester_id),
    subject_type VARCHAR(20) CHECK (subject_type IN ('THEORY','LAB'))
);

-- =========================
-- SUBJECT-TEACHER MAPPING
-- =========================
CREATE TABLE subject_teacher (
    id SERIAL PRIMARY KEY,
    subject_id INT REFERENCES subjects(subject_id),
    teacher_id INT REFERENCES teachers(teacher_id),
    teacher_role VARCHAR(10) CHECK (teacher_role IN ('THEORY', 'LAB'))
);

-- =========================
-- ENROLLMENTS TABLE
-- =========================
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    semester_id INT REFERENCES semesters(semester_id),
    academic_year VARCHAR(20)
);

-- =========================
-- EXAMS TABLE
-- =========================
CREATE TABLE exams (
    exam_id SERIAL PRIMARY KEY,
    exam_name VARCHAR(50) UNIQUE NOT NULL,
    applies_to VARCHAR(10) NOT NULL CHECK (applies_to IN ('THEORY', 'LAB', 'BOTH'))
);

-- =========================
-- MARKS TABLE
-- =========================
CREATE TABLE marks (
    mark_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    subject_id INT REFERENCES subjects(subject_id),
    exam_id INT REFERENCES exams(exam_id),
    marks INT
);

-- =========================
-- THEORY ATTENDANCE
-- =========================
CREATE TABLE theory_attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    subject_id INT REFERENCES subjects(subject_id),
    total_classes INT,
    attended_classes INT
);

-- =========================
-- LAB ATTENDANCE
-- =========================
CREATE TABLE lab_attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    subject_id INT REFERENCES subjects(subject_id),
    total_classes INT,
    attended_classes INT
);