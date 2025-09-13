{% macro generate_schema_name(custom_schema_name, node) -%}
    {{ custom_schema_name | upper if custom_schema_name else target.schema }}
{%- endmacro %}
