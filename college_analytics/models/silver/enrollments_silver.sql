select
    e.enrollment_id,
    s.student_id,
    s.registration_number,
    s.student_name,
    e.academic_year,
    sem.semester_number,
    s.program_name
from {{ ref('enrollments_bronze') }} e
join {{ ref('students_silver') }} s
    on e.student_id = s.student_id
join {{ ref('semester_bronze') }} sem
    on e.semester_id = sem.semester_id