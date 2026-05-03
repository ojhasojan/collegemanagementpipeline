select
    student_id,
    registration_number,
    student_name,
    roll_no,
    program_name,
    semester_number,
    gender,
    admission_year
from {{ ref('students_silver') }}