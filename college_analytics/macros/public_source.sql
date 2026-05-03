{% macro public_source(table_name) %}
    select *
    from public.{{ table_name }}
{% endmacro %}