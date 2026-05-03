select
    t.teacher_id,
    t.teacher_name,
    t.department,
    t.email,
    t.phone
from {{ ref('teacher_bronze') }} t