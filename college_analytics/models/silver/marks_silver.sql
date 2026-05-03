select
    m.mark_id,
    s.student_id,
    s.registration_number,
    s.student_name,
    sub.subject_code,
    sub.subject_name,
    sub.subject_type,
    e.exam_name,
    m.marks,
    s.program_name,
    s.semester_number
from {{ ref('marks_bronze') }} m
join {{ ref('students_silver') }} s
    on m.student_id = s.student_id
join {{ ref('subjects_silver') }} sub
    on m.subject_id = sub.subject_id
join {{ ref('exams_bronze') }} e
    on m.exam_id = e.exam_id
