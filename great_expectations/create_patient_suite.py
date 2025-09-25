import great_expectations as gx
import os
from dotenv import load_dotenv
load_dotenv()

# This is the V3 Fluent Datasources method.
# It does not use DataContext for the connection.
context = gx.data_context.DataContext()

# Define connection string from environment variables
snowflake_connection_str = "snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}".format(
    user=os.environ["SNOWFLAKE_USER"],
    password=os.environ["SNOWFLAKE_PASSWORD"],
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    database=os.environ["SNOWFLAKE_DATABASE"],
    schema="BRONZE",
    warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
    role=os.environ["SNOWFLAKE_ROLE"],
)

# Use SQL datasource for Snowflake (it's essentially the same thing)
datasource = context.sources.add_sql(
    name="snowflake_datasource", 
    connection_string=snowflake_connection_str
)

data_asset = datasource.add_table_asset(
    name="bronze_patients_asset", 
    table_name="BRONZE_FHIR_PATIENTS"
)

batch_request = data_asset.build_batch_request()

# Create the Expectation Suite
suite = context.add_or_update_expectation_suite(
    expectation_suite_name="bronze_patient_suite"
)

# Create a Validator
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite=suite,
)

print("--- Successfully connected. Creating and running Expectations... ---")

# Add expectations
validator.expect_column_values_to_not_be_null(column="PATIENT_ID")
validator.expect_column_values_to_be_in_set(
    column="GENDER", value_set=["male", "female", "other", "unknown"])
validator.expect_column_value_lengths_to_equal(column="POSTAL_CODE", value=5)
validator.expect_column_values_to_not_be_null(column="BIRTH_DATE")

# Save the suite to the context (which will save it to a file)
validator.save_expectation_suite()

print("\n--- Success! ---")
print("Expectation Suite 'bronze_patient_suite' was created and saved.")

# Optional: Run the validation to see the results immediately
result = validator.validate()
print("\n--- Validation Results ---")
print(result)
