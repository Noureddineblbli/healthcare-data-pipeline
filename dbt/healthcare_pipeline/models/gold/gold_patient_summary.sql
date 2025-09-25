-- models/gold/gold_patient_summary.sql

-- This Gold model aggregates the enriched Silver layer data to create high-value
-- analytics tables. This is the final layer that business users, analysts,
-- and dashboards will query from.

{{
  config(
    materialized='table',
    schema='GOLD'
  )
}}

with patient_demographics as (
    -- Select from the Silver layer model
    select * from {{ ref('silver_patient_demographics') }}
)

select
    -- Dimension: The patient's state (this column comes from the silver model)
    -- THIS IS THE CORRECTED COLUMN NAME
    full_address,

    -- Dimension: Age Category
    age_category,

    -- Dimension: Risk Category
    risk_category,

    -- Metric: Total number of patients
    count(distinct patient_id) as total_patients,

    -- Metric: Average patient age
    avg(current_age) as average_patient_age,

    -- Metric: Number of patients in each standardized gender category
    sum(case when standardized_gender = 'M' then 1 else 0 end) as male_patient_count,
    sum(case when standardized_gender = 'F' then 1 else 0 end) as female_patient_count,
    sum(case when standardized_gender = 'O' then 1 else 0 end) as other_patient_count

from patient_demographics

-- We group by our dimensions to calculate the metrics
group by
    1, 2, 3

-- Order the results for clarity
order by
    full_address,
    age_category