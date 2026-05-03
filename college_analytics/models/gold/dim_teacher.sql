select
    teacher_id,
    teacher_name,
    department,
    email,
    phone
from {{ ref('teachers_silver') }}