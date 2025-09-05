# -----------------------------------------------------------------------------
# SNOWFLAKE CONNECTION & AUTHENTICATION VARIABLES
#
# These variables are used by the Snowflake provider to connect and authenticate
# to your Snowflake account.
# -----------------------------------------------------------------------------

variable "snowflake_account" {
  type        = string
  description = "The unique identifier for your Snowflake account (e.g., YOXMCQX-WZ49440)."
  default     = "YOXMCQX-WZ49440"
}

variable "snowflake_user" {
  type        = string
  description = "The username for the Snowflake account."
  default     = "NOURDDINE"
}

variable "snowflake_password" {
  type        = string
  description = "The password for the Snowflake user. Should be set via an environment variable for security."
  sensitive   = true # This prevents Terraform from ever displaying this value in logs or outputs.
}

variable "snowflake_role" {
  type        = string
  description = "The default role to use for the Snowflake session. ACCOUNTADMIN is used for initial setup."
  default     = "ACCOUNTADMIN"
}


# -----------------------------------------------------------------------------
# INFRASTRUCTURE CONFIGURATION VARIABLES
#
# These variables define the names and settings for the resources we will create,
# such as the warehouse, database, and schemas.
# -----------------------------------------------------------------------------

variable "warehouse_name" {
  type        = string
  description = "The name of the virtual warehouse to create for the healthcare pipeline."
  default     = "HEALTHCARE_PIPELINE_WH"
}

variable "warehouse_size" {
  type        = string
  description = "The size of the virtual warehouse. Valid sizes: X-SMALL, SMALL, MEDIUM, etc."
  default     = "X-SMALL"
}

variable "database_name" {
  type        = string
  description = "The name of the central database for the healthcare data."
  default     = "HEALTHCARE_DATA_DB"
}

variable "schema_names" {
  type        = list(string)
  description = "A list of schema names to create, following the medallion data architecture pattern."
  default     = ["RAW", "BRONZE", "SILVER", "GOLD"]
}