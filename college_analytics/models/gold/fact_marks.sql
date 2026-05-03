select
    m.student_id,
    m.registration_number,
    m.student_name,
    m.subject_code,
    m.subject_name,
    m.exam_name,
    m.marks
from {{ ref('marks_silver') }} m