-- models/silver/silver_patient_demographics.sql

-- This Silver model reads from the clean Bronze patient data and applies
-- business-specific logic and enrichments. The goal is to create a dataset
-- that is easy for analysts to understand and use.


{{
  config(
    materialized='table',
    schema='SILVER'
  )
}}

with bronze_patients as (
    -- We use the ref() function to select from our existing dbt model.
    -- This is dbt's way of managing dependencies between models.
    select * from {{ ref('bronze_fhir_patients') }}
)

select
    -- Pass through the unique patient identifier
    patient_id,

    -- Standardize text fields: trim whitespace and convert to proper case
    trim(initcap(given_name)) as standardized_given_name,
    trim(initcap(family_name)) as standardized_family_name,

    -- Standardize GENDER field into single-letter codes for consistency
    case 
        when lower(gender) = 'male' then 'M'
        when lower(gender) = 'female' then 'F'
        else 'O'
    end as standardized_gender,

    -- Keep the original birth date for reference
    birth_date,

    -- Calculate patient's current age. This is a valuable derived field.
    datediff(year, birth_date, current_date()) as current_age,
    
    -- Apply age categorization based on healthcare business rules
    case 
        when current_age <= 17 then 'Pediatric'
        when current_age >= 18 and current_age <= 64 then 'Adult'
        when current_age >= 65 then 'Senior'
        else 'Unknown'
    end as age_category,

    -- Standardize and combine address fields into a single, clean address line
    -- Handle potential nulls with COALESCE to avoid empty strings
    coalesce(trim(initcap(city)), 'Unknown City') || ', ' || 
    coalesce(trim(upper(state)), 'N/A') || ' ' || 
    coalesce(postal_code, '') as full_address,

    -- Simple risk category assignment (example of a clinical business rule)
    -- A more complex model could join with conditions or lab results.
    case
        when age_category = 'Senior' then 'High Risk'
        else 'Standard Risk'
    end as risk_category,

    _transformed_at

from bronze_patients
where
    -- Data quality improvement: only include records with a valid patient_id
    patient_id is not null