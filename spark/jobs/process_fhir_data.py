"""
Spark job to read FHIR JSON data from a specific input path,
validate, FLATTEN it, and write it to a table in the Snowflake RAW schema.
"""
import os
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

# Define the expected schema for the FHIR Patient resource.
FHIR_PATIENT_SCHEMA = StructType([
    StructField("resourceType", StringType(), True),
    StructField("id", StringType(), True),
    StructField("name", ArrayType(StructType([
        StructField("family", StringType(), True),
        StructField("given", ArrayType(StringType()), True)
    ])), True),
    StructField("gender", StringType(), True),
    StructField("birthDate", StringType(), True),
    StructField("address", ArrayType(StructType([
        StructField("city", StringType(), True),
        StructField("state", StringType(), True),
        StructField("postalCode", StringType(), True),
        StructField("country", StringType(), True)
    ])), True),
])


def get_snowflake_options():
    """
    Reads Snowflake connection details from environment variables
    and returns them as a dictionary for the Spark connector.
    """
    return {
        "sfUrl": f"{os.environ['SNOWFLAKE_ACCOUNT']}.snowflakecomputing.com",
        "sfUser": os.environ['SNOWFLAKE_USER'],
        "sfPassword": os.environ['SNOWFLAKE_PASSWORD'],
        "sfDatabase": os.environ['SNOWFLAKE_DATABASE'],
        "sfSchema": "RAW",
        "sfWarehouse": os.environ['SNOWFLAKE_WAREHOUSE'],
        "sfRole": os.environ['SNOWFLAKE_ROLE']
    }


def validate_data(df: DataFrame) -> DataFrame:
    """
    Performs basic validation on the DataFrame.
    """
    return df.filter(
        (col("id").isNotNull()) & (col("resourceType") == "Patient")
    )


def flatten_patient_data(df: DataFrame) -> DataFrame:
    """
    Flattens the nested name and address columns.
    Selects only the first element from the 'name' and 'address' arrays.
    """
    return df.select(
        col("resourceType"),
        col("id"),
        col("name")[0]["family"].alias("name_family"),
        col("name")[0]["given"][0].alias(
            "name_given"),  # Takes the first given name
        col("gender"),
        col("birthDate"),
        col("address")[0]["city"].alias("address_city"),
        col("address")[0]["state"].alias("address_state"),
        col("address")[0]["postalCode"].alias("address_postalcode"),
        col("address")[0]["country"].alias("address_country")
    )


def main():
    """
    Main function to run the Spark job.
    """
    spark = SparkSession.builder \
        .appName("FHIRDataToSnowflake") \
        .getOrCreate()

    input_path = "/opt/bitnami/spark/data/input/fhir_json/"
    print(f"Reading JSON data from {input_path}")
    fhir_df = spark.read.json(
        input_path, schema=FHIR_PATIENT_SCHEMA, multiLine=True)

    validated_fhir_df = validate_data(fhir_df)

    # --- ADDED FLATTENING STEP ---
    flattened_df = flatten_patient_data(validated_fhir_df)

    # --- DEBUGGING ---
    print("--- Row Count of Final DataFrame ---")
    record_count = flattened_df.count()
    print(f"Number of records to be written: {record_count}")

    print("--- Schema and Sample of Final DataFrame ---")
    flattened_df.printSchema()
    flattened_df.show(20, truncate=False)

    # --- OUTPUT ---
    if record_count > 0:
        sf_options = get_snowflake_options()
        print("Writing data to Snowflake table: RAW.PATIENTS...")
        flattened_df.write \
            .format("snowflake") \
            .options(**sf_options) \
            .option("dbtable", "RAW.PATIENTS") \
            .mode("overwrite") \
            .save()
        print("Write to Snowflake complete.")
    else:
        print("DataFrame is empty. Skipping write to Snowflake.")

    print("Spark job finished.")
    spark.stop()


if __name__ == "__main__":
    main()
