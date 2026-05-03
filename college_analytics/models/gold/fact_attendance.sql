select
    a.student_id,
    a.registration_number,
    a.student_name,
    a.subject_code,
    a.subject_name,
    a.attendance_type,
    a.attendance_date,
    a.is_present
from {{ ref('attendance_silver') }} a