select
    ta.attendance_id,
    s.student_id,
    s.registration_number,
    s.student_name,
    sub.subject_code,
    sub.subject_name,
    'THEORY' as attendance_type,
    ta.attendance_date,
    ta.is_present,
    s.program_name,
    s.semester_number
from {{ ref('theory_attendance_bronze') }} ta
join {{ ref('students_silver') }} s
    on ta.student_id = s.student_id
join {{ ref('subjects_silver') }} sub
    on ta.subject_id = sub.subject_id

union all

select
    la.attendance_id,
    s.student_id,
    s.registration_number,
    s.student_name,
    sub.subject_code,
    sub.subject_name,
    'LAB' as attendance_type,
    la.attendance_date,
    la.is_present,
    s.program_name,
    s.semester_number
from {{ ref('lab_attendance_bronze') }} la
join {{ ref('students_silver') }} s
    on la.student_id = s.student_id
join {{ ref('subjects_silver') }} sub
    on la.subject_id = sub.subject_id