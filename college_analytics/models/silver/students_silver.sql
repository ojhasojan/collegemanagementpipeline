select
    s.student_id,
    s.registration_number,
    concat(s.first_name, ' ', s.last_name) as student_name,
    s.roll_no,
    p.program_name,
    sem.semester_number,
    s.gender,
    s.admission_year
from {{ ref('students_bronze') }} s
join {{ ref('programs_bronze') }} p
    on s.program_id = p.program_id
join {{ ref('semester_bronze') }} sem
    on s.semester_id = sem.semester_id
