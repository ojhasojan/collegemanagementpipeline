select
    sub.subject_id,
    sub.subject_code,
    sub.subject_name,
    sub.subject_type,
    p.program_name,
    sem.semester_number
from {{ ref('subjects_bronze') }} sub
join {{ ref('programs_bronze') }} p
    on sub.program_id = p.program_id
join {{ ref('semester_bronze') }} sem
    on sub.semester_id = sem.semester_id
