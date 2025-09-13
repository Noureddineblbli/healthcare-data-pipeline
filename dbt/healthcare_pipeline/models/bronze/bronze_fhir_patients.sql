{{
  config(
    database='HEALTHCARE_DATA_DB',
    schema='BRONZE',
    materialized='table'
  )
}}

select
    ID::string as patient_id,
    GENDER::string as gender,
    NAME_FAMILY::string as family_name,
    NAME_GIVEN::string as given_name,
    ADDRESS_CITY::string as city,
    ADDRESS_STATE::string as state,
    ADDRESS_POSTALCODE::string as postal_code,
    BIRTHDATE::date as birth_date,
    current_timestamp() as _transformed_at
from {{ source('raw', 'patients') }}
