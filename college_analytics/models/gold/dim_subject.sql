select
    subject_id,
    subject_code,
    subject_name,
    subject_type,
    program_name,
    semester_number
from {{ ref('subjects_silver') }}