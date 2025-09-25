# great_expectations/run_validation.py
import sys
from great_expectations.data_context import DataContext
from great_expectations.exceptions import GreatExpectationsError
from dotenv import load_dotenv

# Always load environment variables at the start
load_dotenv()

# --- SCRIPT CONFIGURATION ---
# This dictionary maps a user-friendly name to the actual GX objects.
# This allows you to easily add more checkpoints in the future.
CHECKPOINT_CONFIG = {
    "bronze_patients_check": {
        "datasource_name": "snowflake_datasource",
        "data_asset_name": "bronze_patients_asset",
        "table_name": "BRONZE_FHIR_PATIENTS",
        "expectation_suite_name": "bronze_patient_suite",
    }
}
# ----------------------------


def run_checkpoint(checkpoint_name: str):
    """
    Runs a Great Expectations validation checkpoint.
    """
    print(f"--- Running Great Expectations Checkpoint: {checkpoint_name} ---")

    if checkpoint_name not in CHECKPOINT_CONFIG:
        print(f"Error: Checkpoint '{checkpoint_name}' is not defined in the configuration.")
        sys.exit(1)

    config = CHECKPOINT_CONFIG[checkpoint_name]
    context_root_dir = "great_expectations/gx"
    context = DataContext(context_root_dir=context_root_dir)

    # Create a checkpoint dynamically in code.
    # This is a robust way to ensure all connections and assets are configured correctly.
    checkpoint = context.add_or_update_checkpoint(
        name=checkpoint_name,
        datasource_name=config["datasource_name"],
        data_asset_name=config["data_asset_name"],
        table_name=config["table_name"],
        expectation_suite_name=config["expectation_suite_name"],
    )

    # Run the checkpoint and get the result
    result = checkpoint.run()

    # Check the validation result and exit with an error code if it fails
    if not result["success"]:
        print("Validation failed!")
        # This is critical for Airflow! Exiting with a non-zero status code
        # tells Airflow that the task has failed.
        sys.exit(1)
    
    print("Validation successful!")
    sys.exit(0)


if __name__ == "__main__":
    # The script expects the name of the checkpoint to run to be passed as an argument.
    # e.g., python run_validation.py bronze_patients_check
    if len(sys.argv) != 2:
        print("Usage: python run_validation.py <checkpoint_name>")
        sys.exit(1)
    
    name_to_run = sys.argv[1]
    run_checkpoint(name_to_run)