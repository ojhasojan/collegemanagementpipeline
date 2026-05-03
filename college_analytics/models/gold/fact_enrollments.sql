select
    e.student_id,
    e.registration_number,
    e.student_name,
    e.program_name,
    e.semester_number,
    e.academic_year
from {{ ref('enrollments_silver') }} e